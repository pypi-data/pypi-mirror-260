import re
import inspect
from fnmatch import (
  translate )
import logging
log = logging.getLogger(__name__)

from math import log2
from collections.abc import (
  Mapping,
  Sequence )

from numbers import (
  Number,
  Complex,
  Real,
  Integral )

from rich.text import Text

from ruamel.yaml.comments import (
  CommentedBase,
  CommentedMap,
  CommentedSeq )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from partis.utils.special import (
  SpecialType,
  RequiredType,
  OptionalType,
  DerivedType,
  NotSetType )

from partis.utils import (
  fmt_obj,
  hint_level_num,
  Loc,
  ModelHint,
  ModelError )

from partis.utils.inspect import (
  _filter_traceback )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import partis

LOG_TRACE = hint_level_num('trace')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
name_re = r"^[a-zA-Z\_][a-zA-Z\_0-9]*$"
name_cre = re.compile( name_re )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaError( ModelError ):
  """Base of all schema related errors
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaNameError( SchemaError ):
  """Raised when a name error occurs
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaParseError( SchemaError ):
  """Raised when a schema cannot be detected
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDetectionError( SchemaError ):
  """Raised when a schema cannot be detected
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDeclaredError( SchemaError ):
  """Raised when a schema's declared is used before the schema has been defined
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDefinitionError( SchemaError ):
  """Raised when a schema's definition is not correctly specified
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaValidationError( SchemaError ):
  """Raised when data could not be validated (encoded/decoded) using schema definition
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaEvaluationError( SchemaError ):
  """Raised when evaluated expression failed to result in a decoded value
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaHint( ModelHint ):
  """Base of all schema hints
  """
  pass


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Bias:
  """A metric of how biased (selective) a value is to a schema

  This may be interpreted as the number of needed independent binary decisions
  (questions, or conditional statements) to determine that the value satisfied
  the schema.

  Parameters
  ----------
  val : None | float
    The current/initial bias value
  const :  None | bool
    If ``True``, the bias value is considered to be a constant.

  """
  #-----------------------------------------------------------------------------
  def __init__(self, val = None, const = None ):
    if val is None:
      val = 0.0

    if isinstance(val, Bias):
      if const is None:
        const = val._const

      val = val._val

    self._const = const
    self._val = val

  #-----------------------------------------------------------------------------
  def __float__(self):
    return float(self._val)

  #-----------------------------------------------------------------------------
  def __add__(self, s):
    val = self._val

    if not self._const:
      val += float(s)

    return Bias(val, self._const)

  #-----------------------------------------------------------------------------
  def __iadd__(self, s):
    if not self._const:
      self._val += float(s)

    return self

  #-----------------------------------------------------------------------------
  def __str__(self):
    return str(float(self))

  #-----------------------------------------------------------------------------
  def __repr__(self):
    return f"{type(self).__name__}({float(self)})"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PresetValue:
  """A preset value associated with a schema

  Parameters
  ----------
  val : object
  label: None | str
  doc: None | str

  """
  #-----------------------------------------------------------------------------
  def __init__(self, val, label = None, doc = None ):
    if any(
      check( val )
      for check in [
        is_valued_type,
        is_evaluated ] ):

      val = val._encode

    if doc is None:
      doc = ""

    if label is None:
      label = fmt_obj(val, width = 10, height = 1)

    self._val = val
    self._label = label
    self._doc = doc

  #-----------------------------------------------------------------------------
  @property
  def val(self):
    return self._val

  #-----------------------------------------------------------------------------
  @property
  def label(self):
    return self._label

  #-----------------------------------------------------------------------------
  @property
  def doc(self):
    return self._doc

  #-----------------------------------------------------------------------------
  def __eq__(self, other):
    if isinstance(other, PresetValue):
      return self.val == other.val

    return self.val == other

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def assert_valid_name( name ):
  if not isinstance( name, str ):
    raise SchemaNameError(
      f"Name must be a string: {name}")

  match = name_cre.fullmatch(name)

  if match is None:
    raise SchemaNameError(
      f"Name must be only alpha-numeric or underscrores, and not start with a number: {name}")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def assert_valid_path( path ):

  if isinstance( path, str ):
    if path == '':
      # empty path is valid
      return

    path = path.split('.')

  if not isinstance( path, list ) and all( isinstance(p, str) for p in path ):
    raise SchemaNameError(
      f"Name path must be a string or list of strings: {path}")

  for i, name in enumerate(path):
    try:

      assert_valid_name( name )

    except SchemaNameError as e:
      raise SchemaNameError(
        f"Path name segment {i} not valid: {path}",
        hints = SchemaHint.cast( e ) ) from e


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_special( val ):
  return isinstance( val, SpecialType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_required( val ):
  """
  Returns
  -------
  bool
    True if the value corresponds to being required, likely resulting in
    an error if no value is supplied.
  """

  return isinstance( val, RequiredType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_optional( val ):
  """
  Returns
  -------
  bool
    True if the value corresponds to being optional, resulting in a default of None
  """
  return val is None or isinstance( val, OptionalType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_derived( val ):
  """
  Returns
  -------
  bool
    True if the value is to be derived from some other value(s)
  """
  return isinstance( val, DerivedType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_notset( val ):
  """
  Returns
  -------
  bool
    True if the value corresponds to being not set, or otherwise undefined,
    including not even ``None``.
  """

  return isinstance( val, NotSetType )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_bool( obj ):
  """Is a boolean value
  """
  import partis.schema

  if isinstance( obj, type ):
    return issubclass( obj, (bool, partis.schema.BoolValued) )

  return isinstance( obj, (bool, partis.schema.BoolValued) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_numeric( obj ):
  """Is a numeric value
  """

  if isinstance( obj, type ):
    return issubclass( obj, Number ) and not is_bool( obj )

  return isinstance( obj, Number ) and not is_bool( obj )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_string( obj ):
  """Is a string value
  """

  if isinstance( obj, type ):
    return issubclass( obj, (str, Text) )

  return isinstance( obj, (str, Text) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_sequence( obj ):
  """Is a sequence value, but not a string
  """
  if isinstance( obj, type ):
    return issubclass( obj, Sequence ) and not is_string( obj )

  return isinstance( obj, Sequence ) and not is_string( obj )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_mapping( obj ):
  """Is a mapping value
  """
  if isinstance( obj, type ):
    return issubclass( obj, Mapping )

  return isinstance( obj, Mapping )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
type_tests = [
  is_required,
  is_derived,
  is_optional,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_similar_value_type( a, b ):
  """
  Returns
  -------
  is_similar_value_type : bool
    True if all `type_tests` return the same for both values
  """
  return all( f(a) == f(b) for f in type_tests )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema( obj ):
  """Is a schema class or schema declared
  """
  return issubclass( type(obj), partis.schema_meta.schema.SchemaRef )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_prim( obj ):
  """Is a schema primitive type
  """
  return issubclass( type(type(obj)), partis.schema_meta.prim.SchemaPrimMeta )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_declared( obj ):
  """Is a schema class or schema declared type
  """
  return issubclass( type(obj), partis.schema_meta.schema.SchemaDeclared )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_struct( obj ):
  """Is a schema class or schema declared type
  """
  return (
    issubclass( type(obj), partis.schema_meta.struct.SchemaStruct )
    or issubclass( type(obj), partis.schema_meta.struct.SchemaStructDeclared )
    or issubclass( type(obj), partis.schema_meta.struct.SchemaStructProxy ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_schema_struct_valued( obj ):
  """Is an instance value of a schema class type
  """
  return (
    is_valued_type( obj )
    and is_schema_struct(obj._schema) )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_evaluated_class( val ):
  """Is an evaluated class type
  """
  return ( issubclass( type(val), partis.schema_meta.eval.EvaluatedMeta ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_provider( val ):
  """Is an evaluated type
  """
  return issubclass( type(type(val)), partis.schema_meta.eval.ProviderMeta )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_evaluated( val ):
  """Is an evaluated type
  """
  if is_valued_type(val):
    return is_evaluated(val._src)

  return issubclass( type(type(val)), partis.schema_meta.eval.EvaluatedMeta )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_valued_type( val ):
  """
  Returns
  -------
  is_valued_type : bool
    True if is an instance value of any schema type
  """
  return issubclass( type(type(val)), partis.schema_meta.valued.ValuedMeta )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def any_schema( val, schemas ):
  """Is the schema any of the list schemas

  Parameters
  ----------
  schema : object
    Schema to test
  schema : list[object]
    Schemas to compare to
  """
  if is_valued_type( val ):
    return any( val._schema is s.schema for s in schemas )

  elif is_schema( val ):
    return any( val.schema is s.schema for s in schemas )

  return False


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def is_valued( val ):
  """
  Returns
  -------
  is_valued : bool
    True if value is completely evaluated
  """

  if is_evaluated(val):
    return False

  if is_valued_type( val ):
    return val._valued

  if is_sequence( val ):
    return all( is_valued(v) for v in val )

  if is_mapping( val ):
    return all( is_valued(v) for v in val.values() )

  return True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_line_col(obj, key = None):

  if isinstance( obj, CommentedBase ):
    # NOTE: ruamel appears to store line/col in zero-based indexing
    if (
      key is None
      or not ( isinstance(obj, CommentedMap) or isinstance(obj, CommentedSeq) )
      or obj.lc.data is None
      or (isinstance(obj, CommentedMap) and key not in obj)
      or (isinstance(obj, CommentedSeq) and ( key < 0 or key >= len(obj) ) ) ):

      return obj.lc.line + 1, obj.lc.col + 1

    else:
      return obj.lc.data[key][0] + 1, obj.lc.data[key][1] + 1

  if obj is not None:
    try:
      return inspect.getsourcelines(obj)[1], None
    except:
      pass

  return None, None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class schema_errors:

  #-----------------------------------------------------------------------------
  def __init__(self,
    msg = None,
    data = None,
    loc = None,
    hints = None,
    schema = None,
    cls = None,
    filter = None,
    suppress = False ):

    if cls is None:
      cls = SchemaError

    if msg is None:
      msg = f"Error while validating"

    if hints is None:
      hints = list()

    if not isinstance(hints, list):
      hints = [hints]

    if schema is not None:
      if loc is None:
        loc = Loc( owner = schema )
      else:
        loc.owner = schema

    assert issubclass(cls, SchemaError)

    patterns = [r'*/site-packages/partis/*']
    patterns = [
      re.compile( translate(p) )
      for p in patterns ]

    def _ignore(fname):
      return any(p.match(fname) is not None for p in patterns)

    if filter is None:
      filter = (Exception,)
    elif not isinstance(filter, (list, tuple)):
      filter = (filter,)
    else:
      filter = tuple(filter)

    self._cls = cls
    self._ignore = _ignore
    self._filter = filter
    self._suppress = bool(suppress)

    self.msg = msg
    self.data = data
    self.loc = loc
    self.hints = hints

  #-----------------------------------------------------------------------------
  def __enter__(self):
    return self

  #-----------------------------------------------------------------------------
  def __exit__(self, cls, value, traceback):

    if cls is not None and issubclass(cls, self._filter):
      if not log.isEnabledFor(LOG_TRACE):
        _filter_traceback(
          traceback,
          self._ignore,
          keep_last = not (hasattr(value, 'ignore_frame') and value.ignore_frame))

      msg = self.msg

      raise self._cls(
        msg,
        data = self.data,
        loc = self.loc,
        hints = self.hints + [value],
        ignore_frame = True ) from None

    # do not handle any exceptions here
    return self._suppress
