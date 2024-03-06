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
  StrValued )

from . import (
  SchemaPrimDeclared,
  SchemaPrim )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrPrimDeclared( SchemaPrimDeclared ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StrPrim( SchemaPrim ):
  """Primitive for string values

  Parameters
  ----------
  char_case : NoneType | str
    Cased characters are converted to given case

    - None (default) : Cased characters are not altered

    - 'lower' : Cased characters are converted to their lower-case equivalent

    - 'upper' : Cased characters are converted to their upper-case equivalent
  strip : NoneType | bool
    Strips leading and trailing white-space if ``True``.
  pattern : NoneType | str
    Validates a string using a regular expression (Python syntax)

    .. note::

      The pattern is only matched to non-empty strings.
      See the `nonempty` argument to only allow string that have at least one character.
  nonempty : NoneType | bool
    Only non-empty strings are valid if ``True``.
    If the value is optional, the no-value or a value of ``None`` is still considered valid.
  max_lines : NoneType | int
    Maximum number of lines
  max_cols : NoneType | int
    Maximum number of columns

  **kwargs : arguments passed to :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    char_case = None,
    strip = None,
    pattern = None,
    nonempty = None,
    max_lines = None,
    max_cols = None,
    valued_type = None,
    **kwargs ):

    loc = kwargs.get('loc', None)

    lines = list()

    if char_case not in [ None, 'lower', 'upper' ]:
      raise SchemaDefinitionError(
        f"`char_case` must be None, lower, or upper: {char_case}",
        loc = loc )

    strip = bool(strip)

    if pattern is not None:
      try:
        pattern = re.compile( pattern )

      except BaseException as e:
        raise SchemaDefinitionError(
          f"`pattern` must be a valid Python regular expression: {pattern}",
          loc = loc ) from e

    nonempty = bool(nonempty)

    if max_lines is not None:
      max_lines = int(max_lines)

      if max_lines < 1:
        raise SchemaDefinitionError(
          f"`max_lines` must be >= 1: {max_lines}",
          loc = loc )

    if max_cols is not None:
      max_cols = int(max_cols)

      if max_cols < 1:
        raise SchemaDefinitionError(
          f"`max_cols` must be >= 1: {max_cols}",
          loc = loc )

    if valued_type is None:
      valued_type = StrValued

    namespace = { **namespace, **dict(
      _p_char_case = char_case,
      _p_strip = strip,
      _p_pattern = pattern,
      _p_nonempty = nonempty,
      _p_max_lines = max_lines,
      _p_max_cols = max_cols )}

    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      valued_type = valued_type,
      **kwargs )

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    char_case = None,
    strip = None,
    pattern = None,
    nonempty = None,
    max_lines = None,
    max_cols = None,
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
        'char_case',
        'strip',
        'pattern',
        'nonempty',
        'max_lines',
        'max_cols' ] ])

    return lines

  #-----------------------------------------------------------------------------
  def _schema_hash_node( cls ):
    lines = super()._schema_hash_node()

    for attr in [
      'char_case',
      'strip',
      'pattern',
      'nonempty',
      'max_lines',
      'max_cols' ]:

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
  def char_case( cls ):
    return cls._p_char_case

  #-----------------------------------------------------------------------------
  @property
  def pattern( cls ):
    return cls._p_pattern

  #-----------------------------------------------------------------------------
  @property
  def max_lines( cls ):
    return cls._p_max_lines

  #-----------------------------------------------------------------------------
  @property
  def max_cols( cls ):
    return cls._p_max_cols

  #-----------------------------------------------------------------------------
  @property
  def nonempty( cls ):
    return cls._p_nonempty

  #-----------------------------------------------------------------------------
  @property
  def strip( cls ):
    return cls._p_strip

  #-----------------------------------------------------------------------------
  def validate( cls,
    val,
    loc = None,
    bias = None ):

    bias = Bias(bias)

    #...........................................................................
    if not is_string( val ):
      raise SchemaValidationError(
        f"Must be a `str`: {type(val).__name__}",
        loc = loc )

    bias += 1
    val = str(val)

    #...........................................................................
    if cls.char_case is not None:
      if cls.char_case == 'lower':
        val = str.lower( val )

      elif cls.char_case == 'upper':
        val = str.upper( val )

      else:
        assert False

    #...........................................................................
    if cls.strip:
      val = val.strip()

    #...........................................................................
    if cls.pattern is not None:
      bias += len(val)

      if len(val) > 0 and cls.pattern.fullmatch( val ) is None:
        raise SchemaValidationError(
          f"Does not match pattern `{cls.pattern.pattern}`:",
          data = val,
          loc = loc )

    if cls.nonempty:
      bias += 1

      if len(val) == 0:
        raise SchemaValidationError(
          f"Must be non-empty string",
          loc = loc )

    #...........................................................................
    if cls.max_lines is not None or cls.max_cols is not None:
      lines = val.splitlines()

    #...........................................................................
    if cls.max_lines is not None:
      bias += 1

      if len(lines) > cls.max_lines:
        raise SchemaValidationError(
          f"Maximum lines exceeded {cls.max_lines}: {len(lines)}",
          loc = loc )

    #...........................................................................
    if cls.max_cols is not None:
      cols = list( map(len, lines) )
      bias += len(cols)

      if len(cols) > 0:
        max_cols = max(cols)

        if max_cols > cls.max_cols:
          idx = cols.index( max_cols )

          raise SchemaValidationError(
            f"Maximum columns exceeded {cls.max_cols}: {max_cols} (line {idx})",
            loc = loc )

    return super().validate(
      val = val,
      loc = loc,
      bias = bias )
