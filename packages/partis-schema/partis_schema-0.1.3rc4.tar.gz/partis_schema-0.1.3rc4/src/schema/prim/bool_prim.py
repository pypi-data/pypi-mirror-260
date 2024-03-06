# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

from copy import copy
import inspect
import re

from partis.utils import (
  odict,
  fmt_base_or_type,
  fmt_iterable_or )


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
  is_valued,
  is_optional,
  is_required )

from partis.schema.valued import (
  BoolValued )

from . import (
  SchemaPrimDeclared,
  SchemaPrim )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolPrimDeclared( SchemaPrimDeclared ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolPrim( SchemaPrim ):
  """Primitive for boolean values

  Parameters
  ----------
  **kwargs : arguments passed to :class:`SchemaPrim <partis.schema.prim.SchemaPrim>`
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    **kwargs ):


    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      valued_type = BoolValued,
      **kwargs )

  #-----------------------------------------------------------------------------
  def validate( cls,
    val,
    loc = None,
    bias = None ):

    bias = Bias(bias)

    if not is_bool( val ):
      raise SchemaValidationError(
        f"Must be a `bool`: {type(val).__name__}",
        loc = loc )

    bias += 1
    val = bool(val)

    return super().validate(
      val = val,
      loc = loc,
      bias = bias )
