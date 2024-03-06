import logging
log = logging.getLogger( __name__ )
import os
from pathlib import PurePosixPath, PureWindowsPath, Path
from copy import copy

from partis.utils import (
  adict,
  adict_struct,
  odict,
  attrs_modify )

from partis.utils.special import (
  required,
  optional )

from partis.schema_meta.valued import (
  ValuedMeta )

from partis.schema_meta.base import (
  SchemaError,
  SchemaHint,
  Loc,
  assert_valid_name,
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

from partis.schema import (
  EvaluatedContext )

from .valued import (
  Valued,
  get_schema_loc,
  get_init_val,
  get_src_val )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PathValued(Valued):
  """Container for fully or partially evaluated string data

  Parameters
  ----------
  val : str
    Source data to be evaluated
  schema : :class:`Schema <partis.schema.struct.SchemaStruct>` | :class:`SchemaPrim <partis.schema.prim.base.SchemaPrim>`
  loc : :class:`Loc <partis.schema_meta.base.Loc>`
    Location information of source data (E.G. file, line/column number)
  """

  # #-----------------------------------------------------------------------------
  # def __new__( cls,
  #   val = None,
  #   schema = None,
  #   loc = None,
  #   bias = None ):

  #   # val = get_init_val(
  #   #   val = val,
  #   #   schema = schema,
  #   #   default_val = int() )

  #   self = Valued.__new__( cls )

  #   return self

  #-----------------------------------------------------------------------------
  def __init__( self,
    val = None,
    schema = None,
    loc = None,
    bias = None ):

    Valued.__init__( self,
      val = val,
      schema = schema,
      loc = loc,
      bias = bias )

    if self._valued:
      # track whether an empty 'parts' was explicitly given or not
      self._p_explicit = True

      # NOTE: starting with assuming windows path leads to the same result wether or
      # not it actually was a windows path, replacing slashes etc as necessary.
      # This should handle whether a path was passed in already posix-like, even when
      # on Windows.
      if isinstance(self._src, str):
        if len(self._src) == 0:
          self._p_explicit = False

      elif isinstance(self._src, PathValued):
        self._p_explicit = self._src._explicit

      self._os_path = Path(self._src)

    else:
      self._p_explicit = False
      self._os_path = Path()

  #-----------------------------------------------------------------------------
  @property
  def _explicit(self):
    return self._p_explicit

  #-----------------------------------------------------------------------------
  def __str__( self ):

    if not self._valued:
      return str(self._src)

    if self._explicit:
      return str(self._os_path)

    return ''

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  def __eq__( self, other ):
    res = super().__eq__( other )

    if res is not NotImplemented:
      return res

    if isinstance(other, PathValued):
      return self._os_path == other._os_path

    return self._os_path == other

  #-----------------------------------------------------------------------------
  def __ne__( self, other ):
    return not (self == other)

  #-----------------------------------------------------------------------------
  def __hash__( self ):
    return hash(self._os_path)

  #-----------------------------------------------------------------------------
  @property
  def _encode( self ):
    if self._valued:
      return str(self)

    if is_evaluated( self._src ):
      return self._src._encode

    assert(False)

  #-----------------------------------------------------------------------------
  def __getattribute__( self, name ):
    try:
      return super().__getattribute__(name)
    except AttributeError as e1:
      pass

    self._assert_valued()

    try:
      return getattr(self._os_path, name)
    except AttributeError as e3:
      pass

    raise AttributeError(
      f"'{type(self).__name__}' object has no key '{name}'")

  #-----------------------------------------------------------------------------
  def __fspath__( self ):
    self._assert_valued()
    return os.fspath(self._os_path)

  #-----------------------------------------------------------------------------
  def __truediv__(self, path):
    self._assert_valued()
    return self._os_path / path

  #-----------------------------------------------------------------------------
  def __rtruediv__(self, path):
    self._assert_valued()
    return Path(path) / self._os_path

  #-----------------------------------------------------------------------------
  @property
  def path(self):
    # this was usually used like __fspath__ before this class
    self._assert_valued()
    return os.fspath(self._os_path)

  # #-----------------------------------------------------------------------------
  # @property
  # def anchor(self):
  #   self._assert_valued()
  #   return self._os_path.anchor

  # #-----------------------------------------------------------------------------
  # @property
  # def parts(self):
  #   self._assert_valued()
  #   return self._os_path.parts

  # #-----------------------------------------------------------------------------
  # @property
  # def parents(self):
  #   self._assert_valued()
  #   return self._os_path.parents

  # #-----------------------------------------------------------------------------
  # @property
  # def parent(self):
  #   self._assert_valued()
  #   return type(self)(self._os_path.parent)

  # #-----------------------------------------------------------------------------
  # @property
  # def name(self):
  #   self._assert_valued()
  #   return self._os_path.name

  # #-----------------------------------------------------------------------------
  # def glob(self, pattern):
  #   self._assert_valued()
  #   for path in self._os_path.glob(pattern):
  #     yield type(self)(path)

  # #-----------------------------------------------------------------------------
  # def rglob(self, pattern):
  #   self._assert_valued()
  #   for path in self._os_path.rglob(pattern):
  #     yield type(self)(path)

  # #-----------------------------------------------------------------------------
  # def iterdir(self):
  #   self._assert_valued()
  #   for path in self._os_path.iterdir():
  #     yield type(self)(path)

  #-----------------------------------------------------------------------------
  def resolve(self, strict = False):
    self._assert_valued()
    return self._os_path.resolve(strict = strict)

  #-----------------------------------------------------------------------------
  def unlink(self, missing_ok = False):
    self._assert_valued()

    # patch-in changed in version 3.8: The missing_ok parameter was added.
    if missing_ok and not self._os_path.exists():
      return

    self._os_path.unlink()
