# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

from copy import copy
import inspect
import os
import re

from partis.utils import (
  odict,
  fmt_base_or_type,
  fmt_iterable_or,
  fmt_attr_doc )

from partis.pyproj import (
  hash_sha256 )

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
  PathValued )

from . import (
  SchemaPrimDeclared,
  SchemaPrim )

from .str_prim import StrPrim

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathPrimDeclared( SchemaPrimDeclared ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathPrim( StrPrim ):
  """Primitive for string values

  Parameters
  ----------
  **kwargs : arguments passed to :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    valued_type = None,
    **kwargs ):

    if valued_type is None:
      valued_type = PathValued

    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      strip = True,
      max_lines = 1,
      valued_type = valued_type,
      **kwargs )

  #-----------------------------------------------------------------------------
  def validate( cls,
    val,
    loc = None,
    bias = None ):

    bias = Bias(bias)

    if isinstance(val, os.PathLike):
      val = os.fspath(val)
      bias += 1

    return super().validate(
      val = val,
      loc = loc,
      bias = bias )
