
from .base import SchemaPrim
from .pass_prim import PassPrim

from .bool_prim import (
  BoolPrimDeclared,
  BoolPrim )

from .int_prim import (
  IntPrimDeclared,
  IntPrim )

from .float_prim import (
  FloatPrimDeclared,
  FloatPrim )

from .str_prim import (
  StrPrimDeclared,
  StrPrim )

from .seq_prim import (
  SeqPrimDeclared,
  SeqPrim )

from .map_prim import (
  MapPrimDeclared,
  MapPrim )

from .union_prim import (
  UnionPrimDeclared,
  UnionPrim )


seq_declared = SeqPrimDeclared()
map_declared = MapPrimDeclared()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# bool|float|str|list|dict
any_prim_cases = [
    BoolPrim( default_val = False ),
    FloatPrim( default_val = 0.0 ),
    StrPrim( default_val = "" ),
    seq_declared,
    map_declared ]

AnyPrim = UnionPrim(
  cases = any_prim_cases,
  default_case = 0 )


SeqPrim(
  declared = seq_declared,
  item = AnyPrim,
  default_val = list() )

MapPrim(
  declared = map_declared,
  item = AnyPrim,
  default_val = dict() )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
