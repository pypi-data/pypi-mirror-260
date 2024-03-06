# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

import io
from abc import ABCMeta
from copy import copy
import inspect
import re

from partis.utils import (
  odict,
  fmt_base_or_type,
  fmt_iterable_or,
  StringFunction,
  indent_lines,
  _fmt_class_name,
  fmt_class_name,
  fmt_attr_doc )

from partis.pyproj import (
  hash_sha256 )

from partis.utils.special import (
  required,
  optional )

from partis.schema_meta.schema import (
  Schema,
  SchemaDeclared )

from partis.schema_meta.prim import (
  SchemaPrimMeta )

from partis.schema_meta.base import (
  SchemaError,
  SchemaNameError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaHint,
  Bias,
  Loc,
  assert_valid_name,
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
  is_evaluated_class,
  is_valued,
  is_valued_type,
  is_special,
  is_optional,
  is_required,
  any_schema )

from partis.schema.eval import (
  NotEvaluated )

from partis.schema.valued import (
  Valued )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaPrimDeclared( SchemaDeclared, metaclass = SchemaPrimMeta ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaPrim( Schema, metaclass = SchemaPrimMeta ):
  """Base class for all schema primitives

  Parameters
  ----------
  name : str
    Class name of type
  bases : list[type]
    Base classes of type
  namespace : dict[str, object]
  restricted : None | list[object]
    Restricts the possible decoded values to those given in the list, in addition to being
    the correct type.
    If given, items will be validated against the primitve schema.
  evaluated : None | :class:`Evaluated <partis.schema.eval.Evaluated>`
    Class capable to transforming raw source data (such as Python expressions)
    into the appropriate data type.
    The `val` is checked using `evaluated.check`.
    If it cannot be interpreted as an expression, the value is validated as is.
    If not specified, then source data will not be considered as an expression.
  default_val : None | :class:`OptionalType <partis.utils.special.OptionalType>` | :class:`RequiredType <partis.utils.special.RequiredType>` | :class:`DerivedType <partis.utils.special.DerivedType>` | object
    The default `val` (value) of this schema in the case of missing source data.
    A default of `None` (or `OptionalType`) means the value is optional and will
    be None if source data is missing.
    A default of :class:`RequiredType <partis.utils.special.RequiredType>`
    means the value is required in the source data and
    will raise a :class:`SchemaValidationError <partis.schema_meta.base.SchemaValidationError>`
    if value is missing.
    A default of :class:`DerivedType <partis.utils.special.DerivedType>`
    will attempt to construct a default value from the
    default values of the `struct` items, but will raise a
    :class:`SchemaDefinitionError <partis.schema_meta.base.SchemaDefinitionError>`
    if any items themselves have required values.
    Otherwise, items will be validated against the primitve schema.
  default_eval: :class:`RequiredType <partis.utils.special.RequiredType>` | object
    The default value to use if an evaluated expression results in `None`.
    The purpose of this value is that the `default_val` itself may be an expression
    that could return None, which would reference back to the `default_val` causing
    an un-resolvable loop.
    If that would occur, then this value will be used as the result of the expression
    instead of the `default_val` expression.
    If `default_val` is anything other than an expression, specifying this will raise
    an error to ensure a single source of truth for the resulting value.
  init_val : None | object
    The initial value that is used when creating an editable template for the value.
    This differs from `default_val` in that this value is *not* used to fill in
    any missing source data.
    If `None`, `default_val` will be used, or a value will be derived
    from the schema to produce an initial value that will pass validation.
    However, `init_val` may specified independently from `default_val`.
  preset_vals : None | list[ :class: `PresetValue <partis.schema_meta.base.PresetValue>`]
  doc : None | str
    Description or interpretation of the decoded value.
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    declared = None,
    restricted = None,
    evaluated = None,
    default_val = required,
    default_eval = required,
    init_val = None,
    preset_vals = None,
    schema_deps = None,
    valued_type = None,
    loc = None ):

    if declared is not None:
      # defines the given schema declared

      if not isinstance( declared, SchemaPrimDeclared ):
        raise SchemaDefinitionError(
          f"`declared` must be subclass of SchemaPrimDeclared: {fmt_base_or_type(declared)}",
          loc = loc )

    if restricted is not None:
      if not is_sequence( restricted ):
        raise SchemaDefinitionError(
          f"`restricted` must be None or a list: {fmt_base_or_type(restricted)}",
          loc = loc )

      if len(restricted) == 0:
        raise SchemaDefinitionError(
          f"`restricted` must be None or have at least one value",
          loc = loc )

      for i, val in enumerate(restricted):
        if is_valued_type( val ) or is_evaluated( val ):
          restricted[i] = val._encode

    namespace = dict(**namespace,
      _p_restricted = restricted,
      _p_declared = declared )

    cls = super().__new__(
      mcls,
      name,
      bases,
      namespace,
      evaluated = evaluated,
      default_val = default_val,
      default_eval = default_eval,
      init_val = init_val,
      preset_vals = preset_vals,
      schema_deps = schema_deps,
      valued_type = valued_type,
      loc = loc )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    declared = None,
    restricted = None,
    evaluated = None,
    default_val = required,
    default_eval = required,
    init_val = None,
    preset_vals = None,
    schema_deps = None,
    valued_type = None,
    loc = None,
    doc = None ):

    # must initialize class before additional validation since it uses the derived
    # class's methods to perform the validation
    super().__init__( name, bases, namespace )

    if cls._p_declared is not None:
      cls._p_declared.schema_declared( cls )

  #-----------------------------------------------------------------------------
  @property
  def default_val( cls ):
    """ :class:`OptionalType <partis.utils.special.OptionalType>` | :class:`RequiredType <partis.utils.special.RequiredType>` | object : The
    default decoded value of this schema in the case of missing source data.
    A default of `None` means the value is optional, and will not have a value
    if source data is missing.
    A default of `required` means the value is required in the source data
    """
    val = cls._p_default_val

    if not (
      is_optional( val )
      or is_required( val ) ):

      val = cls.encode( val, cls.loc )

    return val

  #-----------------------------------------------------------------------------
  @property
  def default_eval( cls ):
    """:class:`RequiredType <partis.utils.special.RequiredType>` | object : The
    default value to use if an evaluated expression results in `None`.
    """
    val = cls._p_default_eval

    if not is_required( val ):

      val = cls.encode( val, cls.loc )

    return val

  #-----------------------------------------------------------------------------
  @property
  def init_val( cls ):
    """object : An initial value to use to create a template value that will
    pass validation
    """
    val = cls._p_init_val

    if val is not None:
      return cls.encode( cls._p_init_val, cls.loc )

    # default_eval checked first, only not-required if `default_val` is an expression

    val = cls.default_eval

    if not is_required( val ):
      return cls.encode( val, cls.loc )

    val = cls.default_val

    if not (
      is_optional( val )
      or is_required( val ) ):

      # only use `default_val` if an actual value, and not an expression

      return cls.encode( val, cls.loc )

    if cls.restricted is not None:
      return cls.encode( cls.restricted[0], cls.loc )

    # use whatever value would be created by the valued object
    if issubclass( cls.valued_type, Valued ):
      return cls.valued_type()._encode

    return None

  #-----------------------------------------------------------------------------
  @property
  def evaluated( cls ):
    """None | :class:`Evaluated <partis.schema.eval.Evaluated>` : Class capable
    to transforming raw source data (such as Python expressions)
    into the appropriate data type.
    """
    return cls._p_evaluated

  #-----------------------------------------------------------------------------
  @property
  def restricted( cls ):
    """None | list[object] : The possible decoded values to those given in the list,
    in addition to being the correct type.
    """
    return cls._p_restricted

  #-----------------------------------------------------------------------------
  def validate( cls,
    val,
    loc = None,
    bias = None ):
    """Validates value against schema definition

    Parameters
    ----------
    val : object
    loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
    bias : None | Bias

    Returns
    -------
    val : object
    bias : Bias

    Raises
    ------
    SchemaValidationError
      If the value is not valid
    """

    bias = Bias(bias)

    if cls.restricted is not None:
      try:
        bias += len(val)
      except TypeError:
        bias += 1

      if val not in cls.restricted:
        raise SchemaValidationError(
          f"Must be any of {fmt_iterable_or(cls.restricted)}: {fmt_base_or_type(val)}",
          loc = loc )

    return val, bias

  #-----------------------------------------------------------------------------
  def _encode( cls,
    val = None,
    loc = None,
    no_defaults = None ):

    if is_valued_type( val ) or is_evaluated( val ):
      if loc is None:
        loc = val._loc

      # NOTE: must still validate value since there are no gaurantees about
      # the original schema
      if not ( val._schema is cls and is_valued(val) ):
        val = val._encode

    if loc is None:
      loc = Loc(path = [cls.__name__])

    if val is None:
      val = cls.default_val

      if is_required( val ):
        raise SchemaValidationError(
          f"Value is required",
          loc = loc,
          hints = cls.doc )

      else:
        return None, loc, False

    # elif no_defaults and val == cls.default_val:
    #   return None, loc, False

    if cls.evaluated.check(val):
      # the value would still need to be evaluated, so cannot further validate
      return val, loc, False

    return val, loc, True

  #-----------------------------------------------------------------------------
  def _decode( cls,
    val = None,
    loc = None,
    bias = None ):
    """Validates value against schema definition

    Parameters
    ----------
    val : object
    loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
    bias : None | Bias

    Returns
    -------
    val : object
    loc : :class:`Loc <partis.schema_meta.base.Loc>`
    validate : bool
    bias : Bias

    Raises
    ------
    SchemaValidationError
      If the value is not valid
    """

    bias = Bias(bias)

    if is_valued_type( val ) or is_evaluated( val ):
      if loc is None:
        loc = val._loc

      val = val._encode

    if loc is None:
      loc = Loc(path = [cls.__name__])

    if val is None:
      bias = Bias(const = True)
      val = cls.default_val

      if is_required( val ):
        raise SchemaValidationError(
          f"Value is required",
          loc = loc,
          hints = cls.doc )

      elif is_optional( val ):
        return None, loc, False, bias

    if cls.evaluated.check(val):
      # value will need to be evaluated, so cannot further validate
      return (
        cls.valued_type(
          val = cls.evaluated(
            schema = cls,
            src = val,
            loc = loc ),
          bias = bias ),
        loc,
        False,
        bias )

    return val, loc, True, bias

  #-----------------------------------------------------------------------------
  def encode( cls,
    val = None,
    loc = None,
    no_defaults = None ):
    """Encodes value to basic Python types, performing validation

    Parameters
    ----------
    val : None | object
      Source data used to initialize values
    loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
      Location information of source data (E.G. file, line/column number)
    no_defaults : bool
      Values that are equivalent to the 'default_val' are removed.

    Returns
    -------
    val : object

    Raises
    ------
    SchemaValidationError
      If the value is not valid
    """

    val, loc, validate = cls._encode(
      val = val,
      loc = loc,
      no_defaults = no_defaults )

    if not validate:
      return val

    return cls.validate(
      val = val,
      loc = loc )[0]

  #-----------------------------------------------------------------------------
  def decode( cls,
    val = None,
    loc = None,
    bias = None ):
    """Decodes value to schema values, performing validation

    Parameters
    ----------
    val : None | object
      Source data used to initialize values
    loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
      Location information of source data (E.G. file, line/column number)
    bias : None | Bias

    Returns
    -------
    val : :class:`Valued <partis.schema.valued.Valued>`

    Raises
    ------
    SchemaValidationError
      If the value is not valid
    """

    bias = Bias(bias)

    val, loc, validate, bias = cls._decode(
      val = val,
      loc = loc,
      bias = bias )

    if not validate:
      return val

    val, bias = cls.validate(
      val = val,
      loc = loc,
      bias = bias )

    return cls.valued_type(
      val = val,
      schema = cls,
      loc = loc,
      bias = bias )

  #-----------------------------------------------------------------------------
  def _get_doc( cls,
    noindex = False,
    depth = 0,
    max_depth = 2 ):

    lines = [
      cls.doc,
      '', '' ]

    if isinstance( cls, SchemaPrim ) and depth < max_depth:
      lines.extend( cls._get_attr_doc_lines(
        noindex = noindex,
        depth = depth,
        max_depth = max_depth ) )

    return "\n".join( lines )

  #-----------------------------------------------------------------------------
  def _get_attr_doc_lines( cls,
    noindex = False,
    depth = 0,
    max_depth = 2 ):

    lines = super()._get_attr_doc_lines(
      noindex = noindex,
      depth = depth,
      max_depth = max_depth )

    lines.extend([
      fmt_attr_doc(
        name = attr,
        typename = type( getattr( cls, attr ) ),
        val = getattr( cls, attr ),
        prefix = 'schema',
        noindex = noindex )
      for attr in [
        'default_val',
        'default_eval',
        'init_val',
        'restricted' ] ])

    lines.append( fmt_attr_doc(
      name = 'evaluated',
      typename = cls.evaluated,
      prefix = 'schema',
      noindex = noindex ) )

    return lines

  #-----------------------------------------------------------------------------
  def _schema_hash_node( cls ):
    lines = super()._schema_hash_node()

    for attr in [
      # TODO: should these be included in the hash? Default values used while
      # decoding seem like non-essential information for validating what was
      # originally encoded.
      # 'default_val',
      # 'default_eval',
      # 'init_val',
      'restricted',
      'evaluated' ]:

      val = getattr( cls, attr )
      hash = None

      if hasattr( val, 'schema_hash_node' ):
        hash = val.schema_hash_node
      else:
        hash = hash_sha256( str(val).encode('utf-8') )[0]

      lines.append( f'{attr}, {hash}' )

    return lines

  #-----------------------------------------------------------------------------
  def _schema_resolved( cls ):

    super()._schema_resolved()

    if cls.restricted:
      for i, val in enumerate( cls.restricted ):
        try:

          cls.decode( val )

        except Exception as e:
          raise SchemaDefinitionError(
            f"Schema `restricted[{i}]` not valid: {val}",
            loc = cls.loc,
            hints = SchemaHint.cast( e ) ) from e


  #-----------------------------------------------------------------------------
  def __call__( cls,
    *args,
    **kwargs ):

    if len(args) == 0:
      val = None
      loc = None
    else:
      if len(args) == 1:
        val = args[0]
        loc = None
      elif len(args) == 2:
        val, loc = args
      else:
        raise ValueError(
          f"positional arguments must be at most `(val, loc)`."
          " All keyword arguments are interpreted as items of `val`")

    if kwargs:
      if val:
        val = {**val, **kwargs}
      else:
        val = kwargs

    return cls.decode(
      val = val,
      loc = loc )
