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
def prim_bool_cases( ):
  default_vals = [
    optional,
    required,
    True,
    False ]

  restricteds = [
    None,
    [True],
    [False],
    [True, False] ]

  evaluateds = [
    None,
    PJCEvaluated ]

  vals = [
    None,
    "$expr:py self",
    "$func:py return self",
    True,
    False,
    1,
    0 ]

  test_cases = itertools.product(
    vals,
    default_vals,
    restricteds,
    evaluateds )

  if max_tests >= 0:
    test_cases = itertools.islice( test_cases, 0, max_tests * step_tests, step_tests )

  return test_cases

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.fixture( params = prim_bool_cases() )
def prim_bool_case( request ):
  return request.param


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_bool( prim_bool_case ):

  val, default_val, restricted, evaluated = prim_bool_case


  if should_pass(
    val = val,
    is_type = is_bool,
    default_val = default_val,
    restricted = restricted,
    evaluated = evaluated ):

    p = BoolPrim(
      default_val = default_val,
      restricted = restricted,
      evaluated = evaluated,
      doc = "My bool" )

    assert p.default_val == default_val
    assert p.restricted == restricted
    assert p.doc.startswith("My bool")
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

      p = BoolPrim(
        default_val = default_val,
        restricted = restricted,
        evaluated = evaluated,
        doc = "My bool" )

      _val = p.decode( val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def test_prim_bool_no_defaults( ):
#
#   p = BoolPrim(
#     default_val = True )
#
#   v = p.decode()
#
#   _v = p.encode( v, no_defaults = True )
#
#   assert _v is None
#
#   assert p.encode( val = True, no_defaults = True ) is None
#
#   assert p.encode( val = False, no_defaults = True ) == False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_bool_bias( ):

  p = BoolPrim(
    default_val = True )

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode(True)
  print(v._bias)
  assert float(v._bias) == 1

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_prim_bool_bias()
