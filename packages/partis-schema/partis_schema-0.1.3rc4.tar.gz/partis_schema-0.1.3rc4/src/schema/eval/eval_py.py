# -*- coding: UTF-8 -*-
import os
import sys
import inspect
import weakref
from inspect import getframeinfo, stack
import traceback
import linecache
from copy import copy, deepcopy
import importlib

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  ModelError,
  ModelHint,
  fmt_obj,
  indent_lines,
  split_lines,
  line_segment )

# linting python source
from partis.utils.lint import (
  lint_python )

from partis.schema_meta.base import (
  SchemaHint,
  Loc,
  SchemaEvaluationError )

from .eval import (
  ProviderSupport,
  Provider,
  Evaluated )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def extract_exec_stack( src, e, filename, funcname, mode ):
  # extract traceback information
  if isinstance( e, ModelError ):
    hint = SchemaHint(
      msg = e.msg,
      data = e.data,
      format = e.format,
      loc = e.loc,
      level = e.level,
      hints = e.hints )

  else:
    hint = SchemaHint(
      msg = type(e).__name__,
      data = fmt_obj(e, width = 100, height = 1 ),
      format = 'literal',
      level = 'error' )

  prev_hint = hint

  _stack = list( traceback.walk_tb( e.__traceback__ ) )

  lines = split_lines(src)
  line_offset = 0

  # first determin the offset of the function body for the user's code
  for frame, lineno in _stack:
    code = frame.f_code

    if code.co_filename == filename:
      if code.co_name == funcname:
        line_offset = code.co_firstlineno
        break

  # build trace starting at deepest point
  for frame, lineno in _stack[::-1]:

    code = frame.f_code

    if code.co_filename == filename:
      # remove the offset line-number to the function

      if code.co_name == funcname:
        # stop as soon as traceback reaches main code level
        _lineno = lineno - line_offset

        return SchemaHint(
          f"During `{mode}`",
          # data = linecache.getline( code.co_filename, lineno ).strip(),
          data = lines[lineno-1].strip() if (lineno > 0 and lineno <= len(lines)) else None,
          loc = Loc(
            filename = 'compiled source',
            line = _lineno ),
          format = 'block',
          level = 'debug',
          hints = prev_hint )

    else:

      prev_hint = SchemaHint(
        f"During `{code.co_name}`",
        data = '`' + linecache.getline( code.co_filename, lineno ).strip() + '`',
        format = 'block',
        loc = Loc(
          filename = code.co_filename,
          line = lineno ),
        level = 'debug',
        hints = prev_hint )

  return prev_hint

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvalFunc:
  #-----------------------------------------------------------------------------
  def __init__( self, func ):
    if not callable(func):
      raise ValueError(f"`func` must be callable: {type(func).__name__}")

    self._func = func

  #-----------------------------------------------------------------------------
  def __call__( self, **kwargs ):
    return self._func( **kwargs )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PyProvider( Provider ):
  """Evaluates python expressions
  """

  TAG_EXPR_PY = "$expr:py"
  TAG_FUNC_PY = "$func:py"

  #-----------------------------------------------------------------------------
  def __init__( self, restricted = False ):
    super().__init__()

    self._restricted = bool(restricted)

    self._supported = dict(
      expr_py = ProviderSupport(
        name = "Python expression",
        lexer = 'python',
        doc = f"escaped string: `{self.TAG_EXPR_PY} ...`" ),
      func_py = ProviderSupport(
        name = "Python function",
        lexer = 'python',
        doc = f"escaped string: `{self.TAG_FUNC_PY} ...`" ),
      call_py = ProviderSupport(
        name = "Python callable",
        doc = "instance of EvalFunc" ) )

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return self._supported

  #-----------------------------------------------------------------------------
  def check( self, src ):

    if isinstance( src, EvalFunc ):
      return self.supported['call_py'], src._func

    if isinstance( src, str ):

      if src.startswith(self.TAG_EXPR_PY):
        # python expression
        return self.supported['expr_py'], src[len(self.TAG_EXPR_PY):]

      elif src.startswith(self.TAG_FUNC_PY):
        # python function
        return self.supported['func_py'], src[len(self.TAG_FUNC_PY):]

    return None

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    if support is self.supported['call_py']:
      return EvalFunc( func = src )

    elif support is self.supported['expr_py']:
      # python expression
      return self.TAG_EXPR_PY + src

    elif support is self.supported['func_py']:
      # python function
      return self.TAG_FUNC_PY + src

    raise ValueError(f"`support` must be one of {self.supported.values()}: {support}")

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    loc = None,
    locals = None,
    module = None,
    logger = None ):

    if locals is None:
      locals = dict()

    if logger is None:
      logger = log

    supported = self.check( src )

    if not supported:
      raise SchemaEvaluationError(f"No evaluation support: {src}")

    support, src = supported

    # ensure currend directory is preserved after executing script
    cwd = os.path.abspath( os.getcwd() )

    try:

      if support == self.supported['call_py']:
        return src( **locals )

      elif support in [ self.supported['expr_py'], self.supported['func_py'] ]:

        def _print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False):


          if file is sys.stdout:
            msg = sep.join([ str(o) for o in objects])
            logger.info( msg )
          elif file is sys.stderr:
            msg = sep.join([ str(o) for o in objects])
            logger.error( msg )
          else:
            print( *objects, sep=sep, end=end, file=file, flush=flush )

        if module is None:
          module = schema.__module__

        if isinstance( module, str ):
          module = importlib.import_module(module)

        gvars = {
          '__name__' : module.__name__,
          '__file__' : module.__file__ if hasattr(module, '__file__') else None,
          '__builtins__' : {
            **__builtins__,
            'print' : _print } }

        if support == self.supported['expr_py']:
          # python expression

          lvars = dict(locals)

          try:
            return eval( src, gvars, lvars )

          except BaseException as e:
            ehint = extract_exec_stack( src, e, '<string>', '<module>', 'eval' )

            raise SchemaEvaluationError(
              f"Error in Python eval",
              hints = ehint ) from None

        elif support == self.supported['func_py']:
          # python function

          lvars = dict(
            __result = None,
            __kwargs = locals )

          # add indentation
          _src = "\n".join([ ("  " + l) for l in src.splitlines() ])

          var_keys = ", ".join([ k for k,v in locals.items() ])

          filename = "__src_code_py"
          funcname = "__func_py"

          _src = f"\ndef {funcname}({var_keys}):\n{ _src }\n\n__result = {funcname}(**__kwargs)"

          try:
            src_code = compile( _src, filename, "exec" )

          except BaseException as e:
            raise SchemaEvaluationError(
              f"Error in Python compile",
              hints = SchemaHint.cast( e ) ) from e

          try:
            exec( src_code, gvars, lvars )

          except BaseException as e:
            ehint = extract_exec_stack( _src, e, filename, funcname, 'exec' )

            raise SchemaEvaluationError(
              f"Error in Python exec",
              hints = ehint ) from None

          return lvars['__result']


      assert False, str(support)

    finally:
      os.chdir( cwd )

  #-----------------------------------------------------------------------------
  def lint( self,
    schema,
    src,
    loc = None,
    locals = None,
    module = None,
    logger = None ):

    supported = self.check( src )

    if not supported:
      raise SchemaEvaluationError(f"No evaluation support: {src}")

    support, src = supported

    if support == self.supported['call_py']:
      return list()

    elif support == self.supported['expr_py']:

      return lint_python(
        src,
        locals,
        loc = loc,
        mode = 'expr',
        restricted = self._restricted )

    elif support == self.supported['func_py']:

      return lint_python(
        src,
        locals,
        loc = loc,
        mode = 'func',
        restricted = self._restricted )



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
py_provider = PyProvider()

class PyEvaluated( Evaluated, provider = py_provider ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
py_provider_restricted = PyProvider( restricted = True )

class PyEvaluatedRestricted( Evaluated, provider = py_provider_restricted ):
  pass
