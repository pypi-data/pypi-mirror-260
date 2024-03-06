
__all__ = [
  "base",
  "eval",
  "prim",
  "property",
  "schema",
  "struct",
  "valued"  ]

import sys
from partis.utils.module import LazyModule

self = sys.modules[ __name__ ]
self.__class__ = LazyModule

self.define(
  children = __all__ )
