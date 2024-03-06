import pytest
from pytest import raises

from pprint import pprint

import itertools

from partis.schema import (
  required,
  optional,
  BoolPrimDeclared,
  BoolPrim,
  IntPrimDeclared,
  IntPrim,
  FloatPrimDeclared,
  FloatPrim,
  StrPrimDeclared,
  StrPrim,
  SeqPrimDeclared,
  SeqPrim,
  MapPrimDeclared,
  MapPrim,
  UnionPrimDeclared,
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
  SchemaDefinitionError,
  SchemaDeclaredError,
  schema_declared )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_prim_declared():
  scalar_cases = [
    ( IntPrimDeclared, IntPrim ),
    ( BoolPrimDeclared, BoolPrim ),
    ( FloatPrimDeclared, FloatPrim ),
    ( StrPrimDeclared, StrPrim ) ]

  item_cases = [
    ( SeqPrimDeclared, SeqPrim ),
    ( MapPrimDeclared, MapPrim ) ]

  for decl, prim in scalar_cases:
    d = decl()

    with raises( SchemaDeclaredError ):
      d.schema

    s = prim( declared = d )

    assert d.schema is s

  for decl, prim in item_cases:
    for idecl, iprim in scalar_cases:

      d = decl()
      di = idecl()

      with raises( SchemaDeclaredError ):
        d.schema

      s = prim(
        declared = d,
        item = di )

      assert not d.schema_defined
      assert not s.schema_defined


      si = iprim( declared = di )

      assert d.schema is s

      assert s.item.schema is si

      assert d.schema.item.schema is si

    d = UnionPrimDeclared()

    with raises( SchemaDeclaredError ):
      d.schema

    s = UnionPrim(
      declared = d,
      cases = [
        BoolPrim(),
        IntPrim() ]  )

    assert d.schema is s

    cases = [ a[0]() for a in scalar_cases[1:] ]

    s = UnionPrim(
      cases = cases )

    assert not s.schema_defined

    _cases = [
      a[1]( declared = d ) for d, a in zip( cases, scalar_cases[1:] ) ]

    assert s.schema_defined

    for d, c in zip( cases, _cases ):
      assert d.schema is c

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_struct_declared():

  my_declared = schema_declared( tag = 'my_type', tag_key = 'my_tag' )

  with raises( SchemaDeclaredError ):
    # schema not yet defined
    s = my_declared.schema

  with raises( SchemaError ):
    # cannot instantiate a schema declaration
    v = my_declared( val = dict() )

  with raises( SchemaDefinitionError ):

    # test using metaclass arguments
    class MyType1( StructValued,
      tag = 'not_my_type',
      declared = my_declared ):
      pass

  class MyType2( StructValued,
    declared = my_declared ):
    pass

  assert my_declared.schema is MyType2.schema
  assert MyType2.tag_key == 'my_tag'
  assert MyType2.tag == 'my_type'
