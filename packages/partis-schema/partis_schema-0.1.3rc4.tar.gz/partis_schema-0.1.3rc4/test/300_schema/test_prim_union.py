import pytest
from copy import copy
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
  StructValued,
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
def prim_union_cases( ):
  vals = [
    None,
    "$expr:py self",
    "$func:py return self",
    1,
    1.0,
    "abc",
    [ 1, 2, 3 ],
    { 'a': 'x', 'b': 'y', 'c': 'z' } ]

  class MySchema1( StructValued ):
    schema = dict(
      tag = 'my_schema1',
      struct = [
        ( 'a', StrPrim() ),
        ( 'b', StrPrim() ),
        ( 'c', StrPrim() ) ] )


  class MySchema2( StructValued ):
    schema = dict(
      tag = 'my_schema2',
      struct = [
        ( 'a', StrPrim() ),
        ( 'b', StrPrim() ),
        ( 'c', StrPrim() ) ] )


  valid_cases = [
    # valid combinations of cases
    ( True, [
      ( BoolPrim(), is_bool, None ),
      ( IntPrim(), is_numeric, None ),
      ( StrPrim(), is_string, None ),
      ( SeqPrim( item = IntPrim() ), is_sequence, is_numeric ),
      ( MapPrim( item = StrPrim() ), is_mapping, is_string ) ] ),
    ( True, [
      ( MySchema1, is_mapping, is_string ),
      ( MySchema2, is_mapping, is_string ) ] ),
    ( True, [
      ( BoolPrim(), is_bool, None ),
      ( FloatPrim(), is_numeric, None ),
      ( SeqPrim( item = IntPrim() ), is_sequence, is_numeric ),
      ( MySchema1, is_mapping, is_string ) ] ),
    # invalid combinations of cases
    ( False, [
      ( BoolPrim(), is_bool, None ),
      ( BoolPrim(), is_bool, None ) ] ),
    ( False, [
      ( IntPrim(), is_numeric, None ),
      ( FloatPrim(), is_numeric, None ) ] ),
    ( False, [
      ( IntPrim(), is_numeric, None ),
      ( IntPrim(), is_numeric, None ) ] ),
    ( False, [
      ( FloatPrim(), is_numeric, None ),
      ( FloatPrim(), is_numeric, None ) ] ),
    ( False, [
      ( StrPrim(), is_numeric, None ),
      ( StrPrim(), is_numeric, None ) ] ),
    ( False, [
      ( SeqPrim( item = IntPrim() ), is_sequence, is_numeric ),
      ( SeqPrim( item = StrPrim() ), is_sequence, is_string ) ] ),
    ( False, [
      ( MapPrim( item = IntPrim() ), is_mapping, is_numeric ),
      ( MapPrim( item = StrPrim() ), is_mapping, is_string )  ] ),
    ( False, [
      ( MapPrim( item = IntPrim() ), is_mapping, is_numeric ),
      ( MySchema1, is_mapping, is_string ) ] ) ]

  default_vals = [
    optional,
    required,
    True,
    1,
    "abc",
    [ 1, 2, 3 ],
    { 'a': 'x', 'b': 'y', 'c': 'z' },
    { 'type': 'my_schema1', 'a': 'x', 'b': 'y', 'c': 'z' },
    { 'type': 'my_schema2', 'a': 'x', 'b': 'y', 'c': 'z' } ]

  restricteds = [
    None ]

  evaluateds = [
    None,
    PJCEvaluated ]

  test_cases = itertools.product(
    vals,
    valid_cases,
    default_vals,
    restricteds,
    evaluateds )

  if max_tests >= 0:
    test_cases = itertools.islice( test_cases, 0, max_tests * step_tests, step_tests )

  return test_cases



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.fixture( params = prim_union_cases() )
def prim_union_case( request ):
  return request.param


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_union( prim_union_case ):

  val, ( valid, cases ), default_val, restricted, evaluated = prim_union_case


  _should_pass_default_val = not is_defined( default_val )
  _should_pass_val = False
  num_schemas = sum( is_schema_struct(case) for case, is_type, is_item in cases )

  for case, is_type, is_item in cases:
    valid_val = True
    valid_default_val = True

    if is_schema_struct(case):
      # this checking the schema tag
      if is_mapping(val):
        if (
          num_schemas > 1
          and (
            case.tag_key not in val
            or val[case.tag_key] != case.tag ) ):

          valid_val = False

      if is_mapping(default_val):
        # print(type(case), case)
        # print(dir(case))

        if (
          num_schemas > 1
          and (
            case.tag_key not in default_val
            or default_val[case.tag_key] != case.tag ) ):

          valid_default_val = False

    _should_pass_val = (
      _should_pass_val
      or ( valid_val and should_pass(
        val = val,
        is_type = is_type,
        is_item = is_item,
        default_val = required if default_val is required else optional,
        restricted = restricted,
        evaluated = evaluated ) ) )

    _should_pass_default_val = (
      _should_pass_default_val
      or ( valid_default_val and should_pass(
        val = default_val,
        is_type = is_type,
        is_item = is_item,
        default_val = default_val,
        restricted = restricted,
        evaluated = evaluated ) ) )

    # print( _should_pass_val, _should_pass_default_val, case, is_type, is_item )


  _should_pass = _should_pass_val and _should_pass_default_val

  cases = [ c[0] for c in cases ]

  if valid and _should_pass:
    p = UnionPrim(
      cases = cases,
      default_val = default_val,
      restricted = restricted,
      evaluated = evaluated,
      doc = "My union" )

    schemas = [s for s in cases if is_schema_struct(s)]

    _default_val = copy(default_val)

    if is_mapping(default_val) and len(schemas) == 1 and schemas[0].tag_key in default_val:

      _default_val.pop(schemas[0].tag_key)

    assert p.default_val == _default_val
    assert p.restricted == restricted
    assert p.cases == cases
    assert p.doc.startswith("My union")
    assert p.evaluated == NotEvaluated if evaluated is None else evaluated

    compare = True
    _val = p.decode( val )
    p.encode( _val )

    _expected = get_val( val, default_val )

    if evaluated is not None and evaluated.check(val):
      if is_defined(default_val):
        # only check evaluated when default value is defined
        _val = _val._eval( context = { 'self' : default_val } )
        _expected = default_val
      else:
        compare = False

    if compare:
      if is_schema_struct_valued( _val ):
        for k, v in _expected.items():
          if k != _val._schema.tag_key:
            assert k in _val and v == _val[k]

      else:
        assert _expected == _val

  else:
    with pytest.raises(SchemaError):

      p = UnionPrim(
        cases = cases,
        default_val = default_val,
        restricted = restricted,
        evaluated = evaluated,
        doc = "My union" )

      _val = p.decode( val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_union_bias( ):

  a = BoolPrim(
    default_val = True )

  b = IntPrim(
    default_val = 55,
    min = 1,
    max = 100)

  d = StrPrim(
    default_val = 'abcd',
    pattern = r'.*',
    nonempty = True,
    max_lines = 3,
    max_cols = 100 )

  p = UnionPrim(
    cases = [a, b, d],
    default_case = 0 )

  v = p.decode()
  print(v._bias)
  assert float(v._bias) == 0

  v = p.decode(True)
  print(v._bias)
  assert float(v._bias) == 1

  v = p.decode(10)
  print(v._bias)
  assert float(v._bias) == 3

  v = p.decode('wxyz')
  print(v._bias)
  assert float(v._bias) == 8

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_prim_union_bias()
