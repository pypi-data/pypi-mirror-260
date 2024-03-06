import logging
log = logging.getLogger( __name__ )

from copy import copy

from partis.utils import (
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

from .valued import (
  Valued,
  get_schema_loc,
  get_init_val,
  get_src_val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SeqValued( Valued, list ):
  """Container for fully or partially evaluated sequence (list, array) data

  Parameters
  ----------
  val : list[object]
    Source data to be evaluated
  schema : :class:`Schema <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  loc : :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)
  """

  #-----------------------------------------------------------------------------
  def __new__( cls,
    val = None,
    schema = None,
    loc = None,
    bias = None ):

    self = list.__new__( cls )

    return self

  #-----------------------------------------------------------------------------
  def __init__( self,
    val = None,
    schema = None,
    loc = None,
    bias = None ):

    _val = get_init_val(
      val = val,
      schema = schema,
      default_val = list() )

    list.__init__( self, _val )

    Valued.__init__( self,
      val = val,
      schema = schema,
      loc = loc,
      bias = bias )

  #-----------------------------------------------------------------------------
  def __setitem__( self, key, val ):
    if is_evaluated( self._src ):
      # NOTE: If source is "evaluated", then encoding will not preserve set values
      raise SchemaError(f"Cannot set items on un-evaluated object: {key}")

    loc = None

    if is_valued_type( val ):
      loc = val._loc

    if self._schema is not None:
      _schema = self._schema.item.schema

      if not any_schema(val, [_schema]):
        val = self._schema.item.schema.decode(
          val = val,
          loc = loc )

    super().__setitem__( key, val )

  #-----------------------------------------------------------------------------
  def append( self, val ):

    if self._schema is not None:
      val = self._schema.item.schema.decode( val )

    super().append( val )

  #-----------------------------------------------------------------------------
  def extend( self, vals ):

    if self._schema is not None:
      _schema = self._schema.item.schema

      vals = [
        val if any_schema(val, [_schema]) else self._schema.item.schema.decode( val )
        for val in vals ]

    super().extend( vals )

  #-----------------------------------------------------------------------------
  def __str__( self ):
    if is_evaluated( self._src ):
      return str(self._src)

    return f"{type(self).__name__}({list(self)}"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  @property
  def _encode( self ):

    if is_evaluated( self._src ):
      return self._src._encode

    if self._schema is not None:
      return self._schema.encode( list(self), self._loc )

    return [ v._encode if ( is_valued_type(v) or is_evaluated(v) ) else v for v in self ]
