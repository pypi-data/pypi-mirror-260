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
class StrValued( Valued, str ):
  """Container for fully or partially evaluated string data

  Parameters
  ----------
  val : str
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

    val = get_init_val(
      val = val,
      schema = schema,
      default_val = str() )

    self = str.__new__( cls, val )

    return self

  #-----------------------------------------------------------------------------
  def __init__( self,
    val = None,
    schema = None,
    loc = None,
    bias = None ):

    str.__init__( self )

    Valued.__init__( self,
      val = val,
      schema = schema,
      loc = loc,
      bias = bias )

  #-----------------------------------------------------------------------------
  def __str__( self ):

    if is_evaluated( self._src ):
      return str(self._src)

    return str.__str__( self )

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  @property
  def _encode( self ):
    if self._valued:
      return str(self)

    if is_evaluated( self._src ):
      return self._src._encode

    assert(False)
