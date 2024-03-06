
from copy import copy
import io
import re
import uuid
import inspect
import sys
import importlib

from abc import ABCMeta
import warnings

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  cached_property,
  adict,
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
  derived,
  notset )

from partis.schema_meta.base import (
  schema_errors,
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
  is_special,
  is_optional,
  is_required,
  is_derived,
  is_notset,
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

from partis.schema_meta.property import (
  SchemaProperty,
  ConstProperty )

from .schema import (
  fmt_schema_typename,
  SchemaProxy,
  SchemaDeclared,
  Schema )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaStructDeclared( SchemaDeclared ):
  """Meta-class for all schema declareds

  A schema declared acts as a forward declaration of a schema class if a reference
  to the schema is needed before the schema class has actually been defined.
  The eventual schema definition must have the exact same `tag_key` and `tag`
  as the declared that it defines.
  Once it has been defined, the actual schema definition may be retrieved from the
  `schema` property.
  A declared may only be defined by a *single* eventual schema class.

  Parameters
  ----------
  name : str
    Class name of type
  bases : list[type]
    Base classes of type
  namespace : dict[str, object]
  tag_key : NoneType | str
    The key for the tag defining this schema.
    (default: 'type')
  tag : str
    The tag defining this schema
  See Also
  --------
  :class:`SchemaDeclared <partis.schema.declared.SchemaDeclared>`
  :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`

  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    tag,
    tag_key = None ):


    if tag_key is None:
      tag_key = 'type'

    try:
      assert_valid_name( tag_key )
      assert_valid_name( tag )

    except SchemaNameError as e:

      raise SchemaDeclaredError(
        f"Schema declared name not valid",
        hints = e ) from e

    namespace = {**namespace, **dict(
      _p_tag_key = tag_key,
      _p_tag = tag )}

    cls = super().__new__( mcls, name, bases, namespace )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    tag,
    tag_key = None ):

    super().__init__( name, bases, namespace )


  #-----------------------------------------------------------------------------
  @property
  def tag_key( cls ):
    """str : The key for the tag defining this schema
    """
    return cls._p_tag_key


  #-----------------------------------------------------------------------------
  @property
  def tag( cls ):
    """str : The tag defining this schema
    """
    return cls._p_tag


  #-----------------------------------------------------------------------------
  def _schema_declared( cls, schema ):
    schema = super()._schema_declared( schema )

    if not is_schema_struct(schema):
      raise SchemaDeclaredError(
        f"Must be declared for a SchemaStruct" )

    if (
      schema.tag != cls.tag or
      schema.tag_key != cls.tag_key ):

      raise SchemaDeclaredError(
        f"Defining schema declared must have the same `tag_key` '{cls.tag_key}' and `tag` '{cls.tag}'",
        hints = schema.hints )

    return schema

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaStruct( Schema ):
  """Meta-class for all defined schemas

  Parameters
  ----------
  name : str
    Class name of type
  bases : list[type]
    Base classes of type
  namespace : dict[str, object]
  tag_key : NoneType | str
    The key for the tag defining this schema
  tag : NoneType | str
    The tag defining this schema
  declared : NoneType | :class:`SchemaDeclared <partis.schema.declared.SchemaDeclared>`
    The schema declared for which this is the definition.
    If given, the `tag_key`, `tag` are not required.
  struct : NoneType | dict[ str, :class:`SchemaStruct <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>` ]
    Structure of the defined schema Mapping.
    Keys must be valid attribute names, not be "private" names starting with
    '__' (double-underscore) or '_p', or names of any Mapping attributes 'keys',
    'values', 'items', or 'get'.
  struct_proxy : NoneType | :class:`RequiredType <partis.utils.special.RequiredType>` | str
    Key of primary structure value that may be set, using defaults for all other
    values.
    If any other values are required, specifying this will raise an error.

  Raises
  ------
  SchemaDefinitionError
    If the schema definition is not valid

  See Also
  --------
  :class:`SchemaDeclared <partis.schema.declared.SchemaDeclared>`
  :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`
  """

  #-----------------------------------------------------------------------------
  def __new__(mcls,
    name,
    bases,
    namespace,
    tag_key = None,
    tag = None,
    declared = None,
    struct = None,
    struct_proxy = None,
    evaluated = None,
    default_val = None,
    default_eval = None,
    init_val = None,
    preset_vals = None,
    valued_type = None,
    doc = None,
    loc = None ):

    if default_val is None:
      default_val = required

    if default_eval is None:
      default_eval = required

    if declared is not None:
      # defines the given schema declared

      if not isinstance( declared, SchemaStructDeclared ):
        raise SchemaDefinitionError(
          f"`declared` must be subclass of SchemaStructDeclared: {fmt_base_or_type(declared)}",
          loc = loc )

      if tag_key is not None and tag_key != declared.tag_key:
        raise SchemaDefinitionError(
          f"declared `tag_key` {declared.tag_key} redefined: {tag_key}",
          loc = loc )

      if tag is not None and tag != declared.tag:
        raise SchemaDefinitionError(
          f"declared `tag` {declared.tag} redefined: {tag}",
          loc = loc )

      tag_key = declared.tag_key
      tag = declared.tag

    if tag_key is None:
      tag_key = 'type'


    if tag is None:
      tag = 'base'

    try:
      assert_valid_name( tag_key )
      assert_valid_name( tag )

    except SchemaNameError as e:
      raise SchemaDefinitionError(
        f"Schema name not valid",
        loc = loc,
        hints = SchemaHint.cast( e ) ) from e


    if struct is None:
      struct = dict()

    if not isinstance( struct, dict ):
      if is_sequence( struct ) or is_mapping( struct ):
        try:
          struct = dict( struct )

        except BaseException as e:
          raise SchemaDefinitionError(
            f"Schema struct must be an ordered dictionary, or items list: {struct}",
            loc = loc,
            hints = e )

      else:
        raise SchemaDefinitionError(
          f"Schema struct must be a mapping or sequence of key-value pairs: {struct}",
          loc = loc )

    else:
      struct = copy(struct)


    schema_deps = list()

    # validate struct items
    if tag_key in struct:
      raise SchemaDefinitionError(
        f"Schema `struct` may not define the key used as the schema's `tag_key`: {tag_key}",
        loc = loc )

    for k, v in struct.items():
      if not is_string( k ):
        raise SchemaDefinitionError(
          f"Schema struct key must be string: {k}",
          loc = loc )

      if any( k.startswith(p) for p in protected_attr ):
        raise SchemaDefinitionError(
          f"Key may not start with {protected_attr}: {k}",
          loc = loc )

      if k in mapping_attrs:
        raise SchemaDefinitionError(
          f"Key may not be of any 'Mapping' type attributes {mapping_attrs}: {k}",
          loc = loc )

      try:
        assert_valid_name( k )

      except SchemaNameError as e:
        raise SchemaDefinitionError(
          f"Schema struct key not valid",
          loc = loc,
          hints = e ) from e

      if not is_schema(v):
        raise SchemaDefinitionError(
          f"Schema struct value '{k}' must be subclass of `SchemaStruct` or `SchemaPrim`: {type(v)}",
          loc = loc )

      if not v.schema_defined:
        schema_deps.append(v)

    if evaluated is None:
      from partis.schema.eval import NotEvaluated
      evaluated = NotEvaluated

    if not is_evaluated_class(evaluated):
      raise SchemaDefinitionError(
        f"`evaluated` must be subclass of `Evaluated`: {fmt_base_or_type(evaluated)}",
        loc = loc )

    if is_required(struct_proxy):
      struct_proxy = None

    # evaluated_check = evaluated.check if evaluated else lambda x: False
    if struct_proxy:

      if not is_string(struct_proxy):
        raise SchemaDefinitionError(
          f"Schema `struct_proxy` key must be a string value: {struct_proxy}",
          loc = loc )

      if struct_proxy not in struct:
        raise SchemaDefinitionError(
          f"Schema `struct_proxy` key must be defined in schema: {struct_proxy}",
          loc = loc )

    #...........................................................................
    # for k, v in struct.items():
    #   namespace[k] = SchemaProperty(
    #     schema = v,
    #     name = k )
    #
    # namespace[ tag_key ] = ConstProperty(
    #   name = tag_key )

    namespace = { **namespace, **dict(
      _p_tag_key = tag_key,
      _p_tag = tag,
      _p_struct = struct,
      _p_struct_proxy = struct_proxy,
      _p_declared = declared )}

    cls = super().__new__(
      mcls,
      name,
      bases,
      namespace,
      evaluated = evaluated,
      default_val = default_val,
      default_eval = default_eval,
      init_val = init_val,
      preset_vals = preset_vals,
      schema_deps = schema_deps,
      valued_type = valued_type,
      doc = doc,
      loc = loc )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    tag_key = None,
    tag = None,
    declared = None,
    struct = None,
    struct_proxy = None,
    evaluated = None,
    default_val = None,
    default_eval = None,
    init_val = None,
    preset_vals = None,
    valued_type = None,
    doc = None,
    loc = None ):

    # super().__init__( name, bases, namespace )

    if cls._p_declared is not None:
      cls._p_declared.schema_declared( cls )

    super().__init__( name, bases, namespace )

  #-----------------------------------------------------------------------------
  def _get_attr_doc_lines( cls,
    noindex = False,
    depth = 0,
    max_depth = 2 ):

    lines = super()._get_attr_doc_lines(
      noindex = noindex,
      depth = depth,
      max_depth = max_depth )

    lines.extend([
      fmt_attr_doc(
        name = attr,
        typename = type( getattr( cls, attr ) ),
        obj = cls,
        val = getattr( cls, attr ),
        prefix = 'schema',
        # don't index these attributes on the instance of the meta-class, since
        # these are actually metaclass attributes
        noindex = True )
      for attr in [
        'tag_key',
        'tag',
        'struct_proxy',
        'default_val',
        'default_eval',
        'init_val' ] ])


    lines.append( fmt_attr_doc(
      name = 'evaluated',
      typename = cls.evaluated,
      obj = cls,
      prefix = 'schema',
      noindex = noindex ) )

    lines.extend([
      fmt_attr_doc(
        name = k,
        typename = fmt_schema_typename(v),
        obj = cls,
        prefix = 'schema.struct',
        noindex = noindex,
        doc = v._get_doc(
          # always specify noindex since the item schema already documented
          noindex = True,
          depth = depth + 1,
          max_depth = max_depth ) )
      for k, v in cls.struct.items() ])

    return lines

  #-----------------------------------------------------------------------------
  def _schema_hash_node( cls ):

    lines = super()._schema_hash_node()

    for attr in [
      'tag_key',
      'tag',
      # TODO: should these be included in the hash? Default values used while
      # decoding seem like non-essential information for validating what was
      # originally encoded.
      # 'default_val',
      # 'default_eval',
      # 'init_val',
      'evaluated',
      'struct_proxy' ]:

      val = getattr( cls, attr )
      hash = None

      if hasattr( val, 'schema_hash_node' ):
        hash = val.schema_hash_node
      else:
        hash = hash_sha256( str(val).encode('utf-8') )[0]

      lines.append( f'{attr}, {hash}' )

    lines.append( 'keys, ' + str(list(cls.struct.keys())) )

    return lines

  #-----------------------------------------------------------------------------
  def _schema_hash_children( cls ):
    return super()._schema_hash_children() + list(cls.struct.values())

  #-----------------------------------------------------------------------------
  def _schema_resolved( cls ):
    super()._schema_resolved()

    if cls.struct_proxy:
      for k, v in cls.struct.items():
        v = v.schema

        if k != cls.struct_proxy and is_required( v.default_val ):
          # NOTE: this only validates that no other items in the struct are required

          raise SchemaDefinitionError(
            f"Schema with a `struct_proxy` may not contain other required values: {k}",
            loc = cls.loc,
            hints = v.hints )

    return True

  #-----------------------------------------------------------------------------
  @property
  def tag_key( cls ):
    """str : Key used to obtain the tag for this struct type
    """
    return cls._p_tag_key

  #-----------------------------------------------------------------------------
  @property
  def tag( cls ):
    """str : Tag for this struct type
    """
    return cls._p_tag

  #-----------------------------------------------------------------------------
  @property
  def struct( cls ):
    """dict[ str, :class:`SchemaStruct <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.SchemaPrim>` ] : Structure
    of the defined schema
    """
    return cls._p_struct

  #-----------------------------------------------------------------------------
  @property
  def struct_proxy( cls ):
    return cls._p_struct_proxy

  #-----------------------------------------------------------------------------
  @cached_property
  def default_val( cls ):

    val = cls._p_default_val

    if not (
      is_optional( val )
      or is_required( val )
      or is_derived( val ) ):

      val = copy(val)

    if cls.struct_proxy:

      # standardize values given the struct_proxy
      if not any(
        check( val )
        for check in [
          is_required,
          is_optional,
          is_derived,
          cls.evaluated.check,
          is_mapping ] ):

        val = { cls.struct_proxy : val }

    if is_derived( val ):
      # attempt to derive a default value

      val = { cls.tag_key : cls.tag }

      for k, _schema in cls.struct.items():
        _schema = _schema.schema

        _val = _schema.default_val

        if is_required( _val ):
          raise SchemaDefinitionError(
            f"Cannot derive default from required values: {k}",
            loc = cls.loc)

        if is_valued_type( _val ):
          #TODO is this needed? all default_val should return basic types
          _val = _val._encode

        if not is_optional( _val ):
          if is_mapping( _val ) and is_schema_struct( _schema ):
            # don't need to store tag key since schema is not ambiguous
            if _schema.tag_key in _val:
              _val.pop( _schema.tag_key )

          val[k] = _val

    # ensure default value includes the tag_key: tag
    if is_mapping(val) and cls.tag_key not in val:
      val[ cls.tag_key ] = cls.tag

    return val

    # TODO: why was this here?
    # if is_optional(val) or is_required(val):
    #   return val
    # else:
    #   return cls.encode( val, cls.loc )

  #-----------------------------------------------------------------------------
  @cached_property
  def default_eval( cls ):

    val = cls._p_default_eval

    if cls.struct_proxy:

      # standardize values given the struct_proxy
      if not any(
        check( val )
        for check in [
          is_required,
          is_mapping ] ):

        val = { cls.struct_proxy : val }

    if is_required(val):
      return val
    else:
      return cls.encode( val, cls.loc )

  #-----------------------------------------------------------------------------
  @cached_property
  def init_val( cls ):
    val = cls._p_init_val

    if val is not None:
      if cls.struct_proxy:
        if not any(
          check( val )
          for check in [
            cls.evaluated.check,
            is_mapping ] ):

          val = { cls.struct_proxy : val }


      return cls.encode( val, cls.loc )

    # default_eval checked first, only not-required if `default_val` is an expression

    val = cls.default_eval

    if not is_required( val ):
      return val

    val = cls.default_val

    if not any(
      check( val )
      for check in [
        is_required,
        is_optional,
        is_derived,
        cls.evaluated.check ] ):

      # only use `default_val` if an actual value, and not an expression
      return val


    # attempt to derive an initial value
    val = { cls.tag_key : cls.tag }

    for k, _schema in cls.struct.items():
      _schema = _schema.schema

      if not is_optional( _schema.default_val ):
        _val = _schema.init_val

        val[k] = _val

    return cls.encode( val, cls.loc )

  #-----------------------------------------------------------------------------
  @property
  def evaluated( cls ):
    return cls._p_evaluated

  #-----------------------------------------------------------------------------
  @cached_property
  def hints( cls ):

    # build hints
    # NOTE: hints are constructed dynamically because initially some schemas
    # may not be fully defined with 'declared' placeholders.

    hints = super().hints

    hints.append( SchemaHint(
      f"{cls.tag_key}: {cls.tag}" ) )

    hints.append( SchemaHint(
      f"struct_proxy: {cls.struct_proxy}" ) )

    # NOTE: must check default value here in case it was a derived value
    default_val = cls.default_val

    if is_required( default_val ):
      hints.append( SchemaHint(
        f"default_val: required" ) )

    elif is_optional( default_val ):
      hints.append( SchemaHint(
        f"default_val: optional" ) )

    else:

      hints.append( SchemaHint(
        "default_val: dict",
        hints = [ default_val ] ) )

    if len(cls.struct) == 0:
      struct_hints = "Empty schema structure"

    else:
      struct_hints = list()

      for k, v in cls.struct.items():
        if is_schema_declared(v):
          struct_hints.append( SchemaHint( f"{k}" ) )

        else:
          struct_hints.append( SchemaHint(
            f"{k}:",
            hints = v.hints ) )


    hints.append( SchemaHint(
      "struct: dict[str, schema]",
      hints = struct_hints ) )


    return hints

  #-----------------------------------------------------------------------------
  def encode( cls,
    val = None,
    loc = None,
    no_defaults = None ):

    if is_valued_type( val ):

      if loc is None:
        loc = val._loc

      if val._schema.schema is not cls or is_evaluated( val._src ):
        val = val._encode

    if loc is None:
      loc = Loc(path = [cls.__name__])

    if is_optional(val):
      val = cls.default_val

      if is_required( val ):
        raise SchemaValidationError(
          f"Value is required",
          loc = loc,
          hints = cls.doc )

      elif is_optional( val ):
        return None

    if cls.evaluated.check( val ):
      return val

    if not is_mapping( val ):
      if cls.struct_proxy:
        # uses source data for primary struct key value with remaining defaults
        val = { cls.struct_proxy : val }

      else:
        raise SchemaValidationError(
          f"Value must be a mapping: {type(val).__name__}",
          loc = loc )

    _val = {
      cls.tag_key : cls.tag }

    for k, _schema in cls.struct.items():
      _schema = _schema.schema

      v = val.get(k)
      _loc = loc(key = k)

      with schema_errors(
        msg = f"Encode failed",
        loc = _loc,
        schema = cls,
        cls = SchemaValidationError ):

        v = _schema.encode(
          val = v,
          loc = _loc,
          no_defaults = no_defaults )

      if v is not None:
        if no_defaults and (
          (
            v == _schema.default_val
            and is_similar_value_type(v, _schema.default_val) )
          or (
            is_mapping( v )
            and is_schema_struct( _schema )
            and len(v) == 1
            and _schema.tag_key in v ) ):

          pass

        else:
          if is_mapping( v ) and is_schema_struct( _schema ):
            # don't need to store tag key since schema is not ambiguous
            v.pop( _schema.tag_key )

          _val[k] = v

    val = _val

    if no_defaults and (
      len(val) == 2
      and cls.struct_proxy
      and cls.struct_proxy in val ):

      val = val[cls.struct_proxy]

    # if no_defaults and (
    #   # one item when only the tag_key: tag exist
    #   len(val) == 1
    #   # check that equivalent to default value
    #   or (
    #     val == cls.default_val
    #     and all(
    #       is_similar_value_type(a,b)
    #       for a,b in zip( val.values(), cls.default_val.values() )) )):
    #
    #   val = None

    return val

  #-----------------------------------------------------------------------------
  def decode( cls,
    val = None,
    loc = None,
    bias = None ):

    valued_type = cls.valued_type

    return valued_type( val, loc, bias )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaStructProxy( SchemaProxy ):

  #-----------------------------------------------------------------------------
  def __new__(mcls,
    name,
    bases,
    namespace,
    tag_key = None,
    tag = None,
    declared = None,
    struct = None,
    struct_proxy = None,
    evaluated = None,
    default_val = None,
    default_eval = None,
    init_val = None,
    preset_vals = None,
    doc = None,
    loc = None ):

    if 'schema' in namespace:
      # attempt to take general schema arguments from class body namespace
      schema = namespace.pop('schema')

      if not is_mapping( schema ):
        raise SchemaDefinitionError(
          f"`schema` in schema class body must be a mapping: {schema}",
          loc = loc )

      kwargs = dict(
        tag_key = tag_key,
        tag = tag,
        declared = declared,
        struct = struct,
        struct_proxy = struct_proxy,
        evaluated = evaluated,
        default_val = default_val,
        default_eval = default_eval,
        init_val = init_val,
        preset_vals = preset_vals,
        doc = doc,
        loc = loc )

      for k, v in kwargs.items():

        if k in schema:
          if v is not None and v != schema[k]:
            raise SchemaDefinitionError(
              f"schema '{k}' = {v} redefined in class body: {schema[k]}",
              loc = loc )

          kwargs[k] = schema[k]

      tag_key = kwargs['tag_key']
      tag = kwargs['tag']
      declared = kwargs['declared']
      struct = kwargs['struct']
      struct_proxy = kwargs['struct_proxy']
      evaluated = kwargs['evaluated']
      default_val = kwargs['default_val']
      default_eval = kwargs['default_eval']
      init_val = kwargs['init_val']
      preset_vals = kwargs['preset_vals']
      doc = kwargs['doc']
      loc = kwargs['loc']

    if declared is not None:
      # defines the given schema declared

      if not isinstance( declared, SchemaStructDeclared ):
        raise SchemaDefinitionError(
          f"`declared` must be subclass of SchemaStructDeclared: {fmt_base_or_type(declared)}",
          loc = loc )

      if tag_key is not None and tag_key != declared.tag_key:
        raise SchemaDefinitionError(
          f"declared `tag_key` {declared.tag_key} redefined: {tag_key}",
          loc = loc )

      if tag is not None and tag != declared.tag:
        raise SchemaDefinitionError(
          f"declared `tag` {declared.tag} redefined: {tag}",
          loc = loc )

      tag_key = declared.tag_key
      tag = declared.tag


    if struct is None:
      struct = dict()

    if not isinstance( struct, dict ):
      if is_sequence( struct ) or is_mapping( struct ):
        try:
          struct = dict( struct )

        except BaseException as e:
          raise SchemaDefinitionError(
            f"Schema struct must be an ordered dictionary, or items list: {struct}",
            loc = loc,
            hints = e )

      else:
        raise SchemaDefinitionError(
          f"Schema struct must be a mapping or sequence of key-value pairs: {struct}",
          loc = loc )

    else:
      struct = copy(struct)

    # attempt to extract any struct schema items from class body namespace
    ns_struct_keys = list()

    for k, v in namespace.items():
      if is_schema( v ):
        struct[k] = v

        ns_struct_keys.append(k)

    for k in ns_struct_keys:
      # remove extracted items from namespace
      namespace.pop(k)

    # check base classes for schema definitions
    base_schema = None

    for base in bases:

      if isinstance( base, SchemaStructProxy ):
        if base_schema:
          raise SchemaDefinitionError(
            f"Schema multiple inheritance is not supported: {bases}",
            loc = loc )

        base_schema = base

    schema_bases = tuple()

    if base_schema:
      _base_schema = base_schema.schema

      schema_bases = ( _base_schema, )
      # use values from base schema to fill in those not specified

      # starts with all struct items of base schema
      _struct = dict(_base_schema.struct)

      # add/overwrite any items given for derived schema
      # NOTE: intended to preserve the original order of keys from the base schema
      # for any keys the derived class overwites

      for k,v in struct.items():
        _struct[k] = v

      struct = _struct

      if tag_key is None:
        # attempt to use base class tag_key
        tag_key = base_schema.tag_key

      if tag is None:
        # attempt to use base class tag
        tag = base_schema.tag

      if struct_proxy is None:
        struct_proxy = _base_schema._p_struct_proxy

      if default_val is None:
        default_val = _base_schema._p_default_val

      if default_eval is None:
        default_eval = _base_schema._p_default_eval

      if init_val is None:
        init_val = _base_schema._p_init_val

      # TODO: this would currently make the docs inherit unrelated docstrings
      # if doc is None and not namespace.get('__doc__', None):
      #   doc = _base_schema._p_doc

    schema_namespace = dict()

    if '__doc__' in namespace:
      schema_namespace['__doc__'] = namespace.pop('__doc__')

    schema_namespace['__module__'] = namespace['__module__']
    schema_name = name + '_schema'

    schema = SchemaStruct(
      schema_name,
      schema_bases,
      schema_namespace,
      tag_key = tag_key,
      tag = tag,
      struct = struct,
      struct_proxy = struct_proxy,
      declared = declared,
      evaluated = evaluated,
      default_val = default_val,
      default_eval = default_eval,
      init_val = init_val,
      preset_vals = preset_vals,
      doc = doc,
      loc = loc )

    module = importlib.import_module( namespace['__module__'] )

    if hasattr( module, schema_name ):
      warnings.warn(f"Overriding module attribute with class definition: {module}, {schema_name}")

    setattr( module, schema_name, schema )

    props = dict()

    #...........................................................................
    for k, v in schema.struct.items():
      props[k] = SchemaProperty(
        schema = v,
        name = k )

    props[ schema.tag_key ] = ConstProperty(
      name = schema.tag_key )


    namespace = {
      **namespace,
      **props,
      '_p_tag_key' : schema.tag_key,
      '_p_tag' : schema.tag }

    cls = super().__new__(
      mcls,
      name,
      bases,
      namespace,
      schema = schema )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    tag_key = None,
    tag = None,
    declared = None,
    struct = None,
    struct_proxy = None,
    evaluated = None,
    default_val = None,
    default_eval = None,
    init_val = None,
    doc = None,
    loc = None ):

    # NOTE: schema argument not used by __init__
    super().__init__( name, bases, namespace, schema = None )

    # set this class as the valued_type now that it is fully initialized
    cls.schema.valued_type = cls

  #-----------------------------------------------------------------------------
  @property
  def tag_key( cls ):
    """str : Key used to obtain the tag for this struct type
    """
    return cls._p_tag_key

  #-----------------------------------------------------------------------------
  @property
  def tag( cls ):
    """str : Tag for this struct type
    """
    return cls._p_tag

  #-----------------------------------------------------------------------------
  # NOTE: already implemented by StructValued __init__?
  # def __call__( cls,
  #   *args,
  #   **kwargs ):
  #
  #   if len(args) == 0:
  #     val = None
  #     loc = None
  #   else:
  #     if len(args) == 1:
  #       val = args[0]
  #       loc = None
  #     elif len(args) == 2:
  #       val, loc = args
  #     else:
  #       raise ValueError(
  #         f"positional arguments must be at most `(val, loc)`."
  #         " All keyword arguments are interpreted as items of `val`")
  #
  #   if kwargs:
  #     if val:
  #       val = {**val, **kwargs}
  #     else:
  #       val = kwargs
  #
  #   return cls.schema.decode(
  #     val = val,
  #     loc = loc )
