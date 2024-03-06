import pytest

from pprint import pprint

import itertools

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
  NotEvaluated,
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
  any_schema, )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

from test_prim import (
  is_defined,
  get_val,
  should_pass,
  max_tests,
  step_tests )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# use this to only run sub-set of all possible tests
# max_tests = -1
# step_tests = 1

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def prim_int_cases( ):
  default_vals = [
    optional,
    required,
    0,
    5,
    -10,
    11 ]

  mins = [
    None,
    -10,
    0,
    10 ]

  maxs = [
    None,
    -10,
    0,
    10 ]

  restricteds = [
    None,
    [0],
    [],
    [0, 10, 11] ]

  evaluateds = [
    None,
    PJCEvaluated ]

  vals = [
    None,
    "$expr:py self",
    "$func:py return self",
    -11,
    -10,
    0,
    10,
    11 ]

  test_cases = itertools.product(
    vals,
    default_vals,
    mins,
    maxs,
    restricteds,
    evaluateds )

  if max_tests >= 0:
    test_cases = itertools.islice( test_cases, 0, max_tests * step_tests, step_tests )

  return test_cases



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.fixture( params = prim_int_cases() )
def prim_int_case( request ):
  return request.param


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_int( prim_int_case ):

  val, default_val, min, max, restricted, evaluated = prim_int_case

  if should_pass(
    val = val,
    is_type = is_numeric,
    default_val = default_val,
    restricted = restricted,
    evaluated = evaluated,
    min = min,
    max = max ):

    p = IntPrim(
      default_val = default_val,
      min = min,
      max = max,
      restricted = restricted,
      evaluated = evaluated,
      doc = "My integer" )

    assert p.default_val == default_val
    assert p.min == min
    assert p.max == max
    assert p.restricted == restricted
    assert p.doc.startswith("My integer")
    assert p.evaluated == NotEvaluated if evaluated is None else evaluated

    _val = p.decode( val )

    if evaluated is not None and evaluated.check(val):
      if is_defined(default_val):
        _val = _val._eval( context = { 'self' : default_val } )
        assert _val == p.default_val

    else:
      assert _val == get_val( val, default_val )


  else:
    with pytest.raises(SchemaError):

      p = IntPrim(
        default_val = default_val,
        min = min,
        max = max,
        restricted = restricted,
        evaluated = evaluated,
        doc = "My integer" )

      _val = p.decode( val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def test_prim_int_no_defaults( ):
#
#   p = IntPrim(
#     default_val = 12345 )
#
#   v = p.decode()
#
#   _v = p.encode( v, no_defaults = True )
#
#   assert _v is None
#
#   assert p.encode( val = 12345, no_defaults = True ) is None
#
#   assert p.encode( val = 3456, no_defaults = True ) == 3456

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_int_bias( ):

  p = IntPrim(
    default_val = 12345 )

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode(10)
  print(v._bias)
  assert float(v._bias) == 1

  p = IntPrim(
    default_val = 55,
    restricted = [55, 10],
    min = 1,
    max = 100 )

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode(10)
  print(v._bias)
  assert float(v._bias) == 4


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_prim_int_bias()
