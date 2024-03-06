
import pytest
import sys
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
  is_similar_value_type,
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
  PJCEvaluated,
  PassPrim,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  SchemaStruct,
  EvalFunc )

from partis.schema.valued.valued import (
  Valued)

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

  base_types = [
    ( BoolPrim(), BoolValued, [ False, True ] ),
    ( IntPrim(), IntValued, [ -3, -1, 0, 1, 100 ] ),
    ( FloatPrim(), FloatValued, [ -100.1, -3, -1, -3 / 100, 0, 1, 100, 100.1  ] ),
    ( StrPrim(), StrValued, [ 'a', '1', 'True', '0', 'False'  ] ) ]

  all_types = list()

  for type in base_types:
    schema, cls, vals = type

    all_types.append( type )

    all_types.append(
      ( SeqPrim( item = schema ), SeqValued, [ vals, ] ) )

    keys = [
      (chr( 65 + (i % 26) ) + chr( 65 + ((i//26) % 26) ))
      for i in range(len(vals)) ]

    val = dict(list( zip(keys,vals) ))

    all_types.append(
      ( MapPrim( item = schema ), MapValued, [ val, ] ) )

  should_pass_cases = list()
  should_fail_cases = list()

  for type in all_types:
    schema, cls, vals = type

    for val in vals:
      should_pass_cases.append(
        ( NoError, schema, cls, val, val ) )

      # use closure to create evaluable function
      def _f(val):
        def _g( _ ):
          return val

        return _g

      func = _f(val)

      evaluated = PJCEvaluated(
        schema = schema,
        src = EvalFunc( func = func ) )

      should_pass_cases.append(
        ( NoError, schema, cls, evaluated, val ) )

      # src = ( lambda val: (lambda *args, **kwargs: val) )(None)
      #
      # should_fail_cases.append(
      #   ( SchemaEvaluationError, schema, cls, evaluated, val ) )

  all_cases = should_pass_cases + should_fail_cases


  return all_cases

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@pytest.fixture( params = _cases() )
def _case( request ):
  return request.param


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def test_valued( _case):

  
  #print( _case )

  exc, schema, cls, input, val = _case

  loc = Loc()

  if exc == NoError:
    ctx = NoRaise()
  else:
    ctx = pytest.raises( exc )

  with ctx:
    x = cls(
      val = input,
      schema = schema,
      loc = loc )

    #print( x._src is input )

    assert is_similar_value_type( x, val )
    assert x._src is input
    assert ( loc is None and isinstance( x._loc, Loc ) ) or x._loc is loc
    assert ( schema is None and isinstance(x._schema, PassPrim) ) or ( x._schema is schema )
    assert ( not is_valued( input ) ) or x == input
    assert is_valued( input ) == is_valued( x )

    _x = x._eval( context = { '_' : None } )

    assert is_similar_value_type( _x, val )
    assert is_valued( _x )
    assert _x == val
    assert _x._loc is x._loc
    assert _x._schema is x._schema

    y = cls( x )

    #print( y._src is input )
    #print( y._src is x )

    assert is_similar_value_type( y, val )
    assert y._src is input
    assert y._loc is x._loc
    assert y._schema is x._schema
    assert is_valued( y ) == is_valued( x )

    _y = y._eval( context = { '_' : None } )

    assert is_similar_value_type( _y, val )
    assert is_valued( _y )
    assert _y == val
    assert _y._loc is y._loc
    assert _y._schema is y._schema


def test_model_hint(_case):
  exc, schema, cls, input, val = _case

  loc = Loc()

  if exc == NoError:
    ctx = NoRaise()
  else:
    ctx = pytest.raises( exc )

  with ctx:
    x = cls(
      val = input,
      schema = schema,
      loc = loc )

    h = x.model_hint()
    assert type(h).__name__ == "ModelHint"