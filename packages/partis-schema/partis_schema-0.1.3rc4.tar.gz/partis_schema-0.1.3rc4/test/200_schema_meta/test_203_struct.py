import pytest
import numpy as np
import array

import itertools
from collections.abc import (
  Mapping )

from partis.utils import (
  odict )

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
  PJCEvaluated,
  StructValued,
  SchemaStructProxy )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
namespace_combos = [
  ( 'tag_key', 'key1', 'key2' ),
  ( 'tag', 'tag1', 'tag2' ),
  ( 'struct_proxy', 'x1', 'x2' ),
  ( 'declared', schema_declared( tag = 'tag1' ), schema_declared( tag = 'tag2' ) ),
  ( 'evaluated', PJCEvaluated, None ),
  ( 'default_val', { 'x1': True, 'x2' : True }, { 'x1': True, 'x2' : False } ),
  ( 'default_eval', { 'x1': True, 'x2' : True }, { 'x1': True, 'x2' : False } ),
  ( 'init_val', { 'x1': True, 'x2' : True }, { 'x1': True, 'x2' : False } ) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_namespace():

  # should pass
  for i in range(len(namespace_combos)):
    k, a, b = namespace_combos[i]

    d1 = {
      k : a }

    d2 = {
      k : a }

    if k == 'default_eval':
      # need to set as evaluated if setting default_eval
      d1['evaluated'] = PJCEvaluated
      d1['default_val'] = "$expr:py { 'x1' : True }"

      d2['evaluated'] = PJCEvaluated
      d2['default_val'] = "$expr:py { 'x1' : True }"

    class MyType1( StructValued, **d1 ):
      schema = d2
      x1 = BoolPrim()
      x2 = BoolPrim( default_val = True )


  class MyType1( StructValued ):
    schema = dict(
      struct_proxy = 'x1' )

    x1 = BoolPrim()
    x2 = BoolPrim( default_val = True )

  # should fail
  with pytest.raises( SchemaDefinitionError ):
    # must be mapping
    class MyType1( StructValued ):
      schema = list()
      pass

  # conflicting
  for i in range(len(namespace_combos)):
    k, a, b = namespace_combos[i]

    d1 = {
      k : a }

    d2 = {
      k : b }

    with pytest.raises( SchemaDefinitionError ):
      class MyType1( StructValued, **d1 ):
        schema = d2
        x1 = BoolPrim()
        x2 = BoolPrim( default_val = True )


  with pytest.raises( SchemaDefinitionError ):
    # proxy must be in schema
    class MyType1( StructValued ):
      schema = dict(
        struct_proxy = 'x1' )

  with pytest.raises( SchemaDefinitionError ):
    # proxy can be only non-default
    class MyType1( StructValued ):
      schema = dict(
        struct_proxy = 'x1' )
      x1 = BoolPrim()
      x2 = BoolPrim()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_declared():


  d1 = schema_declared( tag = 'my_type1', tag_key = 'mytagkey' )

  class MyType1( StructValued,
    declared = d1,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    struct = [ ] ):
    pass

  # already defined
  with pytest.raises( SchemaDeclaredError ):

    class MyType2( StructValued,
      declared = d1,
      struct = [ ] ):
      pass

  # type mismatch
  with pytest.raises( SchemaDefinitionError ):

    class MyType2( StructValued,
      declared = MyType1,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [ ] ):
      pass

  # tag mismatch
  with pytest.raises( SchemaDefinitionError ):
    d1 = schema_declared( tag = 'my_type1', tag_key = 'mytagkey' )

    class MyType2( StructValued,
      declared = d1,
      tag = 'my_type2',
      tag_key = 'mytagkey',
      struct = [ ] ):
      pass

  # tag_key mismatch
  with pytest.raises( SchemaDefinitionError ):
    d1 = schema_declared( tag = 'my_type1', tag_key = 'mytagkey2' )

    class MyType2( StructValued,
      declared = d1,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [ ] ):
      pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_values():

  class MyType1( StructValued,
    init_val = { 'x1' : True, 'x2' : False } ):

    x1 = BoolPrim()
    x2 = BoolPrim()

  assert( MyType1.schema.init_val == { 'type' : 'base', 'x1' : True, 'x2' : False } )

  expr = "$expr:py { 'x1' : True }"
  expr_normed = "$expr:py { 'x1' : True }"

  class MyType1( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    evaluated = PJCEvaluated,
    default_val = expr,
    default_eval = { 'x1' : True, 'x2' : False } ):

    x1 = BoolPrim()
    x2 = BoolPrim()

  assert( MyType1.schema.default_val == expr_normed )
  assert( MyType1.schema.default_eval == { 'mytagkey' : 'my_type1', 'x1' : True, 'x2' : False }  )
  # this should end up using the default_eval as the init_val, since default_val is an expression
  assert( MyType1.schema.init_val == { 'mytagkey' : 'my_type1', 'x1' : True, 'x2' : False } )


  # default_eval not used if default_val is not an expression
  with pytest.raises( SchemaDefinitionError ):

    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      evaluated = PJCEvaluated,
      default_val = { 'x1' : True },
      default_eval = { 'x1' : True } ):

      x1 = BoolPrim()
      x2 = BoolPrim()

  # type mismatch
  with pytest.raises( SchemaDefinitionError ):

    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      evaluated = "not an evaluated",
      struct = [ ] ):
      pass

  # evaluated
  class MyType1( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    evaluated = PJCEvaluated ):

    x1 = BoolPrim()


  #.............................................................................
  v1 = MyType1.schema.decode(expr)
  v2 = v1._eval()

  print( v1, v1._encode )
  print( v2, v2._encode )

  #.............................................................................
  # default_val
  # encode evaluated
  class MyType2( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    evaluated = PJCEvaluated,
    default_val = v1 ):

    x1 = BoolPrim()

  assert( MyType2.schema.default_val == expr_normed )

  # encode valued (from evaluation)
  class MyType3( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    default_val = v2 ):

    x1 = BoolPrim()

  assert( MyType3.schema.default_val == { 'mytagkey' : 'my_type1', 'x1' : True } )

  #.............................................................................
  # default_eval

  with pytest.raises( SchemaDefinitionError ):
    # cannot be evaluated
    class MyType2( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      default_val = expr,
      default_eval = v1,
      evaluated = PJCEvaluated ):

      x1 = BoolPrim()


  # encode valued (from evaluation, no longer evaluated)
  class MyType3( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    default_val = expr,
    default_eval = v2,
    evaluated = PJCEvaluated ):

    x1 = BoolPrim()

  assert( MyType3.schema.default_eval == { 'mytagkey' : 'my_type1', 'x1' : True } )

  with pytest.raises( SchemaDefinitionError ):
    # cannot be optional
    class MyType3( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      default_val = expr,
      default_eval = optional,
      evaluated = PJCEvaluated ):

      x1 = BoolPrim()

  with pytest.raises( SchemaDefinitionError ):
    # cannot be an expression
    class MyType3( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      default_val = expr,
      default_eval = expr,
      evaluated = PJCEvaluated ):

      x1 = BoolPrim()

  #.............................................................................
  # init_val

  with pytest.raises( SchemaDefinitionError ):
    # cannot be an expression

    # encode evaluated
    class MyType2( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      init_val = v1 ):

      x1 = BoolPrim()

  # encode evaluated
  class MyType2( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    init_val = v1,
    evaluated = PJCEvaluated ):

    x1 = BoolPrim()


  # encode valued (from evaluation)
  class MyType3( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    init_val = v2 ):

    x1 = BoolPrim()

  assert( MyType3.schema.init_val == { 'mytagkey' : 'my_type1', 'x1' : True }  )

  with pytest.raises( SchemaDefinitionError ):
    # cannot be a special value
    class MyType3( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      init_val = required ):

      x1 = BoolPrim()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_struct():
  b1 = BoolPrim()
  b2 = BoolPrim()

  class MyType1( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey',
    struct = [
      ('x1', b1 ),
      ('x2', b2 ) ] ):
    pass

  assert( MyType1.x1 is b1 )
  assert( MyType1.x2 is b2 )

  class MyType2( StructValued,
    tag = 'my_type2',
    tag_key = 'mytagkey',
    struct = dict(
      x1 = b1,
      x2 = b2 ) ):
    pass

  assert( MyType2.x1 is b1 )
  assert( MyType2.x2 is b2 )


  class MyType3( StructValued,
    tag = 'my_type3',
    tag_key = 'mytagkey',
    struct = odict(
      x1 = b1,
      x2 = b2 ) ):
    pass

  assert( MyType3.x1 is b1 )
  assert( MyType3.x2 is b2 )

  #.............................................................................
  # check invalid struct values

  with pytest.raises( SchemaDefinitionError ):
    # values must be schemas, not base types
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [
        ('x1', bool ),
        ('x2', bool ) ] ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # cannot be something that cannot be converted into a dict
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [1,2,3] ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # cannot be something other than dict or list
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = 1 ):
      pass

  #.............................................................................
  # check invalid struct keys

  with pytest.raises( SchemaDefinitionError ):
    # must be string
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [
        ( 1, b1 ) ] ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # must be a valid python variable name
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [
        ('1', b1 ) ] ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # key cannot be a 'protected' attribute
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [
        ('_p_', b1 )] ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # key cannot be a dunder attribute
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [
        ('__', b1 )] ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # key cannot be one of the 'mapping' functions
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [
        ('items', b1 )] ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # key cannot be the same as the tag_key
    class MyType1( StructValued,
      tag = 'my_type1',
      tag_key = 'mytagkey',
      struct = [
        ('mytagkey', b1 )] ):
      pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_inheritance():

  #.............................................................................
  class MyType1( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey1' ):
    x1 = b1

  class MyType2( StructValued,
    tag = 'my_type2',
    tag_key = 'mytagkey2' ):
    x2 = b2

  class MyType3( MyType1 ):
    pass

  assert( MyType3.tag == 'my_type1' )
  assert( MyType3.tag_key == 'mytagkey1' )
  assert( MyType3.x1 is b1 )


  #.............................................................................
  with pytest.raises( SchemaDefinitionError ):
    # no multiple inheritance
    class MyType5( MyType1, MyType2,
      tag = 'my_type5' ):
      pass


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_names():
  with pytest.raises( SchemaDefinitionError ):
    # cannot be number
    class MyType1( StructValued,
      tag = '1' ):
      pass

  with pytest.raises( SchemaDefinitionError ):
    # cannot be number
    class MyType2( StructValued,
      tag_key = '2' ):
      pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_proxy():
  b1 = BoolPrim()
  b2 = BoolPrim()


  #.............................................................................
  class MyType1( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey1',
    struct_proxy = 'x1' ):
    x1 = b1

  class MyType2( StructValued,
    tag = 'my_type1',
    tag_key = 'mytagkey1',
    struct_proxy = 'x2' ):
    x2 = b2

  class MyType3( MyType1 ):
    pass

  assert( MyType3.schema.struct_proxy == 'x1' )

  v1 = MyType3.schema.decode(True)
  v2 = MyType3.schema.decode(False)

  assert( v1.x1 == True )
  assert( v2.x1 == False )

  #.............................................................................
  with pytest.raises( SchemaDefinitionError ):
    # struct_proxy is ambiguous
    class MyType4( MyType1, MyType2 ):
      pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_doc():

  #.............................................................................
  class MyType1( StructValued ):
    """This is MyType1
    """
    schema = dict(
      tag = 'my_type1',
      tag_key = 'mytagkey1',
      default_val = { 'x1' : True, 'x2' : True } )

    x1 = BoolPrim()
    x2 = BoolPrim()

  doc = str(MyType1.__doc__)

  print(doc)

  assert( doc.startswith("This is MyType1") )
  assert( doc.find('my_type1') > 0 )
  assert( doc.find('mytagkey1') > 0 )
  assert( doc.find('x1') > 0 )
  assert( doc.find('x2') > 0 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_derived():
  #.............................................................................
  # derived only possible when all struct schemas have non-required default_vals
  with pytest.raises( SchemaDefinitionError ):
    class MyType1( StructValued ):
      schema = dict(
        tag = 'my_type1',
        tag_key = 'mytagkey1',
        default_val = derived )

      x1 = BoolPrim()
      x2 = BoolPrim()

    v = MyType1.schema.default_val

  class MyType2( StructValued ):
    schema = dict(
      tag = 'my_type2',
      tag_key = 'mytagkey2',
      default_val = derived )

    x1 = BoolPrim( default_val = True )
    x2 = BoolPrim( default_val = False )

  v = MyType2.schema.default_val
  assert( is_mapping(v) )

  assert( 'mytagkey2' in v )

  assert( 'x1' in v )
  assert( 'x2' in v )

  assert( v['mytagkey2'] == 'my_type2' )
  assert( v['x1'] == True )
  assert( v['x2'] == False )

  class MyType3( StructValued ):
    schema = dict(
      tag = 'my_type3',
      tag_key = 'mytagkey3',
      default_val = derived )

    y1 = MyType2

  w = MyType3.schema.default_val
  assert( is_mapping(w) )

  assert( 'mytagkey3' in w )
  assert( w['mytagkey3'] == 'my_type3' )

  assert( 'y1' in w )

  _v = w['y1']

  # should have removed the tag_key since there is no ambiguity in the schema
  assert( 'mytagkey2' not in _v )

  # should have same defaults as MyType2
  assert( 'x1' in _v )
  assert( 'x2' in _v )

  assert( _v['x1'] == True )
  assert( _v['x2'] == False )
