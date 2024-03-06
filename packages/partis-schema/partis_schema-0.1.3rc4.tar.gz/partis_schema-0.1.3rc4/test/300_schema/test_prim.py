import pytest

from pprint import pprint

import itertools

from partis.utils.special import (
  SpecialType )

from partis.schema import (
  required,
  optional,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  SchemaStruct,
  PJCEvaluated,
  SchemaError,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_schema_prim,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  any_schema,
  BoolValued,
  IntValued,
  FloatValued,
  StrValued,
  SeqValued,
  MapValued,
  SchemaDefinitionError )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
SIMPLE_PRIMS = [
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
max_tests = -1
step_tests = 1

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_defined( val ):
  return not ( val is None or val is required or val is optional )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_val( val, default_val ):
  if val is None:
    if is_defined(default_val):
      return default_val

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def should_pass(
  val,
  is_type,
  is_item = None,
  default_val = optional,
  restricted = None,
  evaluated = None,
  min = None,
  max = None ):

  # check if value is to be evaluated
  _is_eval = evaluated is not None and evaluated.check(val)

  # check if value can be interpreted as given type
  if is_type in [ is_bool, is_numeric, is_string ]:

    _is_type = ( ( val is None
        or is_type(val)
        or _is_eval )
      and ( not is_defined( default_val )
        or is_type(default_val) ) )

  elif is_type is is_sequence:

    _is_type = ( ( val is None
        or ( is_sequence(val)
          and ( len(val) == 0 or all( should_pass( val = v, is_type = is_item, default_val = required ) for v in val ) ) )
        or _is_eval )
      and ( not is_defined( default_val )
        or ( is_sequence(default_val)
          and ( len(default_val) == 0
          or all( should_pass( val = v, is_type = is_item, default_val = required ) for v in default_val ) ) ) ) )

  elif is_type is is_mapping:

    _is_type = ( ( val is None
        or ( is_mapping(val)
          and ( len(val) == 0 or all( should_pass( val = v, is_type = is_item, default_val = required ) for v in val.values() ) ) )
        or _is_eval )
      and ( not is_defined( default_val )
        or ( is_mapping(default_val)
          and ( len(default_val) == 0
            or all( should_pass( val = v, is_type = is_item, default_val = required ) for v in default_val.values() ) ) ) ) )

  else:
    assert False

  # check that value is valid
  val = get_val( val, default_val )

  _is_valid = _is_type and not (
    ( val is None and default_val is required )
    or ( restricted is not None and (
      len(restricted) == 0
      or any( not should_pass( val = v, is_type = is_type, is_item = is_item, default_val = required, min = min, max = max ) for v in restricted )
      or ( is_defined(default_val) and default_val not in restricted )
      or ( not _is_eval and is_defined(val) and val not in restricted ) ) )
    or ( min is not None and (
      ( is_defined(default_val) and default_val < min )
      or ( not _is_eval and is_defined(val) and val < min ) ) )
    or ( max is not None and (
      ( min is not None and max < min )
      or ( is_defined(default_val) and default_val > max )
      or ( not _is_eval and is_defined(val) and val > max ) ) ) )

  return _is_valid

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_default_val():
  class DummyType( SpecialType ):
    pass

  for prim in SIMPLE_PRIMS:
    with pytest.raises( SchemaDefinitionError ):
      s = prim(
        default_val = DummyType() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_restricted():

  for prim in SIMPLE_PRIMS:
    with pytest.raises( SchemaDefinitionError ):
      s = prim(
        restricted = "abcd" )

    with pytest.raises( SchemaDefinitionError ):
      s = prim(
        restricted = list() )
