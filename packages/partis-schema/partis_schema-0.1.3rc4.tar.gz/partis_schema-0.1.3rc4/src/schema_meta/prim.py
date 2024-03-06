
from copy import copy

import re
import uuid
import sys

from abc import ABCMeta


import logging
log = logging.getLogger(__name__)

from partis.utils import (
  adict,
  odict,
  rdict,
  rlist,
  StringFunction,
  mapping_attrs,
  protected_attr,
  indent_lines,
  fmt_base_or_type,
  fmt_class_name,
  make_dynamic_class_name )


from .base import (
  SchemaError,
  SchemaNameError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaHint,
  Loc,
  assert_valid_name,
  assert_valid_path,
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
  any_schema )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaPrimMeta( type ):
  """Meta-class for schema primitives

  .. note::

    The primary purpose of this metaclass is to instantiate primitive schema
    types without the typical class bodies, and providing convenience to generating
    class names.
  """

  #-----------------------------------------------------------------------------
  def __call__( pcls,
    name = None,
    module = None,
    module_set = None,
    doc = None,
    **kwargs ):
    """Creates a new primitive schema class of the primitive meta type

    Parameters
    ----------
    name : str
      Name of sub-class. If not given, a name will be generated automatically
    module : None | str | ModuleType
      Module to use for the subclass.
      If None, the module will be determined from the caller frame.
      If a string, the module must be importable.
    module_set : None | bool
      If True (or None), adds the subclass to the module `module`.
      If False, the return value will be the only reference to the subclass.
    **kwargs :
      Arguments passed to the class __new__ and __init__

    Note
    ----
    This modifies the call signature using the prim class as a generator function
    """


    module, name = make_dynamic_class_name(
      default_name = pcls.__name__,
      module = module,
      name = name )

    bases = tuple()

    namespace = pcls.__prepare__(
      name,
      bases,
      **kwargs )

    namespace['__module__'] = module.__name__

    namespace['__doc__'] = doc

    cls = super().__call__(
      # pcls,
      name,
      bases,
      namespace,
      **kwargs )

    if module_set is None or module_set:

      if hasattr( module, cls.__name__ ):
        log.warning(f"Overriding module attribute with class definition: {cls.__name__}")

      setattr( module, cls.__name__, cls )

    return cls
