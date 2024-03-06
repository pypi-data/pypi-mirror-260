
import logging
log = logging.getLogger(__name__)

from partis.schema_meta.base import (
  SchemaError,
  SchemaHint,
  assert_valid_name )

from partis.schema_meta.struct import (
  SchemaStructDeclared )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDeclared:
  """A schema-declared referencing schemas not yet defined
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    val,
    loc = None ):

    raise SchemaError(
      f"This is a schema declared for `{self.__class__.tag}`, and may not be instantiated.")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def schema_declared(
  tag,
  tag_key = None ):

  class NewSchemaDeclared( SchemaDeclared,
    tag = tag,
    tag_key = tag_key,
    metaclass = SchemaStructDeclared ):
    pass

  return NewSchemaDeclared
