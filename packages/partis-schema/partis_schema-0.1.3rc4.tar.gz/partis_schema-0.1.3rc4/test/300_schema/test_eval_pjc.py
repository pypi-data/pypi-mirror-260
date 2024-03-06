
import pytest

from partis.schema import (
  SchemaError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaValidationError,
  SchemaEvaluationError,
  SchemaHint,
  Loc,
  required,
  optional,
  derived,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_optional,
  is_required,
  is_derived,
  is_schema_prim,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  is_evaluated_class,
  is_evaluated,
  is_valued,
  is_valued_type,
  any_schema,
  BoolValued,
  IntValued,
  FloatValued,
  StrValued,
  SeqValued,
  MapValued,
  PyEvaluated,
  PJCEvaluated,
  PassPrim,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  UnionPrim,
  MapPrim,
  StructValued )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NoRaise:
  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
NoError = None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _cases( ):


  # test using metaclass arguments
  class MyType1( StructValued ):
    schema = dict(
      tag = 'my_type',
      struct = [
        ( 'a', BoolPrim() ),
        ( 'b', IntPrim() ),
        ( 'c', FloatPrim() ),
        ( 'd', StrPrim() ),
        ( 'e', SeqPrim(
          item = IntPrim() ) ),
        ( 'f', MapPrim(
          item = StrPrim() ) )  ],
      evaluated = PJCEvaluated )


  # test using class namespace arguments
  class MyType2( StructValued ):
    schema = dict(
      tag = 'my_type',
      evaluated = PJCEvaluated )

    a = BoolPrim()
    b = IntPrim()
    c = FloatPrim()
    d = StrPrim()
    e =  SeqPrim(
      item = IntPrim() )

    f = MapPrim(
      item = StrPrim() )

  base_cases = [
    ( NoError,
      BoolPrim(
        evaluated = PJCEvaluated ),
      BoolValued,
      "1 == 1",
      True ),
    ( SchemaEvaluationError,
      BoolPrim(
        evaluated = PJCEvaluated ),
      BoolValued,
      "1",
      True ),
    ( NoError,
      IntPrim(
        evaluated = PJCEvaluated ),
      IntValued,
      "12 + 30",
      42 ),
    ( SchemaEvaluationError,
      IntPrim(
        evaluated = PJCEvaluated ),
      IntValued,
      "3/2",
      1 ),
    ( SchemaEvaluationError,
      IntPrim(
        evaluated = PJCEvaluated ),
      IntValued,
      "'42",
      42 ),
    ( NoError,
      FloatPrim(
        evaluated = PJCEvaluated ),
      FloatValued,
      "2.0 * 4.0",
      8.0 ),
    ( NoError,
      FloatPrim(
        evaluated = PJCEvaluated ),
      FloatValued,
      "2 * 4",
      8 ),
    ( SchemaEvaluationError,
      FloatPrim(
        evaluated = PJCEvaluated ),
      FloatValued,
      "'8.0'",
      8.0 ),
    ( NoError,
      StrPrim(
        evaluated = PJCEvaluated ),
      StrValued,
      "\"hello world\"",
      "hello world" ),
    ( SchemaEvaluationError,
      StrPrim(
        evaluated = PJCEvaluated ),
      StrValued,
      "8.0",
      "8.0" ),
    ( NoError,
      SeqPrim(
        item = IntPrim(),
        evaluated = PJCEvaluated ),
      SeqValued,
      "[ 1,2,3,4 ]",
      [ 1,2,3,4 ] ),
    ( SchemaEvaluationError,
      SeqPrim(
        item = IntPrim(),
        evaluated = PJCEvaluated ),
      SeqValued,
      "[ 1,2,'3',4 ]",
      [ 1,2,3,4 ] ),
    ( NoError,
      MapPrim(
        item = IntPrim(),
        evaluated = PJCEvaluated ),
      MapValued,
      "{ 'a': 1, 'b': 2, 'c': 3 }",
      { 'a': 1, 'b': 2, 'c': 3 } ),
    ( SchemaEvaluationError,
      MapPrim(
        item = IntPrim(),
        evaluated = PJCEvaluated ),
      MapValued,
      "{ 'a': 1, 'b': '2', 'c': 3 }",
      { 'a': 1, 'b': 2, 'c': 3 } ),
    ( NoError,
      MyType1,
      MyType1,
      "{ 'type': 'my_type', 'a': 1 == 1, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, 3 ], 'f': { 'q': 'q', 'r': 'r'} }",
      { 'type': 'my_type', 'a': True, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, 3 ], 'f': { 'q': 'q', 'r': 'r'} } ),
    ( SchemaEvaluationError,
      MyType1,
      MyType1,
      "{ 'type': 'my_type', 'a': 1 == 1, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, '3' ], 'f': { 'q': 'q', 'r': 'r'} }",
      { 'type': 'my_type', 'a': True, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, 3 ], 'f': { 'q': 'q', 'r': 'r'} } ),
    ( SchemaEvaluationError,
      MyType1,
      MyType1,
      "{}",
      {} ),
    ( NoError,
      MyType2,
      MyType2,
      "{ 'type': 'my_type', 'a': 1 == 1, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, 3 ], 'f': { 'q': 'q', 'r': 'r'} }",
      { 'type': 'my_type', 'a': True, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, 3 ], 'f': { 'q': 'q', 'r': 'r'} } ),
    ( SchemaEvaluationError,
      MyType2,
      MyType2,
      "{ 'type': 'my_type', 'a': 1 == 1, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, '3' ], 'f': { 'q': 'q', 'r': 'r'} }",
      { 'type': 'my_type', 'a': True, 'b': 1, 'c': 1.0, 'd': '1', 'e': [ 1, 2, 3 ], 'f': { 'q': 'q', 'r': 'r'} } ),
    ( SchemaEvaluationError,
      MyType2,
      MyType2,
      "{}",
      {} ) ]

  expr_py_tmpl = "$expr:py {}"
  func_py_tmpl = "$func:py\n return {}"

  tmpls = [
    expr_py_tmpl,
    func_py_tmpl ]

  all_cases = list()

  for tmpl in tmpls:
    for case in base_cases:
      exc, schema, cls, src, val = case

      src = tmpl.format(src)

      case = ( exc, schema, cls, src, val )

      all_cases.append( case )

  return all_cases

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.fixture( params = _cases() )
def _case( request ):
  return request.param


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_eval_pjc( _case ):

  print( _case )

  exc, schema, cls, src, val = _case

  if exc == NoError:
    ctx = NoRaise()
  else:
    ctx = pytest.raises( exc )

  with ctx:

    f = schema( src )

    print(type(f))
    print(f)

    assert is_evaluated( f ) or is_valued_type( f )
    assert not is_valued( f )

    assert is_evaluated( f ) or isinstance( f, cls )
    assert f._schema is schema.schema


    x = f._eval()

    print( type(x) )
    print(x)


    assert is_valued_type( x )
    assert is_valued( x )

    assert isinstance( x, cls )
    assert x._schema is schema.schema


    assert x == val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_eval_cmp():
  p = BoolPrim(
    evaluated = PyEvaluated )

  v1 = p('$expr:py x')
  v2 = p('$expr:py x')

  assert v1 == v2
  assert v1 == '$expr:py x'
  assert v1 != '$expr:py y'

  assert v1 != False

  p = IntPrim(
    evaluated = PyEvaluated )

  v1 = p('$expr:py x')
  v2 = p('$expr:py x')

  assert v1 == v2
  assert v1 == '$expr:py x'
  assert v1 != '$expr:py y'

  assert v1 != 0

  p = FloatPrim(
    evaluated = PyEvaluated )

  v1 = p('$expr:py x')
  v2 = p('$expr:py x')

  assert v1 == v2
  assert v1 == '$expr:py x'
  assert v1 != '$expr:py y'

  assert v1 != 0.0

  p = StrPrim(
    evaluated = PyEvaluated )

  v1 = p('$expr:py x')
  v2 = p('$expr:py x')

  assert v1 == v2
  assert v1 == '$expr:py x'
  assert v1 != '$expr:py y'

  assert v1 != ''

  p = MapPrim(
    evaluated = PyEvaluated,
    item = BoolPrim(
      evaluated = PyEvaluated ) )

  v1 = p('$expr:py x')
  v2 = p('$expr:py x')

  assert v1 == v2
  assert v1 == '$expr:py x'
  assert v1 != '$expr:py y'

  assert v1 != {}

  v1 = p({'a' : '$expr:py x'})
  v2 = p({'a' : '$expr:py x'})

  assert v1 == v2
  assert v1 == {'a' : '$expr:py x'}
  assert v1 != {'a' : '$expr:py y'}

  p = SeqPrim(
    evaluated = PyEvaluated,
    item = BoolPrim(
      evaluated = PyEvaluated ) )

  v1 = p('$expr:py x')
  v2 = p('$expr:py x')

  assert v1 == v2
  assert v1 == '$expr:py x'
  assert v1 != '$expr:py y'

  assert v1 != []

  v1 = p(['$expr:py x'])
  v2 = p(['$expr:py x'])

  assert v1 == v2
  assert v1 == ['$expr:py x']
  assert v1 != ['$expr:py y']

  class MyType2( StructValued ):
    schema = dict(
      tag = 'my_type',
      evaluated = PyEvaluated,
      default_val = derived )

    a = BoolPrim(
      evaluated = PyEvaluated,
      default_val = True )

  v1 = MyType2('$expr:py x')
  v2 = MyType2('$expr:py x')

  assert v1 == v2
  assert v1 == '$expr:py x'
  assert v1 != '$expr:py y'

  assert v1 != MyType2.schema.default_val

  v1 = MyType2(a = '$expr:py x')
  v2 = MyType2(a = '$expr:py x')

  assert v1 == v2
  assert v1 == {'type': 'my_type', 'a' : '$expr:py x'}
  assert v1 != {'type': 'my_type', 'a' : '$expr:py y'}

  v1['a'] = '$expr:py y'
  assert v1 == {'type': 'my_type', 'a' : '$expr:py y'}

  assert v1 != MyType2.schema.default_val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == '__main__':
  test_eval_cmp()
