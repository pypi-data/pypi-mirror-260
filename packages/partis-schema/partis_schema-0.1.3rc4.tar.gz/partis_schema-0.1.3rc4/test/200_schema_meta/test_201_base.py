import pytest
import numpy as np
import array
import unittest
import itertools
from partis.schema_meta.base import Bias, assert_valid_path
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
  SchemaError,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_schema_prim,
  is_schema_struct,
  is_schema,
  is_schema_declared,
  is_schema_struct_valued,
  is_valued_type,
  is_valued,
  is_evaluated,
  is_similar_value_type,
  any_schema,
  schema_declared,
  SchemaDefinitionError,
  PJCEvaluated )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
bools = [
  True,
  False ]

numerics = [
  1,
  0,
  1.0,
  0.0,
  -1.0,
  1e23 ]

strings = [
  "True",
  "False",
  "yes",
  "no",
  "1",
  "0",
  "1.0",
  "0.0",
  "\0" ]

sequences = [
  list(),
  [1,2,3],
  # TODO: fix arrays as sequences?
  # array.array('i', [1,2,3]),
  # np.array([1,2,3])
  ]

mappings = [
  dict(),
  { '1' : 1 } ]

type_combos = [
  ( is_bool, bools ),
  ( is_numeric, numerics ),
  ( is_string, strings ),
  ( is_sequence, sequences ),
  ( is_mapping, mappings ) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_is_base():

  n = len(type_combos)

  for i in range(n):
    is_f = type_combos[i][0]

    for j in range(n):
      objs = type_combos[j][1]

      if i == j:
        for t in objs:
          assert( is_f(t) )
      else:
        for t in objs:
          assert( not is_f(t) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_is_similar():
  n = len(type_combos)

  for i in range(n):
    a_objs = type_combos[i][1]

    for j in range(n):
      b_objs = type_combos[j][1]

      if i == j:
        for a in a_objs:
          for b in b_objs:
            assert( is_similar_value_type(a, b) )
      else:
        for a in a_objs:
          for b in b_objs:
            assert( not is_similar_value_type(a, b) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_is_schema():
  s = BoolPrim()

  d = schema_declared( tag = 'my_type1' )

  class MyType1( StructValued ):
    schema = dict(
      tag = 'my_type1',
      declared = d,
      struct = [ ] )

  class MyType2( StructValued,
    tag = 'my_type2',
    struct = [ ] ):
    pass

  s1 = s.decode( val = True )
  val = MyType1( dict() )

  assert( is_schema_prim(s) )
  assert( not is_schema_prim(bool) )

  assert( is_schema_declared(d) )
  assert( not is_schema_declared(MyType1) )

  assert( is_schema_struct(d) )
  assert( is_schema_struct(MyType1) )

  assert( not is_schema_struct(s) )

  assert( is_schema_struct_valued(val) )
  assert( not is_schema_struct_valued(s) )
  assert( not is_schema_struct_valued(d) )
  assert( not is_schema_struct_valued(MyType1) )

  assert( is_schema(s) )
  assert( is_schema(d) )
  assert( is_schema(MyType1) )
  assert( not is_schema(bool) )

  assert( any_schema(
    val = s,
    schemas = [ s, ] ) )

  assert( any_schema(
    val = s1,
    schemas = [ s, ] ) )

  assert( any_schema(
    val = val,
    schemas = [ MyType1, ] ) )

  assert( not any_schema(
    val = val,
    schemas = [ MyType2, ] ) )

  assert( any_schema(
    val = MyType1,
    schemas = [ MyType1, ] ) )

  assert( not any_schema(
    val = MyType1,
    schemas = [ MyType2, ] ) )

  assert( not any_schema(
    val = bool,
    schemas = [ s, ] ) )

  assert( not any_schema(
    val = bool,
    schemas = [ bool, ] ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_is_valued():
  s = BoolPrim(
    evaluated = PJCEvaluated )

  class MyType1( StructValued,
    tag = 'my_type1',
    struct = [ ] ):
    pass

  s1 = s.decode( val = True )
  s2 = s.decode( val = "$expr:py True" )
  val1 = MyType1( dict() )

  assert( is_valued_type(s1) )
  assert( is_valued_type(val1) )
  assert( not is_valued_type(True) )

  assert( is_valued(s1) )
  assert( is_valued([ s1, s1, s1 ]) )
  assert( is_valued({ 'a': s1, 'b': s1, 'c': s1 }) )
  assert( is_valued(val1) )
  assert( is_valued(True) )

  assert( not is_valued(s2) )
  assert( not is_valued([ s2, s1, s1 ]) )
  assert( not is_valued({ 'a': s2, 'b': s1, 'c': s1 }) )

  assert( is_evaluated(s2._src) )
  assert( not is_evaluated(s1._src) )
  assert( not is_valued_type(s2._src) )

def test_add():
  s = Bias(5)
  result = s.__add__(12)

  assert result._val == 17.0

class ValidTestCase(unittest.TestCase):
  def test_valid_path(self):
    s = '~/home/patrick/Desktop/proj/'
    instace = ""
    with self.assertRaises(Exception) as context:
      result = assert_valid_path(s)

    #with self.assertRaises(Exception) as context:


if __name__ == "__main__":
  unittest.main() 