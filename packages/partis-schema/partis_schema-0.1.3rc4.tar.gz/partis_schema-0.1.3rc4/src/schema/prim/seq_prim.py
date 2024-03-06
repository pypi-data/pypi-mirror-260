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
  fmt_attr_doc )

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
  is_schema_declared,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  is_evaluated,
  is_valued,
  is_optional,
  is_required )

from partis.schema.valued import (
  SeqValued )

from . import (
  SchemaPrimDeclared,
  SchemaPrim )

from partis.schema_meta.schema import (
  fmt_schema_typename )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SeqPrimDeclared( SchemaPrimDeclared ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SeqPrim( SchemaPrim ):
  """Primitive for list/sequenced values

  Parameters
  ----------
  item : :class:`SchemaPrim <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
    The schema for each item in the list
  min_len : int | None
  max_len : int | None
  **kwargs :
    arguments passed to :class:`SchemaPrim <partis.schema.prim.SchemaPrim>`
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    item,
    min_len = None,
    max_len = None,
    **kwargs ):

    loc = kwargs.get('loc', None)

    if not is_schema( item ):
      raise SchemaDefinitionError(
        f"`SeqPrim` item must be instance of `SchemaPrim` or `Schema`: {item}",
        loc = loc )

    if min_len is None:
      min_len = 0

    min_len = int(min_len)

    if min_len < 0:
      raise SchemaDefinitionError(
        f"`SeqPrim` minimum length must be >= 0: {min_len}",
        loc = loc )

    if max_len is not None:
      max_len = int(max_len)

      if max_len < min_len:
        raise SchemaDefinitionError(
          f"`SeqPrim` maximum length must be >= {min_len}: {max_len}",
          loc = loc )

    namespace['_p_item'] = item
    namespace['_p_min_len'] = min_len
    namespace['_p_max_len'] = max_len

    if not item.schema_defined:
      kwargs['schema_deps'] = kwargs.get('schema_deps', list()) + [item]

    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      valued_type = SeqValued,
      **kwargs )

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    item,
    min_len = None,
    max_len = None,
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
        'min_len',
        'max_len' ] ])


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
    hints.append( f"max_len: {cls.max_len}" )

    if is_schema_declared( cls.item ):
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
  @property
  def max_len( cls ):
    return cls._p_max_len

  #-----------------------------------------------------------------------------
  def validate( cls,
    val,
    loc = None,
    bias = None ):

    bias = Bias(bias)

    if not is_sequence( val ):
      raise SchemaValidationError(
        f"Must be a `sequence`: {type(val).__name__}",
        loc = loc )

    bias += 1

    if cls.min_len:
      bias += 1

      if len(val) < cls.min_len:
        raise SchemaValidationError(
          f"Must have length >= {cls.min_len}: {len(val)}",
          loc = loc )

    if cls.max_len is not None:
      bias += 1

      if len(val) > cls.max_len:
        raise SchemaValidationError(
          f"Must have length <= {cls.max_len}: {len(val)}",
          loc = loc )

    return super().validate(
      val = val,
      loc = loc,
      bias = bias)

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

    val = [
      item_schema.encode(
        val = v,
        no_defaults = no_defaults )
      for v in val ]

    if is_schema_struct( cls.item ):
      tag_key = cls.item.tag_key

      for v in val:
        if is_mapping( v ):
          v.pop( tag_key )

    # if no_defaults:
    #   dv = item_schema.default_val
    #
    #   if is_mapping(dv) and is_schema_struct( cls.item ):
    #     dv.pop(tag_key)
    #
    #   equiv = [ dv if v is None else v for v in val ]
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

    decode_val = list()

    for i, _val in enumerate(val):
      _loc = loc( val, i )

      try:
        _val = cls.item.schema.decode(
          val = _val,
          loc = _loc )

      except SchemaError as e:
        raise SchemaValidationError(
          f"List item invalid: {i}",
          loc = _loc,
          hints = SchemaHint.cast( e ) ) from e

      decode_val.append( _val )

    return cls.valued_type(
      val = decode_val,
      schema = cls,
      loc = loc )
