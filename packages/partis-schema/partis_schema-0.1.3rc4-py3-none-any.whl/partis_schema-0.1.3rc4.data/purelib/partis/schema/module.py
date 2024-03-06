import types
import importlib
import importlib.abc
import inspect
import sys

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaLoader( importlib.abc.Loader ):
  """Loader for a schema module
  """
  #-----------------------------------------------------------------------------
  def __init__( self, schema_module ):

    self._p_schema_module = schema_module

  #-----------------------------------------------------------------------------
  def create_module( self, spec ):

    return self._p_schema_module

  #-----------------------------------------------------------------------------
  def exec_module( self, module ):

    return module


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaFinder( importlib.abc.MetaPathFinder ):
  """Finder for schema modules
  """
  #-----------------------------------------------------------------------------
  def __init__( self ):
    self._p_schema_specs = dict()

  #-----------------------------------------------------------------------------
  @property
  def schema_specs( self ):
    return self._p_schema_specs

  #-----------------------------------------------------------------------------
  def register( self, schema_module, origin = None ):

    if not isinstance( schema_module, SchemaModule ):
      raise ValueError(f"`schema_module` must be instance of SchemaModule: {type(schema_module)}")

    fullname = schema_module.__name__

    if fullname in self.schema_specs:
      raise ValueError(f"Schema module already registered: {fullname}")

    spec = importlib.machinery.ModuleSpec(
      fullname,
      loader = SchemaLoader(
        schema_module = schema_module ),
      origin = origin,
      loader_state = None,
      is_package = False  )

    self.schema_specs[ fullname ] = spec

    return spec

  #-----------------------------------------------------------------------------
  def find_spec( self, fullname, path, target = None ):

    if fullname not in self._p_schema_specs:
      return None

    return self._p_schema_specs[ fullname ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
schema_finder = SchemaFinder()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
sys.meta_path.append( schema_finder )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaModule ( types.ModuleType ):
  """Base class for schema modules
  """

  #-----------------------------------------------------------------------------
  def __init__( self, fullname = None, doc = None, origin = None ):

    if fullname is None:
      idx = 0

      fullname = f"{type(self).__name__}_{idx}"

      while fullname in schema_finder.schema_specs:
        idx += 1
        fullname = f"{type(self).__name__}_{idx}"

    super().__init__( fullname, doc = doc )

    spec = schema_finder.register( self, origin = origin )
    self.__loader__ = spec.loader

    if origin is not None:
      self.__file__ = origin
