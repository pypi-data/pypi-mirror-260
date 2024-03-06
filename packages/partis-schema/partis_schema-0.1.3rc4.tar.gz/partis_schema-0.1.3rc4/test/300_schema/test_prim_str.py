import pytest
from pytest import raises

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
  SchemaDefinitionError,
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
def prim_str_cases( ):
  default_vals = [
    optional,
    required,
    "xyz",
    "asd  asdd" ]

  restricteds = [
    None,
    ["qwe"],
    ["xyz"],
    ["qwe", "asd  asdd"] ]

  evaluateds = [
    None,
    PJCEvaluated ]

  vals = [
    None,
    "$expr:py self",
    "$func:py return self",
    "xyz",
    "qwe",
    "asd  asdd",
    "abc",
    "123.5" ]

  test_cases = itertools.product(
    vals,
    default_vals,
    restricteds,
    evaluateds )

  if max_tests >= 0:
    test_cases = itertools.islice( test_cases, 0, max_tests * step_tests, step_tests )

  return test_cases


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.fixture( params = prim_str_cases() )
def prim_str_case( request ):
  return request.param

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_str( prim_str_case ):

  val, default_val, restricted, evaluated = prim_str_case


  if should_pass(
    val = val,
    is_type = is_string,
    default_val = default_val,
    restricted = restricted,
    evaluated = evaluated ):

    p = StrPrim(
      default_val = default_val,
      restricted = restricted,
      evaluated = evaluated,
      doc = "My string" )

    assert p.default_val == default_val
    assert p.restricted == restricted
    assert p.doc.startswith("My string")
    assert p.evaluated == NotEvaluated if evaluated is None else evaluated

    _val = p.decode( val )

    if evaluated is not None and evaluated.check(val):
      if is_defined(default_val):
        # only check evaluated when default value is defined
        _val = _val._eval( context = { 'self' : default_val } )
        assert _val == p.default_val

    else:
      assert _val == get_val( val, default_val )

  else:
    with raises(SchemaError):

      p = StrPrim(
        default_val = default_val,
        restricted = restricted,
        evaluated = evaluated,
        doc = "My string" )

      _val = p.decode( val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_str_pattern():
  p = StrPrim(
    pattern = r"\w\d\w\d",
    doc = "My string" )

  x = p.decode( "a1b2" )
  assert x == "a1b2"

  with raises(SchemaError):
    x = p.decode( "a1b2c3" )

  with raises(SchemaError):
    x = p.decode( "abc" )

  with raises(SchemaDefinitionError):
    p = StrPrim(
      default_val = "a1b2c3",
      pattern = r"\w\d\w\d",
      doc = "My string" )

  with raises(SchemaDefinitionError):
    p = StrPrim(
      restricted = [ "a1b2c3" ],
      pattern = r"\w\d\w\d",
      doc = "My string" )

  with raises(SchemaDefinitionError):
    p = StrPrim(
      pattern = r"asd(&*^$*&G##&])",
      doc = "My string" )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_str_char_case():
  with raises(SchemaError):
    p = StrPrim(
      char_case = 'asdasd',
      doc = "My string" )

  s_upper = "A1B2C3"
  s_lower = "a1b2c3"

  p_upper = StrPrim(
    default_val = s_lower,
    char_case = 'upper',
    doc = "My string" )

  p_lower = StrPrim(
    default_val = s_upper,
    char_case = 'lower',
    doc = "My string" )

  assert p_upper.default_val == s_upper
  assert p_upper.decode() == s_upper
  assert p_upper.decode(s_upper) == s_upper
  assert p_upper.decode(s_lower) == s_upper

  assert p_upper.encode() is None
  assert p_upper.encode(s_upper) == s_upper
  assert p_upper.encode(s_lower) == s_upper

  assert p_lower.default_val == s_lower
  assert p_lower.decode() == s_lower
  assert p_lower.decode(s_upper) == s_lower
  assert p_lower.decode(s_lower) == s_lower

  assert p_lower.encode() is None
  assert p_lower.encode(s_upper) == s_lower
  assert p_lower.encode(s_lower) == s_lower

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_str_strip():
  val = "asd"
  sval = f"  {val}  "

  p = StrPrim(
    strip = True,
    default_val = sval )

  assert p.default_val == val
  assert p.decode() == val
  assert p.decode(val) == val
  assert p.decode(sval) == val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_nonempty_str():

  with raises(SchemaDefinitionError):
    p = StrPrim(
      nonempty = True,
      default_val = required )

  with raises(SchemaDefinitionError):
    p = StrPrim(
      nonempty = True,
      default_val = optional )

  with raises(SchemaDefinitionError):
    p = StrPrim(
      nonempty = True,
      default_val = "" )

  p = StrPrim(
    nonempty = True,
    default_val = "asd" )

  p = StrPrim(
    nonempty = True,
    init_val = "asd",
    default_val = required )

  p = StrPrim(
    nonempty = True,
    init_val = "asd",
    default_val = optional )

  assert p.decode() == None

  with raises(SchemaError):
    p.decode("")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def test_prim_str_no_defaults( ):
#
#   p = StrPrim(
#     default_val = 'abcdef' )
#
#   v = p.decode()
# 
#   _v = p.encode( v, no_defaults = True )
#
#   assert _v is None
#
#   assert p.encode( val = 'abcdef', no_defaults = True ) is None
#
#   assert p.encode( val = 'xyz', no_defaults = True ) == 'xyz'


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_str_bias( ):

  p = StrPrim(
    default_val = 'abcd' )

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode('wxyz')
  print(v._bias)
  assert float(v._bias) == 1

  p = StrPrim(
    default_val = 'abcd',
    restricted = ['abcd', 'wxyz', 20*'x'],
    pattern = r'.*',
    nonempty = True,
    max_lines = 3,
    max_cols = 100 )

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode('wxyz')
  print(v._bias)
  assert float(v._bias) == 12

  v = p.decode(20*'x')
  print(v._bias)
  assert float(v._bias) == 44


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_prim_str_bias()
