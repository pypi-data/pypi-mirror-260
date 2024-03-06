import pytest

from pprint import pprint

import itertools

from partis.schema import (
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
  SchemaDefinitionError )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_schema():

  # test using metaclass arguments
  class MyType1( StructValued,
    tag = 'my_type',
    struct = [
      ( 'a', BoolPrim() ),
      ( 'b', IntPrim() ),
      ( 'c', FloatPrim() ),
      ( 'd', StrPrim() ),
      ( 'e', SeqPrim(
        item = StrPrim() ) ),
      ( 'f', MapPrim(
        item = StrPrim() ) )  ] ):
    pass

  # test using class namespace arguments
  class MyType2( StructValued ):
    schema = dict(
      tag = 'my_type' )

    a = BoolPrim()
    b = IntPrim()
    c = FloatPrim()
    d = StrPrim()
    e =  SeqPrim(
      item = StrPrim() )

    f = MapPrim(
      item = StrPrim() )

  doc_yaml = """{ type: my_type, a: True, b: 1, c: 1.0, d: "one", e: ["x", "y", "z"], f: { q: q, r: r} }"""

  for cls in [ MyType1, MyType2 ]:
    obj = loads( doc_yaml, cls )

    assert isinstance( obj, cls )
    assert obj._schema is cls.schema
    assert obj._schema.tag == 'my_type'
    assert obj.a == True
    assert obj.b == 1
    assert obj.c == 1.0
    assert obj.d == "one"
    assert obj.e == ["x", "y", "z"]
    assert obj.f == { "q": "q", "r": "r"}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_struct_proxy():

  # test using metaclass arguments
  class MyType1( StructValued,
    tag = 'my_type',
    struct_proxy = 'a',
    struct = [
      ( 'a', BoolPrim() ),
      ( 'b', IntPrim( default_val = 1 ) ) ] ):
    pass

  x = MyType1( True )

  assert x.a == True
  assert x.b == 1

  with pytest.raises( SchemaDefinitionError ):
    # should raise error because struct_proxy conflicts with union
    u = UnionPrim(
      cases = [
        MyType1,
        BoolPrim() ] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_struct_no_defaults( ):

  class MyType2( StructValued ):
    schema = dict(
      tag = 'my_type',
      default_val = derived )

    a = BoolPrim(
      default_val = True )

    b = IntPrim(
      default_val = 1234 )

    c = FloatPrim(
      default_val = 1.234 )

    d = StrPrim(
      default_val = 'abcdef' )

  p = MyType2.schema
  print('default_val', p.default_val)

  v = MyType2()

  print(v)
  _v = p.encode( v, no_defaults = True )
  print(_v)
  assert _v == {'type': 'my_type'}

  _v = p.encode( val = { 'a' : True, 'b' : 1234, 'c' : 1.234, 'd' : 'abcdef' }, no_defaults = True )
  print(_v)

  assert _v == {'type': 'my_type'}

  _v = p.encode( val = { 'a' : True, 'b' : 6789, 'c' : 1.234, 'd' : 'xyz' }, no_defaults = True )
  print(_v)

  assert _v == { 'type' : 'my_type', 'b' : 6789, 'd' : 'xyz' }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_struct_bias( ):

  class MyType( StructValued ):
    schema = dict(
      tag = 'my_type',
      default_val = derived )

    a = BoolPrim(
      default_val = True )

    b = IntPrim(
      default_val = 55,
      min = 1,
      max = 100)

    c = FloatPrim(
      default_val = 55,
      min = 1,
      max = 100)

    d = StrPrim(
      default_val = 'abcd',
      pattern = r'.*',
      nonempty = True,
      max_lines = 3,
      max_cols = 100 )

  v = MyType()
  print(v._bias)
  assert float(v._bias) == 0

  v = MyType(
    a = True,
    b = 10,
    c = 12.34,
    d = 'wxyz' )

  print(v._bias)
  assert float(v._bias) == (
    # keys
    4
    # bool
    + 1
    # int + float
    + 2*3
    # str
    + 8 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_struct_bias()
