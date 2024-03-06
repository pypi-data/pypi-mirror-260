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

from Cheetah.Template import Template

# linting cheetah source
from Cheetah import (
  NameMapper,
  Parser )

from partis.utils import (
  indent_lines,
  line_segment )

from partis.schema_meta.base import (
  SchemaHint,
  Loc,
  SchemaEvaluationError )

from .eval import (
  ProviderSupport,
  Provider,
  Evaluated )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CheetahProvider( Provider ):
  """Evaluates cheetah template expressions
  """

  TAG_TMPL_CHEETAH = "$tmpl:cheetah"

  #-----------------------------------------------------------------------------
  def __init__( self ):
    super().__init__()

    self._supported = dict(
      tmpl_cheetah = ProviderSupport(
        name = "Cheetah template",
        lexer = 'cheetah',
        doc = f"escaped string: `{self.TAG_TMPL_CHEETAH} ...`") )

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return self._supported

  #-----------------------------------------------------------------------------
  def check( self, src ):

    if isinstance( src, str ):

      if src.startswith("$tmpl:cheetah"):
        # cheetah template
        tmpl = src[len("$tmpl:cheetah"):]

        if tmpl.startswith("\n"):
          tmpl = tmpl[1:]

        return self.supported['tmpl_cheetah'], tmpl

    return None

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    if support is self.supported['tmpl_cheetah']:
      # cheetah template
      return f"{self.TAG_TMPL_CHEETAH}\n{src}"


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
      if support is self.supported['tmpl_cheetah']:
        # cheetah template

        return str( Template( src, searchList = [ locals ] ) )

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

    if support is self.supported['tmpl_cheetah']:
      # cheetah template

      return self.lint_cheetah( src, loc, locals )

  #-----------------------------------------------------------------------------
  def lint_cheetah( self, src, loc, locals ):
    if loc is None:
      loc = Loc()
      
    hints = list()

    try:

      val = str( Template( src, searchList = [ locals ] ) )

    except NameMapper.NotFound as e:

      hints.append( SchemaHint(
        str(e),
        loc = loc,
        level = 'warning' ) )

    except Parser.ParseError as e:
      if e.lineno:
        lineno = e.lineno
        col = e.col or 1
        line = e.stream.splitlines()[lineno-1]

      else:
        lineno, col, line = e.stream.getRowColLine()


      msg = e.msg

      loc = loc.replace( line = lineno, col = col )

      offset = col - 1
      idx = lineno - 1

      if line:
        msg += f"\n{indent_lines(2, line)}\n"
        msg += '  ' + ' '*offset + '^'

      hints.append( SchemaHint(
        msg,
        loc = loc,
        level = 'error' ) )


    return hints

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cheetah_provider = CheetahProvider()

class CheetahEvaluated( Evaluated, provider = cheetah_provider ):
  pass
