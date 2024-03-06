import pytest
from pytest import raises

from pprint import pprint

import itertools

from partis.schema import (
  Loc,
  required,
  optional,
  derived,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
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
  any_schema )

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
def prim_struct_cases( ):
  vals = [
    None,
    "$expr:py self",
    "$func:py return self",
    { 'a' : 1, 'b': 2, 'c': 3 },
    { 'a':'a', 'b':'b', 'c':'c' } ]

  items = [
    ( IntPrim(), is_numeric ),
    ( FloatPrim(), is_numeric ),
    ( StrPrim(), is_string ) ]

  default_vals = [
    optional,
    required,
    { 'a' : 4, 'b': 5, 'c': 6 },
    { 'a': 'x', 'b': 'y', 'c': 'z' } ]

  restricteds = [
    None ]

  evaluateds = [
    None,
    PJCEvaluated ]

  test_cases = itertools.product(
    vals,
    items,
    default_vals,
    restricteds,
    evaluateds )

  if max_tests >= 0:
    test_cases = itertools.islice( test_cases, 0, max_tests * step_tests, step_tests )

  return test_cases


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.fixture( params = prim_struct_cases() )
def prim_struct_case( request ):
  return request.param

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_struct( prim_struct_case ):

  val, ( item, is_item ), default_val, restricted, evaluated = prim_struct_case


  if should_pass(
    val = val,
    is_type = is_mapping,
    is_item = is_item,
    default_val = default_val,
    restricted = restricted,
    evaluated = evaluated ):

    p = MapPrim(
      item = item,
      default_val = default_val,
      restricted = restricted,
      evaluated = evaluated,
      doc = "My struct" )

    assert p.default_val == default_val
    assert p.restricted == restricted
    assert p.doc.startswith("My struct")
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
    with pytest.raises(SchemaError):

      p = MapPrim(
        item = item,
        default_val = default_val,
        restricted = restricted,
        evaluated = evaluated,
        doc = "My struct" )

      _val = p.decode( val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_map_default():
  loc = Loc()

  p = MapPrim(
    item = BoolPrim() )

  val = {'a' : True, 'b': False }
  v = p.decode({'a' : True, 'b': False })
  w = p({'a' : True}, b = False)

  assert v == val
  assert w == val
  assert w == v
  assert v._encode == val
  assert w._encode == val
  assert p.encode(v) == val
  assert p.encode(w) == val

  with raises(SchemaValidationError):
    # required
    p()

  with raises(SchemaValidationError):
    # required
    p.decode()

  with raises(SchemaValidationError):
    # required
    p.encode()

  with raises(SchemaDefinitionError):
    # not a schema
    MapPrim(
      item = int )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_map_nesting():
  class MyType2( StructValued ):
    schema = dict(
      tag = 'my_type' )

    a = BoolPrim()


  p = MapPrim(
    item = MyType2 )

  val = {
    'x' : {
      'a' : True } }

  val2 = {
    'x' : {
      'type' : 'my_type',
      'a' : True } }

  v = p.decode(val)
  w = p(val)
  x = p( x = {
    'a' : True } )

  assert v == val2
  assert w == val2
  assert x == val2

  assert v._encode == val
  assert p.encode(v) == val
  assert p.encode(val) == val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# def test_prim_map_no_defaults( ):
#
#   class MyType2( StructValued ):
#     schema = dict(
#       tag = 'my_type',
#       default_val = derived )
#
#     a = BoolPrim(
#       default_val = True )
#
#
#   p = MapPrim(
#     item = MyType2,
#     default_val = { 'x' : {'a' : False } } )
#
#   v = p.decode()
#
#   _v = p.encode( v, no_defaults = True )
#   print(_v)
#
#   assert _v is None
#
#   _v = p.encode( val = { 'x' : {'a' : False } }, no_defaults = True )
#   print(_v)
#
#   assert _v is None
#
#   _v = p.encode( val = { 'x' : {'a' : True } }, no_defaults = True )
#   print(_v)
#
#   assert _v == { 'x' : None }
#
#   p2 = MapPrim(
#     item = MyType2,
#     default_val = { 'x' : {'a' : True } } )
#
#   _v = p2.encode( val = { 'x' : {'a' : True } }, no_defaults = True )
#   print(_v)
#
#   assert _v == None
