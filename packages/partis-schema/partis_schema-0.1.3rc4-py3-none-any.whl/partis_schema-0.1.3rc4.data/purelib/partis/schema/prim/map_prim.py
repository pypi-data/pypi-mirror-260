# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

from copy import copy
import inspect
import re

from partis.utils import (
  odict,
  fmt_base_or_type,
  fmt_iterable_or,
  fmt_attr_doc,
  _fmt_class_name )

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
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_schema_prim,
  is_schema_declared,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  is_evaluated,
  is_valued,
  is_optional,
  is_required )

from partis.schema_meta.schema import (
  fmt_schema_typename )

from partis.schema.valued import (
  MapValued )

from . import (
  SchemaPrimDeclared,
  SchemaPrim )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MapPrimDeclared( SchemaPrimDeclared ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MapPrim( SchemaPrim ):
  """Primitive for dictionary/mapping values

  Parameters
  ----------
  item : :class:`SchemaPrim <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
    The schema for the value of each item in the mapping
  **kwargs : arguments passed to :class:`SchemaPrim <partis.schema.prim.SchemaPrim>`
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    item,
    min_len = None,
    **kwargs ):

    loc = kwargs.get('loc', None)

    if not is_schema( item ):
      raise SchemaDefinitionError(
        f"`MapPrim` item must be instance of `SchemaPrim` or `Schema`: {item}",
        loc = loc )

    if min_len is not None:
      min_len = int(min_len)

      if min_len <= 0:
        raise SchemaDefinitionError(
          f"`SeqPrim` minimum length must be > 0: {min_len}",
          loc = loc )

    namespace['_p_item'] = item
    namespace['_p_min_len'] = min_len

    if not item.schema_defined:
      kwargs['schema_deps'] = kwargs.get('schema_deps', list()) + [item]

    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      valued_type = MapValued,
      **kwargs )

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    item,
    min_len = None,
    **kwargs ):


    super().__init__(
      name = name,
      bases = bases,
      namespace = namespace,
      **kwargs )

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
        'min_len' ] ])

    lines.append(
      fmt_attr_doc(
        name = 'item',
        typename = fmt_schema_typename( cls.item ),
        val = ...,
        prefix = 'schema',
        noindex = noindex,
        doc = cls.item._get_doc(
          # always specify noindex since the item schema already documented
          noindex = True,
          depth = depth + 1,
          max_depth = max_depth ) ) )

    return lines

  #-----------------------------------------------------------------------------
  def _schema_hash_children( cls ):
    return [ cls.item, ]

  #-----------------------------------------------------------------------------
  @property
  def hints( cls ):
    hints = super().hints

    hints.append( f"min_len: {cls.min_len}" )

    if is_schema_declared(cls.item):
      hints.append( SchemaHint(
        f"item: {cls.item.tag}") )
    else:
      hints.append( SchemaHint(
        f"item:",
        hints = cls.item.schema.hints ) )

    return hints

  #-----------------------------------------------------------------------------
  @property
  def item( cls ):
    return cls._p_item

  #-----------------------------------------------------------------------------
  @property
  def min_len( cls ):
    return cls._p_min_len

  #-----------------------------------------------------------------------------
  def validate( cls,
    val,
    loc = None,
    bias = None ):

    bias = Bias(bias)

    if not is_mapping( val ):
      raise SchemaValidationError(
        f"Must be a `dict`: {type(val).__name__}",
        loc = loc )

    bias += 1

    if cls.min_len:
      bias += 1

      if len(val) < cls.min_len:
        raise SchemaValidationError(
          f"Must have length >= {cls.min_len}: {len(val)}",
          loc = loc )

    return super().validate(
      val = val,
      loc = loc,
      bias = bias )

  #-----------------------------------------------------------------------------
  def encode( cls,
    val = None,
    loc = None,
    no_defaults = None ):

    val, loc, validate = cls._encode(
      val = val,
      loc = loc,
      no_defaults = no_defaults )

    if not validate:
      return val

    val = cls.validate(
      val = val,
      loc = loc )[0]

    item_schema = cls.item.schema.schema

    val = odict([
      ( k, item_schema.encode(
        val = v,
        no_defaults = no_defaults ) )
      for k, v in val.items() ])

    if is_schema_struct( cls.item ):
      # don't need to store tag key since schema is not ambiguous
      tag_key = cls.item.tag_key

      for v in val.values():
        if is_mapping( v ):
          v.pop( tag_key )

    # if no_defaults:
    #   dv = item_schema.default_val
    #
    #   if is_mapping(dv) and is_schema_struct( cls.item ):
    #     dv.pop(tag_key)
    #
    #   equiv = { k: (dv if v is None else v) for k,v in val.items() }
    #
    #   if equiv == cls.default_val:
    #     val = None

    return val

  #-----------------------------------------------------------------------------
  def decode( cls,
    val = None,
    loc = None,
    bias = None ):

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

    # create new object of the same type as the value (a subclass of dict)
    decode_val = odict()

    for k,v in val.items():
      _loc = loc( val, k )

      with schema_errors(
        msg = f"Dict item could not be decoded",
        data = f"key = '{k}'",
        loc = loc( val, k ),
        hints = [val],
        schema = cls,
        cls = SchemaValidationError ):

        decode_val[k] = cls.item.schema.decode(
          val = v,
          loc = _loc )

      # try:
      #   decode_val[k] = cls.item.schema.decode(
      #     val = v,
      #     loc = _loc )
      #
      # except SchemaError as e:
      #   raise SchemaValidationError(
      #     f"Dict item could not be decoded: {k}",
      #     loc = _loc,
      #     hints = SchemaHint.cast( e ) ) from e

    return cls.valued_type(
      val = decode_val,
      schema = cls,
      loc = loc )
