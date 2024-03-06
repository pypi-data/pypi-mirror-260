
from copy import copy

from collections.abc import (
  Mapping )

from partis.utils import (
  getLogger,
  max_similarity,
  adict,
  odict )

log = getLogger(__name__)

from partis.schema_meta.base import (
  schema_errors,
  SchemaError,
  SchemaNameError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaHint,
  Bias,
  Loc,
  assert_valid_name,
  is_notset,
  is_valued,
  is_evaluated,
  is_mapping,
  is_derived,
  is_optional,
  is_required,
  is_valued_type,
  is_schema_declared,
  is_schema_struct,
  any_schema )

from partis.schema_meta.struct import (
  SchemaStructProxy )

from partis.schema_meta.valued import (
  ValuedMeta )

from partis.schema import (
  EvaluatedContext )

from .valued import (
  Valued,
  get_schema_loc,
  get_init_val,
  get_src_val )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructValuedMeta( ValuedMeta, SchemaStructProxy ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def extract_val_loc( args, kwargs ):

  if len(args) == 0:
    val = None
    loc = None
    bias = None
  else:
    if len(args) == 1:
      val = args[0]
      loc = None
      bias = None

    elif len(args) == 2:
      val, loc = args
      bias = None

    elif len(args) == 3:
      val, loc, bias = args
    else:
      raise ValueError(
        f"positional arguments must be at most `(val, loc, bias)`."
        " All keyword arguments are interpreted as items of `val`")

  if kwargs:
    if val:
      val = {**val, **kwargs}
    else:
      val = kwargs

  return val, loc, bias

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class StructValued( Valued, Mapping, metaclass = StructValuedMeta ):
  """Container for fully or partially evaluated fixed mapping data.

  .. note::

    The terminology of 'struct' is used to indicate that the allowed key-value
    pairs of the value are fixed, such that keys may not be added or removed
    dynamically.
    However, key-values may be heterogenous, with a unique schema defined for
    each key, unlike the generic MapValue that specifies the same schema for
    all keys.

  Parameters
  ----------
  val : NoneType | object
    Source data used to initialize values
  loc : NoneType | :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)

  Raises
  ------
  SchemaValidationError
    If the value is not valid
  """

  #-----------------------------------------------------------------------------
  def __new__( cls,
    *args, **kwargs ):

    val, loc, bias = extract_val_loc( args, kwargs )
    valued = True
    bias = Bias(bias)

    if is_valued_type( val ) or is_evaluated( val ):
      if loc is None:
        loc = val._loc

      # NOTE: must still validate value since there are no gaurantees about
      # the original schema
      # val = val._encode

    if loc is None:
      loc = Loc()

    if not isinstance( loc, Loc ):
      raise SchemaValidationError(
        f"`loc` must be instance of `Loc`: {type(loc)}")

    if is_optional(val):
      val = cls.schema.default_val
      bias = Bias(bias, const = True)

      if is_required( val ):
        raise SchemaValidationError(
          f"Value is required",
          loc = loc,
          hints = cls.schema.hints )

      elif is_optional( val ):
        return None

    if cls.schema.evaluated.check( val ):
      valued = False

      val = cls.schema.evaluated(
        schema = cls.schema,
        src = val,
        loc = loc )

    self = super().__new__( cls )

    self._p_dict = odict()

    self._p_bias = bias
    self._p_bias_dict = {
      k: Bias(0.0, const = bias._const)
      for k in cls.schema.struct.keys() }

    self._p_loc = loc
    self._p_valued = valued
    self._p_src = val

    return self

  #-----------------------------------------------------------------------------
  def __init__( self,
    *args, **kwargs ):

    val, loc, bias = extract_val_loc( args, kwargs )

    # these are set by the __new__ method
    if not self._valued:
      return

    val = self._src
    loc = self._loc

    tag_key = self._schema.tag_key
    tag = self._schema.tag

    self._p_dict[tag_key] = tag

    loc = self._loc

    if not is_mapping( val ):
      if self._schema.struct_proxy:
        # uses source data for primary struct key value with remaining defaults

        _val = dict()
        _val[ self._schema.struct_proxy ] = val
        val = _val

      else:
        raise SchemaValidationError(
          f"`val` must be a mapping: {val}",
          loc = loc )

    all_keys = set(self._schema.struct.keys()) | set(val.keys())

    _locs = {
      k : loc( val, k )
      for k in all_keys }

    if tag_key in val:
      _tag = val[tag_key]

      if _tag != tag:
        log.warning(SchemaHint(
          msg = f"Expected value '{tag}' for tag key '{tag_key}'",
          data = f"'{tag_key}': '{_tag}'",
          format = 'auto',
          loc = Loc(**{
            **loc( val, tag_key ).to_dict(),
            'owner': f"{self._schema.__module__}.{self._schema.__name__}"}) ))

    _keys = list(self._schema.struct.keys())

    num_known_keys = 0
    unknown_keys = list()

    for k in val.keys():

      if k not in _keys and k != tag_key:
        # issue warnings for unexpected keys

        _k, _similarity = max_similarity(k, _keys)
        unknown_keys.append((k, _k, _similarity))

        from partis.schema.serialize.yaml import dumps
        try:
          # reduce the bias when data is thrown away
          # estimated as 1/2 of the serialized text string
          self._p_bias += -0.5*( len(k) + len(dumps(val[k])) )
        except:
          pass


    for k, _schema in self._schema.struct.items():
      _schema = _schema.schema

      # decode data according to schema
      _val = None
      _loc = None

      if k in val:
        num_known_keys += 1
        _val = val[k]

        if is_valued_type(_val):
          _loc = _val._loc

      if _loc is None:
        _loc = _locs[k]

      with schema_errors(
        msg = f"Struct item could not be decoded",
        data = f"key = '{k}'",
        loc = _loc,
        cls = SchemaValidationError ):

        _val = _schema.decode(
          val = _val,
          loc = _loc )

      if _val is not None:
        self._p_bias_dict[k] += _val._bias

        if not is_valued(_val):
          self._p_valued = False

      self._p_bias_dict[k] += len(k)

      self._p_dict[k] = _val

    if len(unknown_keys) > 0:
      unknown_hint = SchemaHint(
        msg = f"Keys not in schema",
        loc = Loc(**{
          **loc.to_dict(),
          'owner': f"{self._schema.__module__}.{self._schema.__name__}"}),
        hints = [ SchemaHint(
          msg = f"Key",
          data = f"'{k}'",
          level = 'warning',
          format = 'auto',
          loc = _locs[k],
          hints = [SchemaHint(
            f"Guess ({_similarity:.0%})",
            data = f"'{_k}'")] )

          for k, _k, _similarity in unknown_keys ] )

      if len(self._schema.struct) > 0 and num_known_keys == 0:
        raise SchemaValidationError(
          f"Mapping contains only unknown keys",
          loc = loc,
          hints = [unknown_hint] )

      else:
        log.warning(unknown_hint)

  #-----------------------------------------------------------------------------
  @property
  def _valued( self ):
    """bool : False if any item is not fully evaluated. True otherwise.
    """
    return self._p_valued

  #-----------------------------------------------------------------------------
  @property
  def _src( self ):
    return self._p_src

  #-----------------------------------------------------------------------------
  @property
  def _bias( self ):
    return Bias(float(self._p_bias) + sum(float(s) for s in self._p_bias_dict.values()))

  #-----------------------------------------------------------------------------
  @property
  def _loc( self ):
    """:class:`Loc <partis.schema_meta.base.Loc>` : Location information of source
    data (E.G. file, line/column number)
    """
    return self._p_loc

  #-----------------------------------------------------------------------------
  @property
  def _schema( self ):
    """:class:`SchemaStruct <partis.schema.struct.SchemaStruct>` :  Schema class
    of this instance
    """
    return type(self).schema

  #-----------------------------------------------------------------------------
  @property
  def _encode( self ):
    """dict : Plain-data values of items.
    """

    if is_evaluated( self._src ):
      return self._src._encode

    return self._schema.encode(
      val = self,
      loc = self._loc )

  #-----------------------------------------------------------------------------
  def __str__( self ):
    # return self._p_dict.__str__( )
    return f"{type(self).__name__}({list(self._p_dict.items())})"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    # return self._p_dict.__repr__( )
    return f"{type(self).__name__}({list(self._p_dict.items())})"


  #-----------------------------------------------------------------------------
  def __len__( self ):
    return len(self._p_dict)

  #-----------------------------------------------------------------------------
  def __iter__( self ):
    return iter(self._p_dict)

  #-----------------------------------------------------------------------------
  def keys( self ):
    return self._p_dict.keys()

  #-----------------------------------------------------------------------------
  def values( self ):
    return self._p_dict.values()

  #-----------------------------------------------------------------------------
  def items( self ):
    return self._p_dict.items()

  #-----------------------------------------------------------------------------
  def get( self, key, default = None ):
    return self._p_dict.get( key, default )


  # #-----------------------------------------------------------------------------
  # def __getattribute__( self, name ):
  #
  #   try:
  #     return super().__getattribute__(name)
  #
  #   except AttributeError as e:
  #
  #     if name in self._p_dict:
  #       return self._p_dict[name]
  #
  #     raise AttributeError(
  #       f"'{type(self).__name__}' object has no attribute '{name}'") from e
  #
  # #-----------------------------------------------------------------------------
  # def __setattr__( self, name, val ):
  #   if name in self._schema.struct or name == self._schema.tag_key:
  #     self[name] = val
  #     return
  #
  #   if not name.startswith('_'):
  #     raise AttributeError(f"Cannot assign new exposed attribute: {name}")
  #
  #   super().__setattr__( name, val )

  #-----------------------------------------------------------------------------
  def __iter__( self ):
    return iter(self._p_dict)

  #-----------------------------------------------------------------------------
  def __copy__( self ):

    obj = type(self)( self._p_dict, self._loc )

    return obj

  #-----------------------------------------------------------------------------
  def __getitem__( self, key ):
    if key == self._schema.tag_key:
      return self._schema.tag

    if key not in self._schema.struct:
      raise KeyError(
        f"Schema does not contain key: {key}")

    return self._p_dict[key]

  #-----------------------------------------------------------------------------
  def __setitem__( self, key, val ):

    loc = None

    if is_valued_type( val ):
      loc = val._loc

    tag_key = self._schema.tag_key

    if key == tag_key:
      if val != self._schema.tag:
        raise SchemaValidationError(f"Schema value for`{tag_key}` must be `{self._schema.tag}`: {val}")

    else:

      if key not in self._schema.struct:
        raise SchemaValidationError(f"Schema does not contain key: {key}")

      with schema_errors(
        msg = f"Struct item could not be decoded",
        data = f"key = '{key}'",
        loc = loc,
        hints = [val],
        schema = self._schema,
        cls = SchemaValidationError ):

        _schema = self._schema.struct[key].schema

        if not any_schema(val, [_schema]):
          val = _schema.decode(
            val = val,
            loc = loc )

      self._p_bias_dict[key] = Bias(len(key))

      if val is not None:
        self._p_bias_dict[key] += val._bias

      self._p_dict[key] = val


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

    # must evaluate to get value

    if is_evaluated( self._p_src ):

      hints.extend( self._p_src._lint(
        context = context,
        logger = logger ) )

      return hints

    # local variables for items in list or dictionary
    # NOTE: parent of items is the current value, parent of current will be
    # parent of the item parent

    for k, schema in self._schema.struct.items():
      v = self[k]

      if not is_valued(v):

        if isinstance( context, EvaluatedContext ):
          _context = context(
            schema = self._schema,
            parent = self,
            key = k )

        else:
          _context = context

        hints.extend(  v._lint(
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
    value : :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`
      Decoded value resulting from evaluation.
      If there are no un-evaluated values, then will return a shallow copy of
      the current data.

    See Also
    --------
    :class:`Evaluated <partis.schema.eval.Evaluated>`
    """

    if self._valued:
      return copy(self)

    # must evaluate to get value

    if is_evaluated( self._p_src ):

      return self._p_src._eval(
        context = context,
        logger = logger )

    # local variables for items in list or dictionary
    # NOTE: parent of items is the current value, parent of current will be
    # parent of the item parent
    val = adict()

    for k, schema in self._schema.struct.items():
      v = self[k]

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

    return type(self)( val, self._loc )

  #-----------------------------------------------------------------------------
  def on_child_key_changed( self, key, new_key ):
    pass
