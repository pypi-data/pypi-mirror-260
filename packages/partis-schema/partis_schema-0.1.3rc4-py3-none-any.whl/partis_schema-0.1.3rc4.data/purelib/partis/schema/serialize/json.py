# -*- coding: UTF-8 -*-
from collections import OrderedDict as odict
from copy import copy
from abc import ABCMeta
import itertools
import re
import uuid

from abc import ABCMeta

import logging
log = logging.getLogger(__name__)

import ruamel.yaml
import json

from ruamel.yaml.comments import (
  CommentedMap,
  CommentedOrderedMap,
  CommentedKeySeq,
  CommentedSeq )

from ruamel.yaml.scalarstring import LiteralScalarString

from partis.schema_meta.base import (
  Loc,
  SchemaHint,
  SchemaError,
  SchemaParseError,
  SchemaDetectionError,
  is_valued_type,
  is_evaluated,
  is_string,
  is_mapping,
  is_sequence )

from partis.schema.plugin import (
  schema_plugins )

from .utils import (
  as_load,
  as_dump )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dump_prep( val ):
  """Prepares value to be dumped, converting to standard json datastructures
  """

  if is_valued_type( val ) or is_evaluated( val ):
    val = val._encode

  if is_string( val ):
    val = re.sub(r"\r\n", "\n", val)
    val = re.sub(r"[\r\v\f]", "\n", val)
    val = re.sub(r"[\b\a]+", "", val)

  if is_mapping( val ):
    _val = dict()

    for k, v in val.items():
      _val[k] = dump_prep( v )

  elif is_sequence( val ):
    _val = list()

    for v in val:
      _val.append( dump_prep( v ) )

  else:
    _val = val

  return _val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def loads(
  src,
  schema = None,
  loc = None,
  detect_schema = False ):
  """
  Parse a JSON document in a stream
  and produce the corresponding Python object.

  Parameters
  ----------
  src : str
  schema : :class:`Schema <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)

  Returns
  -------
  val : object | :class:`Schema <partis.schema.valued.Valued>`
  """

  if loc is None:
    loc = Loc()

  if isinstance( loc, str ):
    loc = Loc( filename = loc )

  try:
    # NOTE: Since JSON is a subset of YAML, using the YAML parser should work
    # here instead of json.loads, and will include all the correct data for tracking
    # source of values (e.g. line/col numbers)
    val = ruamel.yaml.round_trip_load( src )

  except BaseException as e:
    raise SchemaParseError(
      f"Document failed parsing",
      loc = loc,
      hints = SchemaHint.cast( e ) ) from e

  schema_hash = ''

  if is_mapping( val ) and '__schema_hash__' in val:
    schema_hash = val.pop('__schema_hash__')

  if detect_schema:

    if schema_hash:
      _schemas = schema_plugins.get_by_hash( schema_hash )

      if len(_schemas) > 0:
        schema = _schemas[0]

    if schema is None:
      raise SchemaDetectionError(
        f'Schema could not be detected' )

  if schema is None:
    return val

  loc = loc(val)

  return schema.schema.decode(
    val = val,
    loc = loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dumps( val ):
  """Serializes a suitable Python object into a JSON document string

  Parameters
  ----------
  val : object | :class:`Schema <partis.schema.valued.Valued>`

  Returns
  -------
  src : str
  """

  val = dump_prep( val )

  return json.dumps(
    val,
    skipkeys = False,
    sort_keys = False,
    ensure_ascii = True,
    check_circular = True,
    indent = 2 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
load = as_load( loads )
dump = as_dump( dumps )
