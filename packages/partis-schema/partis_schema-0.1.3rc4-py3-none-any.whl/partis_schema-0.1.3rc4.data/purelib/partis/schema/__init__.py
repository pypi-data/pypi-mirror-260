"""Base elements for defining a data schema, including base types, data structures,
and data classes (:class:`SchemaStruct <partis.schema.struct.SchemaStruct>`)
"""

from partis.utils.special import (
  required,
  optional,
  derived,
  notset )

from .module import (
  SchemaLoader,
  SchemaFinder,
  SchemaModule )

from .eval import (
  ProviderSupport,
  ProviderMeta,
  Provider,
  EvaluatedMeta,
  Evaluated,
  NotEvaluated,
  EvaluatedContext,
  ConstEvaluatedContext,
  PyEvaluated,
  PyEvaluatedRestricted,
  CheetahEvaluated,
  PJCEvaluated,
  EvalFunc )

from .valued import (
  BoolValued,
  IntValued,
  FloatValued,
  StrValued,
  PathValued,
  SeqValued,
  MapValued,
  StructValued )

from .prim import (
  PassPrim,
  BoolPrimDeclared,
  BoolPrim,
  IntPrimDeclared,
  IntPrim,
  FloatPrimDeclared,
  FloatPrim,
  StrPrimDeclared,
  StrPrim,
  PathPrimDeclared,
  PathPrim,
  SeqPrimDeclared,
  SeqPrim,
  MapPrimDeclared,
  MapPrim,
  UnionPrimDeclared,
  UnionPrim )

from .declared import (
  schema_declared )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# import everything from `schema_meta` to have unified "external" imports
# NOTE: `schema_meta` is not meant to be exposed in the main package because it's
# designed to lazily import the `meta` components to avoid issues with circular
# imports while initializing the various modules.
from partis.schema_meta.base import (
  PresetValue,
  assert_valid_name,
  SchemaError,
  SchemaParseError,
  SchemaDetectionError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaEvaluationError,
  SchemaHint,
  Bias,
  Loc,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_special,
  is_optional,
  is_required,
  is_derived,
  is_similar_value_type,
  is_schema_prim,
  is_schema_declared,
  is_schema_struct,
  is_schema,
  is_schema_struct_valued,
  is_provider,
  is_evaluated_class,
  is_evaluated,
  is_valued,
  is_valued_type,
  any_schema )

from partis.schema_meta.valued import (
  ValuedMeta )

from partis.schema_meta.prim import (
  SchemaPrimMeta )

from partis.schema_meta.property import (
  SchemaProperty,
  ConstProperty )

from partis.schema_meta.schema import (
  PassValued,
  SchemaRef,
  SchemaProxy,
  SchemaDep,
  SchemaDeclared,
  Schema )

from partis.schema_meta.struct import (
  SchemaStructDeclared,
  SchemaStruct,
  SchemaStructProxy )

from . import serialize

# from .hint import (
#   Hint,
#   HintList )
