import logging
log = logging.getLogger( __name__ )

from copy import copy
import inspect

from partis.utils import (
  adict,
  odict,
  fmt_obj )

from partis.utils.special import (
  required,
  optional )

from partis.schema_meta.eval import (
  ProviderMeta,
  Provider,
  ProviderSupport,
  EvaluatedContextMeta,
  EvaluatedContext,
  EvaluatedMeta )

from partis.schema_meta.base import (
  SchemaError,
  SchemaEvaluationError,
  SchemaHint,
  Loc,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_schema_prim,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  is_evaluated,
  is_valued,
  is_optional,
  is_required )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _ctx_default( context, context_compat ):
  if context is None:
    # empty 'None' context
    context = EvaluatedContext()

  elif is_mapping( context ):
    # convert regular mappings to a 'None' context with the values
    context = ConstEvaluatedContext( context )

  if not is_sequence( context ):
    context = [ context, ]

  # filter out incompatible contexts
  # NOTE: use of `==` is intended here, instead of `isinstance`, because the
  # equality is compared by the `id` of the respective classes, not a strict
  # inheritance relationship
  context = [ c for c in context if type(c) == context_compat ]

  return context

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ConstEvaluatedContext( EvaluatedContext ):
  """Constant namespace for all evaluations
  """
  #-----------------------------------------------------------------------------
  def __init__( self, locals = None ):
    super().__init__()

    self._p_locals = dict(locals) if locals else dict()

  #-----------------------------------------------------------------------------
  def locals( self, schema ):

    return self._p_locals

  #-----------------------------------------------------------------------------
  def __call__( self,
    schema,
    parent,
    key ):

    return self

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Evaluated( metaclass = EvaluatedMeta ):
  """Base class for evaluated sources

  Parameters
  ----------
  schema : :class:`Schema <partis.schema.Schema>`
  src : object
    Source data to be evaluated.
  loc : :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)

  Note
  ----
  If an expression returns `None`, the default value specified by the schema
  will be used as the result of the expression.
  This could cause an error when the expression evaluates to None, and the default
  value of the schema is also an expression.
  This could also cause an error if the default value, if it is an expression,
  evaluated to None, since this would then result in the same un-evaluated expression.

  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    schema,
    src,
    loc = None ):

    if not is_schema( schema ):
      raise SchemaError(
        f"`schema` must be instance of `Schema` or `SchemaPrim`: {type(schema)}")

    if loc is None:
      loc = Loc()

    if not isinstance( loc, Loc ):
      raise SchemaError(
        f"`loc` must be instance of `Loc`: {type(loc)}")

    self._p_schema = schema
    self._p_src = src
    self._p_loc = loc

  #-----------------------------------------------------------------------------
  def __eq__( self, other ):
    if is_valued(other):
      return self._src == other

    return self._src == other._src

  #-----------------------------------------------------------------------------
  def __ne__( self, other ):
    return not (self == other)

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return f"{type(self).__name__}({self._src})"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  @property
  def _provider( self ):
    return type(self).provider

  #-----------------------------------------------------------------------------
  @property
  def _context( self ):
    return type(self).context

  #-----------------------------------------------------------------------------
  @property
  def _schema( self ):
    return self._p_schema

  #-----------------------------------------------------------------------------
  @property
  def _src( self ):
    return self._p_src

  #-----------------------------------------------------------------------------
  @property
  def _loc( self ):
    return self._p_loc

  #-----------------------------------------------------------------------------
  @property
  def _encode( self ):
    return type(self).escaped( *(type(self).check( self._src )) )

  #-----------------------------------------------------------------------------
  def _lint( self,
    context = None,
    logger = None ):
    """Lints source

    Parameters
    ----------
    context : None | :class:`EvaluatedContext` | list[ :class:`EvaluatedContext` ]
      Sets the context for which this expression is to be evaluated.
      The expression is evaluated only when the specified context is equivalent
      to the one for this evaluated class.
    logger : logging.Logger
      A logger object to direct expression logs/prints instead of stdout

    Returns
    -------
    : list[SchemaHint]

    """

    context = _ctx_default( context, self._context )

    if len(context) == 0:
      # only evaluate if specified context does not exclude this evaluation
      return list()

    context = next(iter(context))

    if self._provider is None:
      # TODO: why is this not done in the initializer?
      raise SchemaError(f"May not perform evaluation without a `provider`")

    try:
      hints = self._provider.lint(
        schema = self._schema,
        src = self._src,
        loc = self._loc,
        locals = adict( context.locals(
          schema = self._schema ) ),
        module = context.module,
        logger = logger )

    except BaseException as e:

      raise SchemaEvaluationError(
        f"Linting failed",
        loc = self._loc,
        hints = [
          f"source: {self._src}",
          f"context: {context}",
          SchemaHint.cast( e ) ] ) from e

    return hints

  #-----------------------------------------------------------------------------
  def _eval( self,
    context = None,
    logger = None ):
    """Evaluates source

    Parameters
    ----------
    context : None | :class:`EvaluatedContext` | list[ :class:`EvaluatedContext` ]
      Sets the context for which this expression is to be evaluated.
      The expression is evaluated only when the specified context is equivalent
      to the one for this evaluated class.
    logger : logging.Logger
      A logger object to direct expression logs/prints instead of stdout

    Returns
    -------
    : object

    """

    context = _ctx_default( context, self._context )

    if len(context) == 0:
      # only evaluate if specified context does not exclude this evaluation
      return self

    context = next(iter(context))

    if self._provider is None:
      # TODO: why is this not done in the initializer?
      raise SchemaError(f"May not perform evaluation without a `provider`")

    try:
      _val = self._provider.eval(
        schema = self._schema,
        src = self._src,
        loc = self._loc,
        locals = adict( context.locals(
          schema = self._schema ) ),
        module = context.module,
        logger = logger )

    except BaseException as e:

      raise SchemaEvaluationError(
        f"Evaluation failed",
        loc = self._loc,
        hints = [
          f"source: {self._src}",
          f"context: {context}",
          SchemaHint.cast( e ) ] ) from e

    try:
      val = self._schema.decode(
        val = _val,
        loc = self._loc )

    except BaseException as e:

      raise SchemaEvaluationError(
        f"Evaluation result not decoded by schema",
        loc = self._loc,
        hints = [
          f"source: {self._src}",
          f"context: {context}",
          f"result: {fmt_obj(_val)}",
          SchemaHint.cast( e ) ] ) from e

    if not is_valued(val):
      if (
        is_evaluated( val._src )
        and _val is None
        and val._src._src == self._src ):

        # NOTE: this means the default value is itself an expression, and the source
        # code is the same, so evaluating the default value will currently cause
        # infinite recursion.

        if is_required( self._schema.default_eval ):
          # No default eval given to use in this case

          raise SchemaEvaluationError(
            f"Evaluation resulted in another evaluation from default values",
            loc = self._loc,
            hints = [
              f"source: {self._src}",
              f"context: {context}",
              f"result: {fmt_obj(_val)}",
              f"decoded: {fmt_obj(val)}" ] )

        val = self._schema.default_eval

        # the machinery should have ensured default_eval is valued
        assert is_valued(val)

      else:
        # NOTE: It's not clear the constraints that should be placed on recursively
        # evaluating expressions. For instance, an expression that evaluates to
        # a path that then evaluates to a relative/absolute path would be ok, but
        # maybe not to another general expression.
        val = val._eval(
          context = context,
          logger = logger )

    return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NotEvaluated( Evaluated ):
  pass
