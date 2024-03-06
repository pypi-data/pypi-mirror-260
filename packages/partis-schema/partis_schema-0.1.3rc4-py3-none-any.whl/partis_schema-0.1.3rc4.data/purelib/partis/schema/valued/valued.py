import logging
log = logging.getLogger( __name__ )

from copy import copy

from partis.utils import (
  ModelHint,
  adict,
  adict_struct,
  odict,
  attrs_modify )


from partis.utils.special import (
  required,
  optional )

from partis.schema_meta.valued import (
  ValuedMeta )

from partis.schema_meta.base import (
  SchemaError,
  SchemaHint,
  Bias,
  Loc,
  assert_valid_name,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_special,
  is_optional,
  is_required,
  is_derived,
  is_similar_value_type,
  is_schema_prim,
  is_schema_declared,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  is_evaluated_class,
  is_evaluated,
  is_valued,
  is_valued_type,
  any_schema )

from partis.schema import (
  EvaluatedContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_schema_loc( val, schema = None, loc = None ):

  if is_valued_type( val ):
    # copy source information to prevent chaining
    if schema is None:
      schema = val._schema

    if loc is None:
      loc = val._loc

    # NOTE: this is necessary before checking for is_evaluated
    val = val._src

  if is_evaluated( val ):
    if schema is None:
      schema = val._schema

    if loc is None:
      loc = val._loc

  if loc is None:
    loc = Loc()

  return schema, loc

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_init_val( val, schema, default_val ):

  if val is None or not (
    is_valued( val )
    or is_sequence( val )
    or is_mapping( val ) ):

    # dummy value
    if schema is None:
      schema, loc = get_schema_loc(
        val = val )

    if not (
      schema is None
      or schema.init_val is None ):

      val = schema.init_val

    else:
      val = default_val

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_src_val( val ):

  if is_valued_type( val ):
    val = val._src

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Valued( metaclass = ValuedMeta ):
  """Base class of schema primitive values

  Parameters
  ----------
  val : object
    Source data to be evaluated
  schema : :class:`Schema <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  loc : :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    val = None,
    schema = None,
    loc = None,
    bias = None ):

    if bias is None:
      bias = Bias()

    self._p_bias = bias

    self._p_src = get_src_val( val )

    if not is_valued( self._p_src ):
      self._p_valued = False

    else:
      self._p_valued = True

    if not ( schema is None or is_schema( schema ) ):
      raise SchemaError(
        f"`schema` must be instance of `Schema` or `SchemaPrim`: {type(schema)}")

    if not ( loc is None or isinstance( loc, Loc ) ):
      raise SchemaError(
        f"`loc` must be instance of `Loc`: {type(loc)}")

    schema, loc = get_schema_loc(
      val = val,
      schema = schema,
      loc = loc )

    self._p_schema = schema
    self._p_loc = loc

  #-----------------------------------------------------------------------------
  def _assert_valued(self):
    if not self._valued:
      raise ValueError(f"{type(self).__name__} not yet evaluated: {self._src}")

  #-----------------------------------------------------------------------------
  def model_hint( self ):
    if self._schema is None:
      name = type(self).__name__

    else:
      name = self._schema.__name__

      if name.endswith('_schema'):
        name = name[:-7]

    hints = list()

    if is_sequence(self):
      for i,v in enumerate(self):
        hints.append(ModelHint.cast(v))

      return ModelHint(
        f"<{name}>",
        level = 'info',
        hints = hints )

    elif is_mapping(self):
      from partis.schema.prim import (
        SeqPrimDeclared,
        SeqPrim,
        MapPrimDeclared,
        MapPrim )

      for k,v in self.items():
        if v is None:
          continue

        if not is_valued_type(v):
          hints.append(ModelHint(
            f"{k}",
            data = v ))

        elif (
          not is_schema_prim( v._schema )
          or isinstance(v._schema, (
            SeqPrim,
            SeqPrimDeclared,
            MapPrim,
            MapPrimDeclared)) ):


          # Cast 'non-trivial' values to full hint object
          hint = ModelHint.cast(v)
          hint.msg = f"{k}"
          hints.append(hint)

        else:
          # 'trivial' values formatted directly into key's hint
          hints.append(ModelHint(
            f"{k}",
            data = v._encode,
            loc = v._loc ))

      return ModelHint(
        data = f"<{name}>",
        level = 'info',
        loc = self._loc,
        hints = hints )

    else:
      return ModelHint(
        data = self._encode,
        loc = self._loc)

  #-----------------------------------------------------------------------------
  def __rich__( self ):
    return ModelHint.cast(self).fmt( with_rich = True )

  #-----------------------------------------------------------------------------
  def __copy__( self ):
    return type(self)(
      val = self,
      loc = self._loc )

  #-----------------------------------------------------------------------------
  def __eq__( self, other ):

    va = is_evaluated(self)
    vb = is_evaluated(other)

    if va:
      if vb:
        return self._src == other._src
      else:
        return self._src == other

    elif vb:
      return self == other._src

    # neither are evaluated

    return super().__eq__( other )

  #-----------------------------------------------------------------------------
  def __ne__( self, other ):
    return not (self == other)

  #-----------------------------------------------------------------------------
  def __hash__( self ):
    if not is_valued(self):
      return hash(self._src)

    return super().__hash__()

  #-----------------------------------------------------------------------------
  @property
  def _schema( self ):
    return self._p_schema

  #-----------------------------------------------------------------------------
  @property
  def _loc( self ):
    return self._p_loc

  #-----------------------------------------------------------------------------
  @property
  def _valued( self ):
    return self._p_valued

  #-----------------------------------------------------------------------------
  @property
  def _src( self ):
    return self._p_src


  #-----------------------------------------------------------------------------
  @property
  def _bias( self ):
    r"""A metric of how biased (selective) the value is to the ``_schema``

    This may be interpreted as the number of needed independent binary decisions
    (questions, or conditional statements) to determine that the value satisfied
    the schema.

    Returns
    -------
    float
    """
    return self._p_bias

  #-----------------------------------------------------------------------------
  @property
  def _encode( self ):
    if self._valued:
      return self._src

    if is_evaluated( self._src ):
      return self._src._encode

    assert False


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

    See Also
    --------
    :class:`Evaluated <partis.schema.eval.Evaluated>`
    """

    hints = list()

    if self._valued:
      return hints

    if is_evaluated( self._p_src ):

      hints.extend( self._p_src._lint(
        context = context,
        logger = logger ) )

    elif is_sequence( self._p_src ):

      # local variables for items in list or dictionary
      # NOTE: parent of items is the current value, parent of current will be
      # parent of the item parent

      for i, v in enumerate(self._p_src):
        if not is_valued(v):

          if isinstance( context, EvaluatedContext ):
            _context = context(
              schema = self._schema,
              parent = self,
              key = i )

          else:
            _context = context

          hints.extend( v._lint(
            context = _context,
            logger = logger ) )

    elif is_mapping( self._p_src ):
      # local variables for items in list or dictionary
      # NOTE: parent of items is the current value, parent of current will be
      # parent of the item parent

      for k, v in self._p_src.items():

        if not is_valued(v):

          if isinstance( context, EvaluatedContext ):
            _context = context(
              schema = self._schema,
              parent = self,
              key = k )

          else:
            _context = context

          hints.extend( v._lint(
            context = _context,
            logger = logger ) )

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
    val : :class:`Valued <partis.schema.valued.Valued>`
      Decoded value resulting from evaluation.
      If there are no un-evaluated values, then will return a shallow copy of
      the current data.

    See Also
    --------
    :class:`Evaluated <partis.schema.eval.Evaluated>`
    """


    if self._valued:
      return copy(self)

    if is_evaluated( self._p_src ):

      val = self._p_src._eval(
        context = context,
        logger = logger )

    elif is_sequence( self._p_src ):

      # local variables for items in list or dictionary
      # NOTE: parent of items is the current value, parent of current will be
      # parent of the item parent
      val = list()

      for i, v in enumerate(self._p_src):
        if is_valued(v):
          val.append( v )

        else:
          if isinstance( context, EvaluatedContext ):
            _context = context(
              schema = self._schema,
              parent = val,
              key = i )

          else:
            _context = context

          val.append( v._eval(
            context = _context,
            logger = logger ) )

    elif is_mapping( self._p_src ):
      # local variables for items in list or dictionary
      # NOTE: parent of items is the current value, parent of current will be
      # parent of the item parent
      val = adict()

      for k, v in self._p_src.items():

        if is_valued(v):
          val[k] = v

        else:
          if isinstance( context, EvaluatedContext ):
            _context = context(
              schema = self._schema,
              parent = val,
              key = k )

          else:
            _context = context

          val[k] = v._eval(
            context = _context,
            logger = logger )


    if is_optional(val):
      return val

    if is_valued_type( val ):
      val._p_loc = self._loc

      return val

    return type(self)(
      val = val,
      schema = self._schema,
      loc = self._loc )
