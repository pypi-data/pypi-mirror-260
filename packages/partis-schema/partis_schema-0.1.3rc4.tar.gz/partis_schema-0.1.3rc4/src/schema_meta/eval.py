
from copy import copy

import re
import uuid
import sys

from abc import ABCMeta
import inspect

import logging
log = logging.getLogger(__name__)

from partis.pyproj import (
  hash_sha256 )

from pygments.lexers import get_lexer_by_name

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
  fmt_base_or_type,
  fmt_class_name,
  _fmt_class_name,
  fmt_attr_doc,
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
  is_provider,
  is_evaluated_class,
  is_evaluated,
  is_valued,
  is_valued_type,
  any_schema )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProviderMeta( ABCMeta ):
  """Meta class for evaluation provider
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProviderSupport:
  """Information about a single supported evaluation by a provider

  Parameters
  ----------
  name : str
    A unique name of supported evaluation
  lexer : NoneType | str | Lexer
    Pygments lexer that may be used to apply syntax highlighting.
    If None, no highlighting will be applied.
  doc : NoneType | str
    Extra documentation about the support
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    name,
    lexer = None,
    doc = None ):

    if isinstance( lexer, str ):
      lexer = get_lexer_by_name( lexer )

    if doc is None:
      doc = ""

    self._name = str(name)
    self._lexer = lexer
    self._doc = inspect.cleandoc( doc )

  #-----------------------------------------------------------------------------
  @property
  def name( self ):
    return self._name

  #-----------------------------------------------------------------------------
  @property
  def lexer( self ):
    return self._lexer

  #-----------------------------------------------------------------------------
  @property
  def doc( self ):
    return self._doc

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return self._name

  #-----------------------------------------------------------------------------
  def __lt__( self, other ):
    return self._name < str(other)

  #-----------------------------------------------------------------------------
  def __eq__( self, other ):
    return self._name == str(other)

  #-----------------------------------------------------------------------------
  def __hash__( self ):
    return hash(self._name)

  #-----------------------------------------------------------------------------
  @cached_property
  def schema_hash_node( self ):
    """urlsafe Base64 encoded hash
    """

    return hash_sha256( self._name.encode('utf-8') )[0]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Provider( metaclass = ProviderMeta ):

  #-----------------------------------------------------------------------------
  def __init__( self ):
    pass

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    """Supported types of evaluations

    Returns
    -------
    : dict[ str, :class:`ProviderSupport`]
    """
    raise NotImplementedError("Derived provider must implement `supported`")

  #-----------------------------------------------------------------------------
  def check( self, src ):
    """Checks whether a particular source is supported

    Parameters
    ----------
    src : object
      The source data to be checked for supporting the evaluation

    Returns
    -------
    : None | tuple[ :class:`ProviderSupport`, object ]
      The evaluation support for the source data, and a (possibly) modified source
      object such as removal of any escape sequence.
      If None, evaluation is not supported
    """
    raise NotImplementedError("Derived provider must implement `check`")

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    """Modifies source data to apply escaping
    """

    raise NotImplementedError("Derived provider must implement `escaped`")

  #-----------------------------------------------------------------------------
  def lint( self,
    schema,
    src,
    loc = None,
    locals = None,
    module = None,
    logger = None ):
    """Lints source data

    Parameters
    ----------
    schema : :class:`Schema <partis.schema.Schema>`
      Schema for evaluation result
    src : object
      The source data to be evaluated
    loc : None | Loc
    locals : dict[ str, object ] | None
      Defines local variables to use for evaluation.
    module : None | str | ModuleType
      Effective python module for evaluation context, such as performing relative imports
    logger : logging.Logger
      A logger object to direct expression logs/prints instead of stdout

    Returns
    -------
    errors : list[SchemaHint]
      List of any errors to report from linting of source
    """
    return list()

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    loc = None,
    locals = None,
    module = None,
    logger = None ):
    """Evaluates source data

    Parameters
    ----------
    schema : :class:`Schema <partis.schema.Schema>`
      Schema for evaluation result
    src : object
      The source data to be evaluated
    loc : None | Loc
    locals : dict[ str, object ] | None
      Defines local variables to use for evaluation.
    module : None | str | ModuleType
      Effective python module for evaluation context, such as performing relative imports
    logger : logging.Logger
      A logger object to direct expression logs/prints instead of stdout

    Returns
    -------
    value : object
      Value resulting from evaluation.
      If there are no un-evaluated values, then will return a shallow copy of
      the current data.

    """
    raise NotImplementedError("Derived provider must implement `eval`")

  #-----------------------------------------------------------------------------
  @cached_property
  def schema_hash_node( self ):
    """urlsafe Base64 encoded hash
    """

    return hash_sha256( '\n'.join([
      f'{k}, {v.schema_hash_node}'
      for k,v in self.supported.items()  ]).encode('utf-8') )[0]


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProviderUnion( Provider ):

  #-----------------------------------------------------------------------------
  def __init__( self, providers ):
    super().__init__()

    support_map = dict()
    supported = dict()

    for i, p in enumerate(providers):
      if not isinstance(p, Provider):
        raise SchemaDefinitionError(
          f"provider {i} must be instance of Provider: {p}")

      for k, s in p.supported.items():
        if k in supported:
          if supported[k] != s:
            raise SchemaDefinitionError(
              f"provider support '{k}' redefined: {s}")
        else:
          supported[k] = s
          support_map[s] = p

    self._p_providers = providers
    self._p_supported = supported
    self._p_support_map = support_map

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return self._p_supported

  #-----------------------------------------------------------------------------
  def check( self, src ):
    for i, p in enumerate(self._p_providers):
      res = p.check(src)

      if res:
        return res

    return None

  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    if support in self._p_support_map:
      return self._p_support_map[support].escaped( support, src )

    raise ValueError(f"`support` must be one of {self.supported.values()}: {support}")

  #-----------------------------------------------------------------------------
  def lint( self,
    schema,
    src,
    loc = None,
    locals = None,
    module = None,
    logger = None ):

    supported = self.check( src )

    if not supported:
      raise SchemaEvaluationError(f"No evaluation support: {src}")

    support, _src = supported

    return self._p_support_map[support].lint(
      schema = schema,
      src = src,
      loc = loc,
      locals = locals,
      module = module,
      logger = logger )

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    loc = None,
    locals = None,
    module = None,
    logger = None ):

    supported = self.check( src )

    if not supported:
      raise SchemaEvaluationError(f"No evaluation support: {src}")

    support, _src = supported

    return self._p_support_map[support].eval(
      schema = schema,
      src = src,
      loc = loc,
      locals = locals,
      module = module,
      logger = logger )

  #-----------------------------------------------------------------------------
  @cached_property
  def schema_hash_node( self ):

    return hash_sha256( '\n'.join([
      f'{k}, {v.schema_hash_node}'
      for k,v in self.supported.items()  ]).encode('utf-8') )[0]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvaluatedContextMeta( ABCMeta ):
  """Defines a context for evaluating expressions.

  Parameters
  ----------
  id : string
    Identifier for this context
  doc : NoneType | string
  """

  #-----------------------------------------------------------------------------
  def __new__(mcls,
    name,
    bases,
    namespace,
    id = None,
    doc = None ):

    assert_valid_name( name )

    base_id = set()

    for base in bases:

      if isinstance( base, EvaluatedContextMeta ):
        base_id.add( base.id )

    if id is None and len(base_id) > 0:

      if len(base_id) > 1:
        raise SchemaDefinitionError(
          f"base class `id` is ambiguous: {base_id}")

      id = next(iter(base_id))

    # NOTE: this is intended behaviour even when id is None, resulting in
    # id -> 'None', denoting a general category with little restrictions
    id = str(id)

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


    namespace = { **namespace, **dict(
      _p_doc = doc,
      __doc__ = StringFunction(),
      _p_id = id ) }

    cls = super().__new__( mcls, name, bases, namespace )

    cls.__doc__._func = cls._get_doc

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    id = None,
    doc = None ):

    super().__init__( name, bases, namespace )

  #-----------------------------------------------------------------------------
  @classmethod
  def __prepare__( mcls, name, bases, *args, **kwargs ):
    return odict()

  #-----------------------------------------------------------------------------
  def _get_doc( cls ):
    return cls.doc

  #-----------------------------------------------------------------------------
  @property
  def doc( cls ):
    return cls._p_doc

  #-----------------------------------------------------------------------------
  @property
  def id( cls ):
    return cls._p_id

  #-----------------------------------------------------------------------------
  def __str__( cls ):
    return cls._p_id

  #-----------------------------------------------------------------------------
  def __hash__( cls ):
    return hash(cls._p_id)

  #-----------------------------------------------------------------------------
  def __eq__( cls, other ):

    return cls._p_id == str(other)

  #-----------------------------------------------------------------------------
  def __ne__( cls, other ):

    return cls._p_id != str(other)

  #-----------------------------------------------------------------------------
  @cached_property
  def schema_hash_node( cls ):
    """urlsafe Base64 encoded hash
    """

    return hash_sha256(cls._p_id.encode('utf-8'))[0]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvaluatedContext(
  metaclass = EvaluatedContextMeta ):
  """Defines a context for evaluating expressions.

  Parameters
  ----------
  module : None | str | ModuleType
    Module relative to which the evaluation is to occur
  """

  #-----------------------------------------------------------------------------
  def __init__(self, *, module = None ):

    self._p_module = module

  #-----------------------------------------------------------------------------
  @property
  def module( self ):
    return self._p_module

  #-----------------------------------------------------------------------------
  def locals( self, *,
    schema ):
    """Provides the local variables to use when evaluating

    Parameters
    ----------
    schema : :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>` | :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`
      Schema for the resulting value.

    Returns
    -------
    :class:`Mapping`
    """

    return dict()

  #-----------------------------------------------------------------------------
  def __call__( self, *,
    schema,
    parent,
    key ):
    """Generates a new context for a child of the current valued object.

    .. note::
      New context instance must be of the same class as the current context

    Parameters
    ----------
    schema : :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>` | :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`
      Schema for the parent value.
    parent : :class:`Valued <partis.schema.valued.Valued>` | :class:`SchemaStruct <partis.schema.struct.SchemaStruct>`
      Parent valued object to which the current :class:`EvaluatedNamespace` was
      originally generated.

      .. note::

        The parent value will only contain those values that have been
        evaluated up to the point at which the current value is being evaluated.
        If those previous evaluations have a different context, they will
        may remain un-evaluated.

    key : str | int
      Key (str) of mapping, or index (int) of sequence, within the ``parent``
      that the returned ``EvaluatedContext`` should correspond.

    Returns
    -------
    :class:`EvaluatedContext`
    """

    return self

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvaluatedMeta( ABCMeta ):
  """Meta-class for a variable type that must be evaluated

  Parameters
  ----------
  name : str
    Class name of type
  bases : list[type]
    Base classes of type
  namespace : dict[str, object]
  provider : NoneType | :class:`Provider <partis.schema.eval.Provider>`
    Provider for evaluating expressions.
  context : NoneType | :class:`EvaluatedContextMeta`
    Sets the context for which these expressions is to be evaluated.
    A value of None will cause the expression to be evaluated upon any call.
    Otherwise, the expression is evaluated only when called with the specified
    context.
  """
  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    provider = None,
    context = None ):

    assert_valid_name( name )

    base_provider = list()
    base_context = list()

    for base in bases:

      if is_evaluated_class( base ):
        if base.provider and base.provider not in base_provider:
          base_provider.append( base.provider )

        if base.context and base.context not in base_context:
          base_context.append( base.context )

    if provider is None and len(base_provider) > 0:

      if len(base_provider) > 1:
        provider = ProviderUnion(base_provider)
      else:
        provider = next(iter(base_provider))

    if provider is not None and not is_provider( provider ):
        raise SchemaDefinitionError(
          f"`provider` must be instance of `Provider`: {provider}")

    if context is None:
      if len(base_context) > 0:

        if len(base_context) > 1:
          raise SchemaDefinitionError(
            f"base class `context` is ambiguous: {base_context}")

        context = next(iter(base_context))

      else:
        context = EvaluatedContext

    if not isinstance( context, EvaluatedContextMeta ):
      raise SchemaDefinitionError(
        f"`context` must be an `EvaluatedContextMeta`: {context}")


    if '__doc__' not in namespace:
      lines = list()

      if provider is None:
        supported = "Evaluation not supported."
      else:
        supported = "\n".join([
          'Supported evaluations:\n',
          *[f"* {s}" for s in provider.supported.values()] ])

      lines.extend([
        fmt_attr_doc(
          name = 'context',
          prefix = 'property',
          typename = _fmt_class_name(context),
          val = context,
          doc = context.doc ),
        fmt_attr_doc(
          name = 'provider',
          prefix = 'property',
          typename = type(provider),
          val = ...,
          doc = supported ) ])


      namespace['__doc__'] = "\n".join(lines)

    namespace = odict( **namespace,
      _p_num_subclass = 0,
      _p_provider = provider,
      _p_context = context )

    cls = super().__new__( mcls, name, bases, namespace )

    return cls

  #-----------------------------------------------------------------------------
  def __init__( cls,
    name,
    bases,
    namespace,
    provider = None,
    context = None ):

    super().__init__( name, bases, namespace )

  #-----------------------------------------------------------------------------
  def __or__( cls, other ):

    module, name = make_dynamic_class_name(
      default_name = cls.__name__ + '_' + other.__name__ )

    return cls.subclass(
      name = name,
      module = module,
      bases = (other,) )

  #-----------------------------------------------------------------------------
  @property
  def provider( cls ):
    """:class:`Provider <partis.schema.eval.Provider>` : Provider for evaluating expressions.
    """
    return cls._p_provider

  #-----------------------------------------------------------------------------
  @property
  def context( cls ):
    """NoneType | :class:`EvaluatedContextMeta`
    """
    return cls._p_context

  #-----------------------------------------------------------------------------
  @property
  def supported( cls ):
    """Supported types of evaluations

    Returns
    -------
    : dict[ str, :class:`ProviderSupport`]
    """

    if cls.provider is None:
      return dict()

    return cls.provider.supported

  #-----------------------------------------------------------------------------
  def check( cls, src ):
    """Checks whether a particular source is supported

    Parameters
    ----------
    src : object
      The source data to be checked

    Returns
    -------
    : NoneType | tuple[ :class:`ProviderSupport`, object ]
      The evaluation support for the source data, and a (possibly) modified source
      object such as removal of any escape sequence.
      If None, evaluation is not supported
    """
    if cls.provider is None:
      return None

    return cls.provider.check( src )

  #-----------------------------------------------------------------------------
  def escaped( cls, support, src ):
    """Modifies source data to apply escaping
    """

    if cls.provider is None:
      return src

    return cls.provider.escaped( support, src )

  #-----------------------------------------------------------------------------
  def subclass( cls,
    name = None,
    module = None,
    module_set = None,
    bases = None,
    **kwargs ):
    """
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
      Keyword arguments passed
    """

    module, name = make_dynamic_class_name(
      default_name = cls.__name__,
      module = module,
      name = name )

    cls._p_num_subclass += 1

    if bases is None:
      bases = tuple()

    bases = ( cls, ) + bases

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
        warnings.warn(f"Overriding module attribute with class definition: {sub_cls.__name__}")

      setattr( module, sub_cls.__name__, sub_cls )



    return sub_cls

  #-----------------------------------------------------------------------------
  def _schema_hash_node( cls ):

    lines = list()

    for attr in [
      'provider',
      'context' ]:

      val = getattr( cls, attr )
      hash = None

      if hasattr( val, 'schema_hash_node' ):
        hash = val.schema_hash_node
      else:
        hash = hash_sha256( str(val).encode('utf-8') )[0]

      lines.append( f'{hash}' )

    return lines

  #-----------------------------------------------------------------------------
  @cached_property
  def schema_hash_node( cls ):
    """urlsafe Base64 encoded hash
    """

    return hash_sha256(
      '\n'.join( cls._schema_hash_node() ).encode('utf-8') )[0]
