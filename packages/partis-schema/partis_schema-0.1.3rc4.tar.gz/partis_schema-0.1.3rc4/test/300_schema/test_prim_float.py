import pytest
from pytest import raises

from pprint import pprint

import itertools

from partis.schema import (
  Loc,
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
  SchemaDefinitionError,
  SchemaValidationError,
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
  is_valued_type,
  is_valued )

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
def prim_float_cases( ):
  default_vals = [
    optional,
    required,
    0.0,
    5.0,
    -10.0,
    11 ]

  mins = [
    None,
    -10,
    0,
    10 ]

  maxs = [
    None,
    -10,
    -0.0,
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
@pytest.fixture( params = prim_float_cases() )
def prim_float_case( request ):
  return request.param


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_float( prim_float_case ):

  val, default_val, min, max, restricted, evaluated = prim_float_case


  if should_pass(
    val = val,
    is_type = is_numeric,
    default_val = default_val,
    restricted = restricted,
    evaluated = evaluated,
    min = min,
    max = max ):

    p = FloatPrim(
      default_val = default_val,
      min = min,
      max = max,
      restricted = restricted,
      evaluated = evaluated,
      doc = "My float" )

    assert p.default_val == default_val
    assert p.min == min
    assert p.max == max
    assert p.restricted == restricted
    assert p.doc.startswith("My float")
    assert p.evaluated == NotEvaluated if evaluated is None else evaluated

    _val = p.decode( val )

    if evaluated is not None and evaluated.check(val):
      if is_defined(default_val):
        _val = _val._eval( context = { 'self' : default_val } )
        assert _val == p.default_val

    else:
      assert _val == get_val( val, default_val )

  else:
    with raises(SchemaError):

      p = FloatPrim(
        default_val = default_val,
        min = min,
        max = max,
        restricted = restricted,
        evaluated = evaluated,
        doc = "My float" )

      _val = p.decode( val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_float_default( ):

  p = FloatPrim( )

  v = p.decode( 1.0 )
  w = p(1.0)

  assert is_valued(v)
  assert is_valued_type(v)
  assert v == 1.0
  assert p.encode(v) == 1.0
  assert v._encode == 1.0


  assert is_valued(w)
  assert is_valued_type(w)
  assert w == v
  assert w == 1.0
  assert p.encode(w) == 1.0
  assert w._encode == 1.0

  loc = Loc()

  assert p.decode(1, loc)._loc is loc
  assert p(1, loc)._loc is loc

  with raises( ValueError ):
    # too many args
    p(1, loc, 'xyz')

  with raises(SchemaValidationError):
    # required
    p.decode( None )

  with raises(SchemaValidationError):
    # required
    p.encode( None )

  with raises(SchemaValidationError):
    # required
    p.decode()

  # complex ok as long as imaginary component is zero
  p.decode( 1.0 + 0.0 * 1j )

  with raises(SchemaValidationError):
    # complex -> float does not preserve value
    p.decode( 1j )

  p = FloatPrim(
    default_val = optional )

  assert p.decode( 1.0 ) == 1.0
  assert p.decode( None ) == None
  assert p.decode() == None

  p = FloatPrim(
    default_val = 1.0 )

  assert p.decode( 1.0 ) == 1.0
  assert p.decode( None ) == 1.0
  assert p.decode() == 1.0

  with raises(SchemaDefinitionError):
    p = FloatPrim(
      default_val = 1.0,
      min = 2.0 )

  with raises(SchemaDefinitionError):
    p = FloatPrim(
      default_val = 1.0,
      max = 0.0 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_float_init( ):

  p = FloatPrim( )

  assert p.init_val == 0.0

  p = FloatPrim(
    init_val = 1.0 )

  assert p.init_val == 1.0

  with raises(SchemaDefinitionError):
    p = FloatPrim(
      init_val = 1.0,
      min = 2.0 )

  with raises(SchemaDefinitionError):
    p = FloatPrim(
      init_val = 1.0,
      max = 0.0 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def test_prim_float_no_defaults( ):
#
#   p = FloatPrim(
#     default_val = 1.2345 )
#
#   v = p.decode()
#
#   _v = p.encode( v, no_defaults = True )
#
#   assert _v is None
#
#   assert p.encode( val = 1.2345, no_defaults = True ) is None
#
#   assert p.encode( val = 3.456, no_defaults = True ) == 3.456


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_float_bias( ):

  p = FloatPrim(
    default_val = 12345 )

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode(10)
  print(v._bias)
  assert float(v._bias) == 1

  p = FloatPrim(
    default_val = 55,
    restricted = [55, 10],
    min = 1,
    max = 100)

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode(10)
  print(v._bias)
  assert float(v._bias) == 4


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_prim_float_bias()
