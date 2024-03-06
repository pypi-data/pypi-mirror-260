# -*- coding: UTF-8 -*-

import logging
log = logging.getLogger(__name__)

from copy import copy
import inspect
import re

from partis.utils import (
  odict,
  cached_property,
  fmt_base_or_type,
  fmt_iterable_or,
  fmt_attr_doc,
  _fmt_class_name,
  fmt_class_name,
  indent_lines,
  isinstance_any )

from partis.pyproj import (
  hash_sha256 )

from partis.utils.special import (
  required,
  optional,
  derived )

from partis.schema_meta.base import (
  SchemaError,
  SchemaNameError,
  SchemaDeclaredError,
  SchemaDefinitionError,
  SchemaValidationError,
  SchemaHint,
  Bias,
  Loc,
  assert_valid_name,
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
  is_similar_value_type,
  is_evaluated,
  is_valued,
  is_optional,
  is_required )

from partis.schema_meta.schema import (
  fmt_schema_typename )

from partis.schema.valued import (
  Valued )

from partis.schema.eval import (
  NotEvaluated )

from . import (
  SchemaPrimDeclared,
  SchemaPrim,
  PassPrim,
  BoolPrimDeclared,
  BoolPrim,
  IntPrimDeclared,
  IntPrim,
  FloatPrimDeclared,
  FloatPrim,
  StrPrimDeclared,
  StrPrim,
  SeqPrimDeclared,
  SeqPrim,
  MapPrimDeclared,
  MapPrim )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UnionPrimDeclared( SchemaPrimDeclared ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def validate_union_cases( cases, loc ):

  _bool_prim = None
  _numeric_prim = None
  _string_prim = None
  _list_prim = None
  _dict_prim = None
  _schemas = list()
  _evaluated_cases = list()
  _schema_deps = list()

  proxy_cases = list()
  proxies = list()

  for case in cases:
    if case.schema_defined and is_schema_struct( case ) and case.schema.struct_proxy:
      proxy = case.schema.struct[case.schema.struct_proxy]

      if is_schema_struct( proxy ) and proxy.schema.struct_proxy:
        raise SchemaDefinitionError(
          f"`UnionPrim` may not have `Schema` case with a nested `struct_proxy`",
          loc = loc,
          hints = str(case) )

      proxy_cases.append(case)
      proxies.append(proxy)

  for case in cases + proxies:
    if not case.schema_defined:
      _schema_deps.append(case)

    # these conditions are to prevent ambiguities when blind coding 'simple'
    # data that may be interpreted in more than one way
    if is_schema_prim( case ):

      if case.schema_defined:
        _evaluated_cases.append( case.schema.evaluated )

      if isinstance_any( case, [ BoolPrim, BoolPrimDeclared ] ):
        if _bool_prim is not None:
          raise SchemaDefinitionError(
            f"`UnionPrim` may only have one `BoolPrim` case",
            loc = loc,
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ])

        _bool_prim = case

      elif isinstance_any( case, [ IntPrim, IntPrimDeclared, FloatPrim, FloatPrimDeclared ] ):
        if _numeric_prim is not None:
          raise SchemaDefinitionError(
            f"`UnionPrim` may only have one numeric {{`IntPrim`, `FloatPrim`}} case",
            loc = loc,
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ])

        _numeric_prim = case

      elif isinstance_any( case, [ StrPrim, StrPrimDeclared ] ):
        if _string_prim is not None:
          raise SchemaDefinitionError(
            f"`UnionPrim` may only have one `StrPrim` case",
            loc = loc,
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ])

        _string_prim = case

      elif isinstance_any( case, [ SeqPrim, SeqPrimDeclared ] ):
        if _list_prim is not None:
          raise SchemaDefinitionError(
            f"`UnionPrim` may only have one `SeqPrim` case",
            loc = loc,
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ] )

        _list_prim = case

      elif isinstance_any( case, [ MapPrim, MapPrimDeclared ] ):
        if len(_schemas) > 0:
          raise SchemaDefinitionError(
            f"`UnionPrim` may not have both `SchemaStruct` and `MapPrim` cases",
            loc = loc,
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ] )

        elif _dict_prim is not None:
          raise SchemaDefinitionError(
            f"`UnionPrim` may only have one `MapPrim` case",
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ] )

        _dict_prim = case

      elif isinstance_any( case, [ UnionPrim, UnionPrimDeclared ] ):
        raise SchemaDefinitionError(
          f"`UnionPrim` may not contain any `UnionPrim` cases",
          loc = loc,
          hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ] )

      elif isinstance( case, PassPrim ):
        raise SchemaDefinitionError(
          f"`UnionPrim` may not contain any `PassPrim` cases",
          loc = loc,
          hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ] )

      else:
        assert False

    elif is_schema_struct( case ):

      if case.schema_defined:

        _evaluated_cases.append( case.schema.evaluated )

        # if case.schema.struct_proxy:
        #   raise SchemaDefinitionError(
        #     f"`UnionPrim` may not have `Schema` case with a `struct_proxy`",
        #     loc = loc,
        #     hints = str(case) )

        if _dict_prim is not None:
          raise SchemaDefinitionError(
            f"`UnionPrim` may not have both `SchemaStruct` and `MapPrim` cases",
            loc = loc,
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ] )

        if len(_schemas) > 1 and _schemas[0].tag_key != case.tag_key:
          raise SchemaDefinitionError(
            f"`UnionPrim` may not have Schemas cases with multiple values for `tag_key`",
            loc = loc,
            hints = [ SchemaHint(f"case: {i}", hints = str(c) ) for i,c in enumerate(cases) ] )

      # multiple schemas may be in the union, since they can be differentiated
      # by the `tag_key`
      _schemas.append( case )

    else:
      assert False

  return ( _bool_prim,
    _numeric_prim,
    _string_prim,
    _list_prim,
    _dict_prim,
    _schemas,
    proxy_cases,
    proxies,
    _evaluated_cases,
    _schema_deps )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class UnionPrim( SchemaPrim ):
  """Primitive for union of types values

  Parameters
  ----------
  cases : list[ :class:`SchemaStruct <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>` ]
    Schemas that are considered for decoding a value.
    The union of schemas may not be ambiguous, restricting the combinations to

      - Max of one case of :class:`BoolPrim <partis.schema.prim.bool_prim.BoolPrim>`.

      - Max of one numeric case of either :class:`IntPrim <partis.schema.prim.int_prim.IntPrim>`
        or :class:`FloatPrim <partis.schema.prim.float_prim.FloatPrim>`.

      - Max of one case of :class:`StrPrim <partis.schema.prim.str_prim.StrPrim>`.

      - Max of one case of :class:`SeqPrim <partis.schema.prim.seq_prim.SeqPrim>`.

      - Max of one case of :class:`MapPrim <partis.schema.prim.map_prim.MapPrim>`.

      - May not have cases of both :class:`MapPrim <partis.schema.prim.map_prim.MapPrim>`
        and :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`.

      - All cases of :class:`SchemaStruct <partis.schema.struct.SchemaStruct>` must be defined
        with the same `tag_key`, and no cases with a nested `struct_proxy`.

      - May not have any case of :class:`PassPrim <partis.schema.prim.pass_prim.PassPrim>`

  default_case : NoneType | int
    Case to use for default value when source data is not available, including
    if the case's `default_val` is required or optional.

  **kwargs : arguments passed to :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  """

  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    cases,
    default_case = None,
    **kwargs ):

    loc = kwargs.get('loc', None)

    if not is_sequence( cases ):
      raise SchemaDefinitionError(
        f"`UnionPrim` cases must be list of `SchemaPrim` or `Schema`: {type(cases).__name__}",
        loc = loc )

    cases = list( cases )

    for i, case in enumerate(cases):
      if not is_schema( case ):
        raise SchemaDefinitionError(
          f"`UnionPrim` case '{i}' must be instance of `SchemaPrim` or `Schema`: {case}",
          loc = loc )

    if len(cases) < 1:
      raise SchemaDefinitionError(
        f"`UnionPrim` must have at least one case",
        loc = loc )

    if default_case is None:
      default_case = required

    if not is_required( default_case ):
      if not is_numeric( default_case ):
        raise SchemaDefinitionError(
          f"`default_case` must be an integer: {default_case}",
          loc = loc )

      # TODO: check that default_val is 'required', since it would be ambiguous
      # to specify both default_val and default_case

      default_case = int(default_case)

      if default_case < 0 or default_case >= len(cases):
        raise SchemaDefinitionError(
          f"`default_case` invalid with {len(cases)} cases: {default_case}",
          loc = loc )

    ( _bool_prim,
      _numeric_prim,
      _string_prim,
      _list_prim,
      _dict_prim,
      _schemas,
      proxy_cases,
      proxies,
      _evaluated_cases,
      _schema_deps ) = validate_union_cases(
        cases = cases,
        loc = loc )

    #...........................................................................
    _schema_tags = [ c.tag for c in _schemas ]

    kwargs['schema_deps'] = kwargs.get('schema_deps', list()) + _schema_deps

    namespace = { **namespace, **dict(
      _p_bool_prim = _bool_prim,
      _p_numeric_prim = _numeric_prim,
      _p_string_prim = _string_prim,
      _p_list_prim = _list_prim,
      _p_dict_prim = _dict_prim,
      _p_schemas = _schemas,
      _p_proxy_cases = proxy_cases,
      _p_proxies = proxies,
      _p_schema_tags = _schema_tags,
      _p_default_case = default_case,
      _p_cases = cases ) }

    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      valued_type = Valued,
      **kwargs )

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    cases,
    default_case = None,
    **kwargs ):


    super().__init__(
      name = name,
      bases = bases,
      namespace = namespace,
      **kwargs )

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
        val = getattr( cls, attr ),
        prefix = 'schema',
        noindex = noindex )
      for attr in [
        'default_case' ] ])

    case_lines = list()

    for i, case in enumerate(cls.cases):
      # schema = case.schema

      case_lines.append( f"{i} {fmt_schema_typename(case, fmt_class_name)}" )

      # case_lines.append( indent_lines( 2, schema._get_doc(
      #   # always specify noindex since the item schema already documented
      #   noindex = True,
      #   depth = depth + 1,
      #   max_depth = max_depth ) ) )

      case_lines.append('')

    lines.append(
      fmt_attr_doc(
        name = 'cases',
        typename = f'list[~partis.schema_meta.schema.Schema]',
        val = ...,
        prefix = 'schema',
        doc = '\n'.join(case_lines),
        noindex = noindex ) )

    return lines

  #-----------------------------------------------------------------------------
  def _schema_hash_children( cls ):
    return list(cls.cases)

  #-----------------------------------------------------------------------------
  @property
  def cases( cls ):
    return cls._p_cases

  #-----------------------------------------------------------------------------
  @property
  def default_case( cls ):
    return cls._p_default_case

  #-----------------------------------------------------------------------------
  @cached_property
  def default_val( cls ):
    val = super().default_val

    if (
      ( is_optional(val) or is_required(val) )
      and not is_required(cls.default_case) ):

      case = cls.cases[ cls.default_case ].schema
      val = case.default_val

      if (
        is_mapping(val)
        and is_schema_struct(case)
        and case.tag_key in val
        and len(cls._p_schemas) == 1 ):
          # tag is not needed when schema is not ambiguous
          # NOTE: this is an exception to the rule that the default_val includes the
          # tag, since there cannot be a union directly in another union.
          val.pop( case.tag_key )

    return val

  #-----------------------------------------------------------------------------
  @cached_property
  def default_eval( cls ):
    val = super().default_eval

    if not is_required( cls.default_case ) and (
      is_optional( val )
      or is_required( val ) ):

      case = cls.cases[ cls.default_case ].schema
      val = case.default_eval

      if (
        is_mapping(val)
        and is_schema_struct(case)
        and case.tag_key in val
        and len(cls._p_schemas) == 1 ):
          # tag is not needed when schema is not ambiguous
          val.pop( case.tag_key )

    return val

  #-----------------------------------------------------------------------------
  @cached_property
  def init_val( cls ):
    val = super().init_val

    if val is not None:
      return val

    init_case = cls.default_case

    if is_required( init_case ):
      init_case = 0

    case = cls.cases[ init_case ].schema
    val = case.init_val

    if is_schema_struct(case) and len(cls._p_schemas) == 1:
      val.pop( case.tag_key )

    return val

  #-----------------------------------------------------------------------------
  @property
  def hints( cls ):
    hints = super().hints

    hints.append(f"default_case: {cls.default_case}")

    _hints = list()

    for i, c in enumerate(cls.cases):
      _hints.append( SchemaHint( f"{i}: {c.schema.__module__}.{c.schema.__name__}" ) )

      # if is_schema_declared(c):
      #   _hints.append( SchemaHint( f"{i}: {case.schema.__module__}.{case.schema.__name__}" ) )
      #
      # else:
      #   _hints.append( SchemaHint( f"{i}:", hints = c.schema.hints ) )

    hints.append( SchemaHint(
      f"cases: list[schema]",
      hints = _hints ) )

    return hints

  #-----------------------------------------------------------------------------
  def _schema_resolved( cls ):

    ( _bool_prim,
      _numeric_prim,
      _string_prim,
      _list_prim,
      _dict_prim,
      _schemas,
      proxy_cases,
      proxies,
      _evaluated_cases,
      _schema_deps ) = validate_union_cases(
        cases = cls._p_cases,
        loc = cls.loc )

    cls._p_bool_prim = _bool_prim
    cls._p_numeric_prim = _numeric_prim
    cls._p_string_prim = _string_prim
    cls._p_list_prim = _list_prim
    cls._p_dict_prim = _dict_prim
    cls._schemas = _schemas
    cls._p_proxy_cases = proxy_cases
    cls._p_proxies = proxies

    _evaluated_cases.append( cls.evaluated )

    eval_options = list()

    for eval in _evaluated_cases:
      if ( eval is not NotEvaluated ) and ( eval not in eval_options ):
        eval_options.append(eval)

    if len(eval_options) == 0:
      evaluated = NotEvaluated

    elif len(eval_options) == 1:
      evaluated = eval_options[0]

    else:
      evaluated = eval_options[0].subclass(
        name = cls.__name__ + '_evaluated',
        module = cls.__module__,
        bases = eval_options[1:] )

    cls._p_evaluated = evaluated

    super()._schema_resolved()

  #-----------------------------------------------------------------------------
  def encode( cls,
    val = None,
    loc = None,
    no_defaults = None ):

    val, loc, validate = cls._encode(
      val = val,
      loc = loc,
      no_defaults = no_defaults )

    if not validate:
      return val

    val = cls.validate(
      val = val,
      loc = loc )[0]

    schema = None
    tag_key = None
    tag_key_optional = False

    if is_bool( val ) and cls._p_bool_prim is not None:
      schema = cls._p_bool_prim.schema

    elif is_numeric( val ) and cls._p_numeric_prim is not None:
      schema = cls._p_numeric_prim.schema

    elif is_string( val ) and cls._p_string_prim is not None:
      schema = cls._p_string_prim.schema

    elif is_sequence( val ) and cls._p_list_prim is not None:
      schema = cls._p_list_prim.schema

    elif is_mapping( val ) and cls._p_dict_prim is not None:
      schema = cls._p_dict_prim.schema

    elif is_mapping( val ) and len(cls._p_schemas) > 0:
      tag_key = cls._p_schemas[0].tag_key

      if len(cls._p_schemas) == 1:
        # only one schema to try
        schema = cls._p_schemas[0].schema
        tag_key_optional = True

      else:
        # requires tag to resolve ambiguity

        if tag_key not in val:
          # if the schema is ambiguous, must have given the tag value
          _tags = fmt_iterable_or( cls._p_schema_tags )

          raise SchemaValidationError(
            f"Union of schemas item '{tag_key}' must be any of {_tags}",
            loc = loc )

        tag = val[tag_key]

        if tag not in cls._p_schema_tags:
          _tags = fmt_iterable_or( cls._p_schema_tags )

          raise SchemaValidationError(
            f"Union of schemas item '{tag_key}' must be any of {_tags}: {tag}",
            loc = loc )

        schema = cls._p_schemas[ cls._p_schema_tags.index( tag ) ].schema

    else:
      raise SchemaValidationError(
        f"`{cls.__name__}` union case not found for value: {fmt_base_or_type(val)}",
        loc = None,
        hints = [ SchemaHint(
          f"case {i}: `{c.schema.__name__}` <{type(c.schema).__name__}>" )
          for i,c in enumerate(cls.cases) ] )

    val = schema.encode(
      val = val,
      no_defaults = no_defaults )

    # if no_defaults:
    #   default_val = cls.default_val
    #
    #   if not ( is_optional(default_val) or is_required(default_val) ):
    #
    #     if is_similar_value_type(val, default_val) and val == default_val:
    #       # NOTE: is_similar_value_type is needed to prevent removal of values
    #       # that are "equal", but have a different type.
    #       # E.G: 0.0 == False, but float != bool.
    #       val = None
    #
    #   if val is None and (
    #     is_required(default_val)
    #     or is_optional(default_val)
    #     or is_required(cls.default_case)
    #     or schema is not cls.cases[ cls.default_case ].schema ):
    #
    #     val = schema.default_val

    if is_mapping(val) and tag_key in val and tag_key_optional:
      val.pop( tag_key )

    return val

  #-----------------------------------------------------------------------------
  def decode( cls,
    val = None,
    loc = None,
    bias = None ):

    bias = Bias(bias)

    val, loc, validate, bias = cls._decode(
      val = val,
      loc = loc,
      bias = bias )

    if not validate:
      return val

    val, bias = cls.validate(
      val = val,
      loc = loc,
      bias = bias )

    if is_bool( val ) and cls._p_bool_prim is not None:
      if cls._p_bool_prim in cls._p_proxies:
        return cls._p_proxy_cases[cls._p_proxies.index(cls._p_bool_prim)].schema.decode(
          val = val,
          loc = loc,
          bias = bias )
      else:
        return cls._p_bool_prim.schema.decode(
          val = val,
          loc = loc,
          bias = bias  )

    if is_numeric( val ) and cls._p_numeric_prim is not None:
      if cls._p_numeric_prim in cls._p_proxies:
        return cls._p_proxy_cases[cls._p_proxies.index(cls._p_numeric_prim)].schema.decode(
          val = val,
          loc = loc,
          bias = bias  )
      else:
        return cls._p_numeric_prim.schema.decode(
          val = val,
          loc = loc,
          bias = bias )

    if is_string( val ) and cls._p_string_prim is not None:
      if cls._p_string_prim in cls._p_proxies:
        return cls._p_proxy_cases[cls._p_proxies.index(cls._p_string_prim)].schema.decode(
          val = val,
          loc = loc,
          bias = bias )
      else:
        return cls._p_string_prim.schema.decode(
          val = val,
          loc = loc,
          bias = bias )

    if is_sequence( val ) and cls._p_list_prim is not None:
      if cls._p_list_prim in cls._p_proxies:
        return cls._p_proxy_cases[cls._p_proxies.index(cls._p_list_prim)].schema.decode(
          val = val,
          loc = loc,
          bias = bias )
      else:
        return cls._p_list_prim.schema.decode(
          val = val,
          loc = loc,
          bias = bias )

    if is_mapping( val ) and cls._p_dict_prim is not None:
      if cls._p_dict_prim is not None:
        return cls._p_dict_prim.schema.decode(
          val = val,
          loc = loc,
          bias = bias )

    if is_mapping( val ) and len(cls._p_schemas) > 0:

      if len(cls._p_schemas) == 1:
        # only one schema to try
        return cls._p_schemas[0].schema.decode(
          val = val,
          loc = loc,
          bias = bias )

      else:
        # requires tag to resolve ambiguity

        tag_key = cls._p_schemas[0].tag_key

        if tag_key not in val:
          # if the schema is ambiguous, must have given the tag value
          _tags = fmt_iterable_or( cls._p_schema_tags )

          raise SchemaValidationError(
            f"Union of schemas item '{tag_key}' must be any of {_tags}",
            loc = loc )


        tag = val[tag_key]

        if tag not in cls._p_schema_tags:
          _tags = fmt_iterable_or( cls._p_schema_tags )

          raise SchemaValidationError(
            f"Union of schemas item '{tag_key}' must be any of {_tags}: {tag}",
            loc = loc )

        schema = cls._p_schemas[ cls._p_schema_tags.index( tag ) ].schema

        return schema.decode(
          val = val,
          loc = loc,
          bias = bias )

    raise SchemaValidationError(
      f"`{cls.__name__}` union case not found for value: {fmt_base_or_type(val)}",
      loc = loc,
      hints = [ SchemaHint(
        f"case {i}: `{c.schema.__name__}` <{type(c.schema).__name__}>" )
        for i,c in enumerate(cls.cases) ] )
