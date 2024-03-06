import pytest
import numpy as np
import array

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
  SchemaDeclaredError,
  PJCEvaluated )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_declared():

  d = schema_declared( tag = 'my_type1', tag_key = None )

  assert( d.tag_key == 'type' )
  assert( d.tag == 'my_type1' )

  with pytest.raises( SchemaDeclaredError ):
    d = schema_declared( tag = None )

  with pytest.raises( SchemaDeclaredError ):
    d = schema_declared( tag = '1' )

  with pytest.raises( SchemaDeclaredError ):
    d = schema_declared( tag = 'mytag', tag_key = '1' )

  with pytest.raises( SchemaDeclaredError ):
    d = schema_declared( tag = 'mytag', tag_key = ['a', None] )

  with pytest.raises( SchemaDeclaredError ):
    d = schema_declared( tag = 'mytag', tag_key = ['a', '1'] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_declared_defined():

  d1 = schema_declared( tag = 'my_type1', tag_key = 'mytagkey' )
  d2 = schema_declared( tag = 'my_type2', tag_key = None )

  assert( not d1.schema_defined )
  assert( not d2.schema_defined )

  with pytest.raises( SchemaDeclaredError ):
    # must define using a schema class
    d1.schema_declared( None )

  with pytest.raises( SchemaDeclaredError ):
    # cannot be another declared
    d1.schema_declared( d2 )

  class MyType1( StructValued,
    declared = d1,
    struct = [ ] ):
    pass

  class MyType2( StructValued,
    tag = 'my_type2',
    tag_key = 'type',
    struct = [ ] ):
    pass

  class MyType3( StructValued,
    tag = 'my_type2',
    # mismatch key
    tag_key = 'type3',
    struct = [ ] ):
    pass

  class MyType4( StructValued,
    # mismatch tag
    tag = 'my_type3',
    tag_key = 'type',
    struct = [ ] ):
    pass


  with pytest.raises( SchemaDeclaredError ):
    # already defined
    d1.schema_declared( MyType2 )

  with pytest.raises( SchemaDeclaredError ):
    # tag/key mismatch
    d2.schema_declared( MyType3 )

  with pytest.raises( SchemaDeclaredError ):
    # tag/key mismatch
    d2.schema_declared( MyType4 )

  # should be ok
  d2.schema_declared( MyType2 )

  # should now be defined
  assert( d1.schema_defined )
  assert( d1.schema is MyType1.schema )
  assert( MyType1.tag == 'my_type1' )
  assert( MyType1.tag_key == 'mytagkey' )


  assert( d2.schema_defined )
  assert( d2.schema is MyType2.schema )
