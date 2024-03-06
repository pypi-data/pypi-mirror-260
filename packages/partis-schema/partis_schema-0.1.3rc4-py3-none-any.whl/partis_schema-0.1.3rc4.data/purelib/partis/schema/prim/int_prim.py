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
  IntValued )

from . import (
  SchemaPrimDeclared,
  SchemaPrim )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntPrimDeclared( SchemaPrimDeclared ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class IntPrim( SchemaPrim ):
  """Primitive for integer values

  Parameters
  ----------
  **kwargs : arguments passed to :class:`SchemaPrim <partis.schema.prim.SchemaPrim>`
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    min = None,
    max = None,
    **kwargs ):

    loc = kwargs.get('loc', None)

    if min is not None:
      min = int(min)

    if max is not None:
      max = int(max)

      if not ( min is None or max >= min ):
        raise SchemaDefinitionError(
          f"`IntPrim` max must be greater than or equal to min ({min}): {max}",
          loc = loc )

    namespace = { **namespace, **dict(
      _p_min = min,
      _p_max = max )}


    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      valued_type = IntValued,
      **kwargs )

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    min = None,
    max = None,
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
        'min',
        'max' ] ])

    return lines

  #-----------------------------------------------------------------------------
  def _schema_hash_node( cls ):
    lines = super()._schema_hash_node()

    for attr in [
      'min',
      'max' ]:

      val = getattr( cls, attr )
      hash = None

      if hasattr( val, 'schema_hash' ):
        hash = val.schema_hash
      else:
        hash = hash_sha256( str(val).encode('utf-8') )[0]

      lines.append( f'{attr}, {hash}' )

    return lines

  #-----------------------------------------------------------------------------
  @property
  def hints( cls ):
    hints = super().hints

    if cls.min is not None:
      hints.append( SchemaHint(
        "min: int",
        hints = f"value >= {cls.min}" ) )

    if cls.max is not None:
      hints.append( SchemaHint(
        "max: int",
        hints = f"value <= {cls.max}" ) )

    return hints

  #-----------------------------------------------------------------------------
  @property
  def min( cls ):
    return cls._p_min

  #-----------------------------------------------------------------------------
  @property
  def max( cls ):
    return cls._p_max

  #-----------------------------------------------------------------------------
  def validate( cls,
    val,
    loc = None,
    bias = None ):

    bias = Bias(bias)

    if not is_numeric( val ):
      raise SchemaValidationError(
        f"Must be a `numeric`: {fmt_base_or_type(val)}",
        loc = loc )

    bias += 1
    _val = int( val.real )

    if _val != val:
      raise SchemaValidationError(
        f"Casting to integer does not preserve value: {fmt_base_or_type(val)}",
        loc = loc )

    val = _val

    if cls.min is not None:
      bias += 1

      if val < cls.min:
        raise SchemaValidationError(
          f"Must be >= {cls.min}: {fmt_base_or_type(val)}",
          loc = loc )

    if cls.max is not None:
      bias += 1.0

      if val > cls.max:
        raise SchemaValidationError(
          f"Must be <= {cls.max}: {fmt_base_or_type(val)}",
          loc = loc )

    return super().validate(
      val = val,
      loc = loc,
      bias = bias )

  #-----------------------------------------------------------------------------
  @property
  def init_val( cls ):
    val = super().init_val

    if cls.min is not None and val < cls.min:
      val = cls.min

    if cls.max is not None and val > cls.max:
      val = cls.max

    return val
