# -*- coding: UTF-8 -*-

import io

import logging
log = logging.getLogger(__name__)

import configparser

from partis.schema_meta.base import (
  Loc,
  SchemaHint,
  SchemaError,
  is_valued_type,
  is_evaluated,
  is_string,
  is_mapping,
  is_sequence )

from .utils import (
  as_load,
  as_dump )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dump_prep( val, level = 0 ):
  """Prepares value to be dumped, converting to standard json datastructures
  """

  if is_valued_type( val ) or is_evaluated( val ):
    val = val._encode

  if is_mapping( val ):
    if level > 1:
      raise SchemaError(
        f"Config (INI) files do not support mappings with more than two levels: {val}" )

    elif level == 0:
      _val = configparser.ConfigParser()

    else:
      _val = dict()

    for k, v in val.items():
      _val[k] = dump_prep( v, level = level + 1 )

  elif is_sequence( val ):
    raise SchemaError(
      f"Config (INI) files do not support sequence values: {val}" )

  else:
    if level <= 1:
      raise SchemaError(
        f"Config (INI) files require two levels of mapping to values: {val}" )

    _val = str(val)

  return _val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def load_prep( val ):
  _val = dict(val)

  for k,v in _val.items():
    _val[k] = dict(v)

  if 'DEFAULT' in _val:
    _default_val = _val.pop('DEFAULT')

    for j, u in _val.items():
      for k, v in _default_val.items():
        if k not in u:
          u[k] = v

  return _val, _default_val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def loads(
  src,
  schema = None,
  loc = None ):
  """
  Parse a Config (INI) document in a stream
  and produce the corresponding Python object.

  Note that any 'DEFAULT' section is *not* considered a part of the schema, since
  that section provides default values for all other sections.

  Parameters
  ----------
  src : str
  schema : :class:`Schema <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)

  Returns
  -------
  val : dict | :class:`Schema <partis.schema.valued.Valued>`
  default_val : dict
    Values specified in the 'DEFAULT' section.
  """

  if loc is None:
    loc = Loc()

  if isinstance( loc, str ):
    loc = Loc( filename = loc )

  try:
    parser = configparser.ConfigParser()
    parser.read_string( src )
    val, default_val = load_prep( parser )

  except BaseException as e:
    raise SchemaError(
      f"Document failed parsing",
      loc = loc,
      hints = SchemaHint.cast( e ) ) from e

  if schema is None:
    return val, default_val

  return (
    schema.schema.decode(
      val = val,
      loc = loc ),
    default_val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dumps( val ):
  """Serializes a suitable Python object into a Config (INI) document string

  Parameters
  ----------
  val : object | :class:`Schema <partis.schema.valued.Valued>`

  Returns
  -------
  src : str
  """

  val = dump_prep( val )

  fp = io.StringIO()

  config.write(fp)

  src = fp.getvalue()

  return src

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
load = as_load( loads )
dump = as_dump( dumps )
