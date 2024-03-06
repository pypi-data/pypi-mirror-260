
from copy import copy
import io
import re
import uuid
import inspect
import sys

from abc import ABCMeta
import warnings

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  cached_property,
  adict,
  odict,
  rdict,
  rlist,
  StringFunction,
  mapping_attrs,
  protected_attr,
  indent_lines,
  split_lines,
  fmt_obj,
  fmt_base_or_type,
  _fmt_class_name,
  fmt_class_name,
  fmt_attr_doc,
  make_dynamic_class_name )

from partis.pyproj import (
  hash_sha256 )

from partis.utils.special import (
  required,
  optional,
  derived )

from .base import (
  schema_errors,
  SchemaError,
  SchemaNameError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaHint,
  Loc,
  PresetValue,
  assert_valid_name,
  assert_valid_path,
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
  is_evaluated_class,
  is_evaluated,
  is_valued,
  is_valued_type,
  any_schema )

from .property import (
  SchemaProperty,
  ConstProperty )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def fmt_schema_typename( obj, fmt = _fmt_class_name ):

  if isinstance( obj, SchemaDeclared ):
    obj = obj.schema

  if isinstance( obj, Schema ):
    if isinstance( obj.valued_type, SchemaProxy ):
      obj = obj.valued_type

  if isinstance( obj, SchemaProxy ):
    return fmt(obj)

  elif isinstance( obj, Schema ):
    return f"{fmt(obj.valued_type)} [ {fmt(obj)} ]"

  return obj

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def PassValued(
  val = None,
  schema = None,
  loc = None ):
  """Dummy function that simply returns the original un-modified value

  Note
  ----
  This technically not related to the 'Valued' classes, but provides for the
  ability to 'pass-through' a value using a similar call signature as the 'Valued'
  classes.
  """

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaRef( ABCMeta ):
  """Base class of all schema-like class types (is or uses a schema)
  """

  #-----------------------------------------------------------------------------
  @property
  def schema( cls ):
    """:class:`SchemaDep <partis.schema_meta.schema.SchemaDep>` : The defined schema.
    """
    raise NotImplementedError(f"Not implemented by {cls}")

  #-----------------------------------------------------------------------------
  @property
  def schema_defined( cls ):
    """bool: True if the schema has been defined for this reference.
    """

    raise NotImplementedError(f"Not implemented by {cls}")

  #-----------------------------------------------------------------------------
  def subclass( cls,
    name = None,
    module = None,
    module_set = None,
    **kwargs ):
    """Generator function for sub-classing the schema class

    Parameters
    ----------
    name : NoneType | str
      Name of subclass.
      If None, will generate a name automatically.
    module : None | str | ModuleType
      Module to use for the subclass.
      If None, the module will be determined from the caller frame.
      If a string, the module must be importable.
    module_set : None | bool
      If True (or None), adds the subclass to the module `module`.
      If False, the return value will be the only reference to the subclass.
    **kwargs :
      Keyword arguments passed to `__new__` and `__init__` of
      :class:`SchemaMeta <partis.schema_meta.schema.SchemaMeta>`.

    Returns
    -------
    subclass : :class:`SchemaMeta <partis.schema_meta.schema.SchemaMeta>`
      New subclass with the current class as the only base class.
    """

    module, name = make_dynamic_class_name(
      default_name = cls.__name__,
      module = module,
      name = name )

    bases = ( cls, )

    namespace = type(cls).__prepare__(
      name,
      bases,
      **kwargs )

    namespace['__module__'] = module.__name__

    sub_cls = type(cls)(
      name,
      bases,
      namespace,
      **kwargs )

    if module_set is None or module_set:

      if hasattr( module, sub_cls.__name__ ):
        warnings.warn(f"Overriding module attribute with class definition: {module}, {sub_cls.__name__}")

      setattr( module, sub_cls.__name__, sub_cls )


    return sub_cls


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaProxy( SchemaRef ):
  """Base class for types that use a schema, by is not itself a schema

  Parameters
  ----------
  name : str
    Class name of type
  bases : list[type]
    Base classes of type
  namespace : dict[str, object]
    Type namespace (class body)
  schema : :class:`SchemaDep <partis.schema_meta.schema.SchemaDep>`
    The defined schema.
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    schema ):

    if schema and not isinstance( schema, SchemaDep ):
      raise SchemaError(
        f"Schema proxy must be a SchemaDep.")


    namespace = {
      **namespace,
      '_p_schema': schema,
      # NOTE: generates docstring on-demand using _get_doc
      '__doc__' : StringFunction() }

    cls = super().__new__(
      mcls,
      name,
      bases,
      namespace )

    cls.__doc__._func = cls._get_doc

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    schema ):

    super().__init__( name, bases, namespace )

  #-----------------------------------------------------------------------------
  def _get_doc( cls,
    noindex = False,
    depth = 0,
    max_depth = 2 ):
    """Internal method to generate the docstring for the class

    Note
    ----
    The normal `__doc__` attribute should be used to access the generated
    docstring, which caches the result of this method.

    Parameters
    ----------
    noindex : bool
      Whether to add the attribute references to the doc index.

      Used with recursivly including schema docstrings in-place, preventing
      multiple index references to the same attribute, or for keeping the doc
      of 'class' attributes from clashing with any 'instance' attributes with
      the same name in the index.

      .. note::

        Even when True, the docstring will still be included in the generation
        of the documentation, but it won't be referencable.

    depth : int
      Current depth of recursively included docstrings
    max_depth : int
      Maximum depth to recursively included docstrings of related schema classes

    Returns
    -------
    str
    """

    return cls.schema._get_doc(
      noindex = True,
      depth = depth,
      max_depth = max_depth )

  #-----------------------------------------------------------------------------
  @property
  def schema( cls ):
    return cls._p_schema

  #-----------------------------------------------------------------------------
  @property
  def schema_defined( cls ):
    return cls._p_schema.schema_defined

  #-----------------------------------------------------------------------------
  def schema_resolvable( cls, checking = None ):
    return cls._p_schema.schema_resolvable(checking = checking)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDep( SchemaRef ):
  """Base class of concrete schema types

  Parameters
  ----------
  name : str
    Class name of type
  bases : list[type]
    Base classes of type
  namespace : dict[str, object]
    Type namespace (class body)
  schema_deps : None | list[ :class:`SchemaRef <partis.schema_meta.schema.SchemaRef>` ]
    Other schemas which this schema depends upon to be defined.
  schema_refs : None | list[ :class:`SchemaRef <partis.schema_meta.schema.SchemaRef>` ]
    Other schemas which depend on (defined with) this schema.
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    schema_deps = None,
    schema_refs = None ):

    if schema_deps is None:
      schema_deps = list()

    if schema_refs is None:
      schema_refs = list()

    if not all( isinstance(schema, SchemaRef) for schema in schema_deps ):
      raise SchemaDeclaredError(
        f"`schema_deps` must be list of SchemaRef: {schema_deps}")

    if not all( isinstance(schema, SchemaRef) for schema in schema_refs ):
      raise SchemaDeclaredError(
        f"`schema_refs` must be list of SchemaRef: {schema_refs}")

    namespace = {
      **namespace,
      '_p_schema_resolved' : False,
      # all dependencies of this schema
      '_p_schema_deps' : schema_deps,
      # schemas referencing this schema as a dependency
      '_p_schema_refs' : schema_refs }

    cls = super().__new__( mcls, name, bases, namespace )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    schema_deps = None,
    schema_refs = None ):

    super().__init__( name, bases, namespace )

  #-----------------------------------------------------------------------------
  @property
  def schema_defined( cls ):
    return cls._p_schema_resolved and len(cls._p_schema_deps) == 0

  #-----------------------------------------------------------------------------
  def schema_depends( cls, schema ):
    """Reference another schema having this schema as a dependency

    Parameters
    ----------
    schema : :class:`SchemaDep <partis.schema_meta.schema.SchemaDep`
    """
    if schema not in cls._p_schema_refs:
      cls._p_schema_refs.append( schema )

    if cls.schema_defined:
      schema.schema_resolved( cls )

  #-----------------------------------------------------------------------------
  def _schema_resolved( cls ):
    """Internal method called once all dependencies have been resolved.
    """
    raise NotImplementedError(f"Not implemented by {cls}")

  #-----------------------------------------------------------------------------
  def schema_resolved( cls, schema = None ):
    """Schema previously referenced as a dependency has been resolved

    Parameters
    ----------
    schema : :class:`SchemaRef <partis.schema_meta.schema.SchemaRef`
    """

    if cls._p_schema_resolved:
      return True

    if schema:
      if schema in cls._p_schema_deps:
        cls._p_schema_deps.remove( schema )

      if schema.schema in cls._p_schema_deps:
        cls._p_schema_deps.remove( schema.schema )

    if not cls.schema_resolvable():
      # still at least one un-resolved dependency
      return False

    # fully resolved
    cls._p_schema_resolved = True

    with schema_errors(
      msg = f"Resolution failed: {cls.__module__}.{cls.__name__}",
      loc = cls.loc if hasattr(cls, 'loc') else None,
      cls = SchemaDefinitionError ):

      cls._schema_resolved()

    refs = cls._p_schema_refs
    cls._p_schema_refs = list()

    for schema in refs:
      # signal schemas referencing this schema that it is now defined
      schema.schema_resolved( cls )


    return True

  #-----------------------------------------------------------------------------
  def schema_resolvable( cls, checking = None ):
    """Schema previously referenced as a dependency has been resolved

    Parameters
    ----------
    schema : :class:`SchemaRef <partis.schema_meta.schema.SchemaRef`
    """
    if checking is None:
      checking = list()

    if cls.schema in checking:
      return True

    checking.append(cls.schema)

    for _schema in cls._p_schema_deps:
      if not _schema.schema_resolvable( checking = checking ):
        return False

    return True

  #-----------------------------------------------------------------------------
  def _schema_hash_node( cls ):
    """Internal method to format the hashes of the class state contributing
    to the hash of the schema, **not** including the relative
    'connections' to other schemas.

    .. note::

      Each line may be formatted in any manner that uniquely identifies the
      *relevant* state of the schema as it relates to validating data.

    Returns
    -------
    list[str]

    See Also
    --------
    * :meth:`schema_hash_node`
    """

    return list()

  #-----------------------------------------------------------------------------
  @cached_property
  def schema_hash_node( cls ):
    """urlsafe Base64 encoded hash of this schema, **not** including connections
    (dependencies) to other schemas.

    .. note::

      The hash might not include all state information of the object, such as
      documentation or other data that might be used for informing user
      interfaces.
      The intention is the hash only identifies unique data **structure**.

    Returns
    -------
    str
    """

    return hash_sha256(
      '\n'.join( cls._schema_hash_node() ).encode('utf-8') )[0]

  #-----------------------------------------------------------------------------
  def _schema_hash_children( cls ):
    """Internal method to get the connected 'child' schema classes that
    contribute to the hash of the  schema.

    See Also
    --------
    * :meth:`schema_hash`

    Returns
    -------
    list[ :class:`SchemaRef <partis.schema_meta.schema.SchemaRef` ]
    """
    return list()

  #-----------------------------------------------------------------------------
  def _schema_hash( cls, visited = None ):
    """Internal method to format all connections that contribute to the hash of
    the  schema.

    The algorithm is generalized to handle reference cycles by enumerating all
    recursively referenced schemas in a **depth-first order** with no repeats.
    Each line is formatted as:

      `[node index], [hash of node], [list of child node indices]`

    For example, a hash starting at an arbitrary node marked as ``node(0)`` that
    includes a dependency cycle:

    .. code-block::

          0------<------
          |            |
      --<--->--        |
      |       |        |
      1       3        |
      |       |        |
      2   --<--->--    |
          |       |    |
          4       5-->--

    .. code-block::

      2, hash(node(2)), []
      1, hash(node(1)), [2]
      4, hash(node(4)), []
      5, hash(node(5)), [0]
      3, hash(node(3)), [4, 5]
      0, hash(node(0)), [1, 3]


    Parameters
    ----------
    visited : None | list[ :class:`SchemaRef <partis.schema_meta.schema.SchemaRef` ]
      Internally tracks the schema classes that have already been visited in
      a depth-first search

      .. note::

        This list will be updated by the method call with all nodes visited that
        where not initially in the list.

    Returns
    -------
    list[str]

    See Also
    --------
    * :meth:`schema_hash`

    Note
    ----
    The hash is only of the relative sub-graph starting at the schema the
    method is initially called on, and not necessarily of the entire graph of
    all schemas.

    Note
    ----
    The `schema_hash` attribute should be used to access the generated
    hash.

    :meta public:
    """

    if visited is None:
      visited = list()

    lines = list()

    if cls in visited:
      # base case where a cycle exists
      return lines

    visited.append( cls )

    idx = len(visited) - 1

    edges = list()

    for v in cls._schema_hash_children():

      lines.extend( v.schema._schema_hash( visited = visited ) )

      edges.append( visited.index( v.schema ) )

    # this node defined by its visit index, hash of non-connecting data, and
    # the indices of the nodes of outgoing connections
    lines.append( f'{idx}, {cls.schema_hash_node}, {edges}' )

    return lines

  #-----------------------------------------------------------------------------
  @cached_property
  def schema_hash( cls ):
    """urlsafe Base64 encoded hash of this schema, **including** connections
    to other schemas.

    The ``schema_hash`` is computed to be unique to the combination of all
    'relevent' attributes and relative connections between this schema and all
    other referenced schemas.
    The algorithm is generalized to handle reference cycles by enumerating all
    recursively referenced schemas in a depth-first order.

    Returns
    -------
    str

    """

    return hash_sha256(
      '\n'.join( cls._schema_hash() ).encode('utf-8') )[0]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaDeclared( SchemaDep ):
  """Base class for all schema forward declarations

  A schema declared acts as a forward declaration of a schema class, where
  a reference to the schema is needed before the schema class has actually been
  defined.
  A declared may only be defined by a *single* eventual schema class.

  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    schema_deps = None,
    schema_refs = None ):

    namespace = {
      **namespace,
      '_p_schema': None }

    cls = super().__new__( mcls,
      name,
      bases,
      namespace,
      schema_deps = schema_deps,
      schema_refs = schema_refs )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    schema_deps = None,
    schema_refs = None ):

    super().__init__( name, bases, namespace )

  #-----------------------------------------------------------------------------
  @property
  def schema( cls ):

    if not cls._p_schema:
      raise SchemaDeclaredError(
        f"Schema declared but not defined: {cls}")

    return cls._p_schema

  #-----------------------------------------------------------------------------
  @property
  def schema_defined( cls ):
    return cls._p_schema and super().schema_defined and cls._p_schema.schema_defined

  #-----------------------------------------------------------------------------
  def schema_resolvable( cls, checking = None ):
    return (
      cls._p_schema is not None
      and cls._p_schema.schema_resolvable(checking = checking) )

  #-----------------------------------------------------------------------------
  def _schema_resolved( cls ):
    cls.schema._schema_resolved()

  #-----------------------------------------------------------------------------
  def _schema_declared( cls, schema ):
    """Internal method for validating when a schema is to be defined

    Parameters
    ----------

    Returns
    """

    if cls._p_schema:
      raise SchemaDeclaredError(
        f"Schema already defined")

    if not is_schema( schema ):
      raise SchemaDeclaredError(
        f"Schema declared must be defined with a schema class: {fmt_base_or_type(schema)}")

    schema = schema.schema

    if not isinstance(schema, SchemaDep):
      raise SchemaDeclaredError(
        f"Schema declared must be defined with a schema class: {fmt_base_or_type(schema)}")

    return schema

  #-----------------------------------------------------------------------------
  def schema_declared( cls, schema ):
    """Defines the schema for this schema declared.

    .. note::

      This method should return the concrete schema, for example if the provided
      is a reference to the actual schema to be used to define it, since
      the declared must act as the reference to the concrete schema and not another
      reference.

    Parameters
    ----------
    schema : :class:`SchemaRef <partis.schema_meta.schema.SchemaRef`

    Returns
    -------
    :class:`SchemaDep <partis.schema_meta.schema.SchemaDep`
    """

    schema = cls._schema_declared( schema )

    cls._p_schema = schema

    cls._p_schema_deps.append( cls._p_schema )
    cls._p_schema.schema_depends( cls )

  #-----------------------------------------------------------------------------
  def _get_doc( cls,
    noindex = False,
    depth = 0,
    max_depth = 2 ):

    return cls.schema._get_doc(
      noindex = True,
      depth = depth,
      max_depth = max_depth )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Schema( SchemaDep ):
  """Base class for all schemas

  Parameters
  ----------
  name : str
    Class name of type
  bases : list[type]
    Base classes of type
  namespace : dict[str, object]
  evaluated : None | :class:`Evaluated <partis.schema.eval.Evaluated>`
    Class capable to transforming raw source data (such as Python expressions)
    into the appropriate data type.
    The `val` is checked using `evaluated.check`.
    If it cannot be interpreted as an expression, the value is validated as is.
    If not specified, then source data will not be considered as an expression.
  default_val : None | :class:`OptionalType <partis.utils.special.OptionalType>` | :class:`RequiredType <partis.utils.special.RequiredType>` | :class:`DerivedType <partis.utils.special.DerivedType>` | object
    The default `val` (value) of this schema in the case of missing source data.
    A default of `None` (or `OptionalType`) means the value is optional and will
    be None if source data is missing.
    A default of :class:`RequiredType <partis.utils.special.RequiredType>`
    means the value is required in the source data and
    will raise a :class:`SchemaValidationError <partis.schema_meta.base.SchemaValidationError>`
    if value is missing.
    A default of :class:`DerivedType <partis.utils.special.DerivedType>`
    will attempt to construct a default value from the
    default values of the `struct` items, but will raise a
    :class:`SchemaDefinitionError <partis.schema_meta.base.SchemaDefinitionError>`
    if any items themselves have required values.
    Otherwise, items will be validated against the primitve schema.
  default_eval: :class:`RequiredType <partis.utils.special.RequiredType>` | object
    The default value to use if an evaluated expression results in `None`.
    The purpose of this value is that the `default_val` itself may be an expression
    that could return None, which would reference back to the `default_val` causing
    an un-resolvable loop.
    If that would occur, then this value will be used as the result of the expression
    instead of the `default_val` expression.
    If `default_val` is anything other than an expression, specifying this will raise
    an error to ensure a single source of truth for the resulting value.
  init_val : None | object
    The initial value that is used when creating an editable template for the value.
    This differs from `default_val` in that this value is *not* used to fill in
    any missing source data.
    If `None`, `default_val` will be used, or a value will be derived
    from the schema to produce an initial value that will pass validation.
    However, `init_val` may specified independently from `default_val`.
  preset_vals : None | list[ :class: `PresetValue <partis.schema_meta.base.PresetValue>`]
  schema_deps : None | list[ :class:`SchemaRef <partis.schema_meta.schema.SchemaRef>` ]
    Other schemas which this schema depends upon to be defined.
  schema_refs : None | list[ :class:`SchemaRef <partis.schema_meta.schema.SchemaRef>` ]
    Other schemas which depend on (defined with) this schema.
  valued_type : None | type
    The type used to instantiate values that have been validated ('decoded')
    by this schema.
    This may be initially undefined, by the schema will not be defined/resolved
    until it is set using the ``valued_type`` setter.
  doc : None | str
    Description of this schema
  loc : None | :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)

  Raises
  ------
  SchemaDefinitionError
    If the schema definition is not valid

  """


  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    evaluated = None,
    default_val = None,
    default_eval = None,
    init_val = None,
    preset_vals = None,
    schema_deps = None,
    schema_refs = None,
    valued_type = None,
    doc = None,
    loc = None ):


    if default_val is None:
      default_val = required

    if any(
      check( default_val )
      for check in [
        is_valued_type,
        is_evaluated ] ):

      default_val = default_val._encode

    if is_special( default_val ):

      if not any(
        check( default_val )
        for check in [
          is_required,
          is_optional,
          is_derived ] ):

        raise SchemaDefinitionError(
          f"`default_val` special values may only be `optional`, `required`, or `derived`: {default_val}",
          loc = loc )

    if evaluated is None:
      from partis.schema.eval import NotEvaluated
      evaluated = NotEvaluated

    if not is_evaluated_class( evaluated ):
      raise SchemaDefinitionError(
        f"`evaluated` must be subclass of `Evaluated`: {fmt_base_or_type(evaluated)}",
        loc = loc )


    if default_eval is None:
      default_eval = required

    if any(
      check( default_eval )
      for check in [
        is_valued_type,
        is_evaluated ] ):

      default_eval = default_eval._encode

    if not is_required( default_eval ):

      if not evaluated.check( default_val ):
        raise SchemaDefinitionError(
          f"`default_eval` not needed if `default_val` is not an expression: {default_eval}, {default_val}",
          loc = loc )

      if is_optional( default_eval ):
        raise SchemaDefinitionError(
          f"`default_eval` may not be an `OptionalType`: {default_eval}",
          loc = loc )

      if evaluated.check( default_eval ):
        raise SchemaDefinitionError(
          f"`default_eval` may not be an expression: {default_eval}",
          loc = loc )

    if any(
      check( init_val )
      for check in [
        is_valued_type,
        is_evaluated ] ):

      init_val = init_val._encode

    if is_special( init_val ):
      raise SchemaDefinitionError(
        f"`init_val` may not be a special value: {init_val}",
        loc = loc )

    if preset_vals is None:
      preset_vals = list()

    if not isinstance(preset_vals, list):
      raise SchemaDefinitionError(
        f"`preset_vals` must be a list: {preset_vals}",
        loc = loc )

    preset_vals = copy(preset_vals)

    for i,v in enumerate(preset_vals):
      if not isinstance(v, PresetValue):
        preset_vals[i] = PresetValue(v)

    if valued_type is not None:
      if not isinstance( valued_type, type ):
        raise SchemaDefinitionError(
          f"`valued_type` must be a type: {valued_type}",
          loc = loc )

    # format docstring
    if doc is None:
      doc = ""
    else:
      doc = inspect.cleandoc( doc )


    if '__doc__' in namespace and namespace['__doc__']:
      _doc = inspect.cleandoc( str(namespace['__doc__']) )

      if doc:
        doc += '\n\n' + _doc
      else:
        doc = _doc

    if loc is None:
      loc = Loc()

    namespace = { **namespace, **dict(
      __doc__ = StringFunction(),
      _p_doc = doc,
      _p_evaluated = evaluated,
      _p_default_val = default_val,
      _p_default_eval = default_eval,
      _p_init_val = init_val,
      _p_preset_vals = preset_vals,
      _p_valued_type = valued_type,
      _p_loc = loc )}

    cls = super().__new__(
      mcls,
      name,
      bases,
      namespace,
      schema_deps = schema_deps,
      schema_refs = schema_refs )

    cls.__doc__._func = cls._get_doc

    if schema_deps:
      for schema in schema_deps:
        if schema:
          if isinstance( schema, SchemaDep ):
            schema.schema_depends( cls )

          elif isinstance( schema, SchemaProxy ):
            schema.schema.schema_depends( cls )

          else:
            raise SchemaDefinitionError(
              f"`schema_deps` must be SchemaDep or SchemaProxy: {schema}",
              loc = loc )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    evaluated = None,
    default_val = None,
    default_eval = None,
    init_val = None,
    schema_deps = None,
    schema_refs = None,
    valued_type = None,
    doc = None,
    loc = None ):

    super().__init__( name, bases, namespace )

    cls.schema_resolved()

  #-----------------------------------------------------------------------------
  @property
  def schema_defined( cls ):
    return cls.valued_type and super().schema_defined

  #-----------------------------------------------------------------------------
  @property
  def valued_type( cls ):
    return cls._p_valued_type

  #-----------------------------------------------------------------------------
  @valued_type.setter
  def valued_type( cls, valued_type ):

    if valued_type is None:
      return

    if cls._p_valued_type:
      raise SchemaDefinitionError(
        f"Schema valued type already defined: {cls._p_valued_type}",
        loc = cls.loc )

    if not isinstance( valued_type, type ):
      raise SchemaDefinitionError(
        f"`valued_type` must be a type: {valued_type}",
        loc = cls.loc )

    cls._p_valued_type = valued_type

    cls.schema_resolved()

  #-----------------------------------------------------------------------------
  def schema_resolvable( cls, checking = None ):
    return (
      cls.valued_type is not None
      and super().schema_resolvable(checking = checking) )

  #-----------------------------------------------------------------------------
  @property
  def doc( cls ):
    """str : Base documentation
    """
    return cls._p_doc

  #-----------------------------------------------------------------------------
  def _get_attr_doc_lines( cls,
    noindex = False,
    depth = 0,
    max_depth = 2 ):

    return list()

  #-----------------------------------------------------------------------------
  def _get_doc( cls,
    noindex = False,
    depth = 0,
    max_depth = 2 ):


    lines = [
      cls.doc,
      '', '' ]

    if isinstance( cls, Schema ) and cls.schema_defined and depth < max_depth:
      lines.extend( cls._get_attr_doc_lines(
        noindex = noindex,
        depth = depth,
        max_depth = max_depth ) )

    return "\n".join( lines )

  #-----------------------------------------------------------------------------
  @property
  def loc( cls ):
    return cls._p_loc

  #-----------------------------------------------------------------------------
  @property
  def schema( cls ):

    return cls

  #-----------------------------------------------------------------------------
  @property
  def hints( cls ):
    """list[ :class:`SchemaHint <partis.schema_meta.base.SchemaHint>` ] : Definition
    hints.
    """

    hints = [
      SchemaHint(
        f"doc: {cls.doc}" ) ]

    return hints

  #-----------------------------------------------------------------------------
  # def depends( cls, schema ):
  #
  #   if schema not in cls._p_schema_refs:
  #     cls._p_schema_refs.append( schema )
  #
  #   if cls.schema_defined:
  #     schema.resolve( cls )

  #-----------------------------------------------------------------------------
  def _schema_resolved( cls ):

    # fully resolved
    # test-run the generation of values
    for attr in [
      'default_val',
      'default_eval',
      'init_val']:

      with schema_errors(
        msg = f"{cls.__name__}.{attr} not valid",
        loc = cls.loc,
        cls = SchemaDefinitionError ):

        v = getattr( cls.schema, attr )

        if not (
          is_optional( v )
          or is_required( v ) ):

          cls.schema.decode( v, cls.loc )

    for i, preset in enumerate(cls.preset_vals):
      with schema_errors(
        msg = f"{cls.__name__}.preset_vals[{i}] not valid",
        loc = cls.loc,
        cls = SchemaDefinitionError ):

        cls.schema.decode( preset.val, cls.loc )

  #-----------------------------------------------------------------------------
  @property
  def default_val( cls ):
    """object: default value
    """
    return cls._p_default_val

  #-----------------------------------------------------------------------------
  @property
  def default_eval( cls ):
    """object : default value used when the default value is itself an expression
    that returns nothing.
    """
    return cls._p_default_eval

  #-----------------------------------------------------------------------------
  @property
  def init_val( cls ):
    """object : initial value used, even when there is no default value
    """
    return cls._p_init_val

  #-----------------------------------------------------------------------------
  @property
  def preset_vals( cls ):
    """object : preset values that may be used
    """
    return cls._p_preset_vals

  #-----------------------------------------------------------------------------
  @property
  def evaluated( cls ):
    """:class:`Evaluated <partis.schema.eval.Evaluated>` : Evaluation class
    """
    return cls._p_evaluated
