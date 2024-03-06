# -*- coding: UTF-8 -*-

import os

try:
  from importlib.metadata import distributions

except ImportError:
  from importlib_metadata import distributions

from partis.utils import getLogger
log = getLogger(__name__)

from partis.utils.plugin import (
  Plugin,
  PluginError,
  plugin_manager )

from partis.schema import (
  is_string,
  is_sequence,
  is_schema )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_base_schemas():
  from .hint import (
    HintList,
    HintLoc,
    Hint )

  return [ SchemaPluginGroup(
    label = "",
    schemas = {
      'Hints' : HintList }) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaPluginError( PluginError ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaPluginGroup( Plugin ):
  """Group of schemas to load as a plugin

  Parameters
  ----------
  schemas : dict[str, Schema]
    Dictionary of loaded schemas. Keys are the labels for each schema in the
    group.
  label : str
    User-friendly label for the group of schemas loaded by this plugin
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    schemas,
    label = None ):

    if label is None:
      label = ''

    for k, v in schemas.items():
      if not is_string(k):
        raise SchemaPluginError(
          f'Key must be a string: {type(k)}' )

      if not is_schema(v):
        raise SchemaPluginError(
          f'Value must be a schema: {type(v)}' )

      # ensure schemas are not a proxy
      schemas[k] = v.schema


    self._p_label = str(label)
    self._p_schemas = dict(schemas)

  #-----------------------------------------------------------------------------
  @property
  def label(self):
    return self._p_label

  #-----------------------------------------------------------------------------
  @property
  def schemas(self):
    return self._p_schemas

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaPluginManager:
  """Manages schema plugins

  Distributions providing schema plugins should define an 'entry_point' with
  a group name of 'partis.schema' that is a callable returning a list of
  instances of :class:`SchemaPluginGroup`.
  The loaded schemas can be used for automatic discovery of schemas to use for
  decoding contents using the .
  """
  #-----------------------------------------------------------------------------
  def __init__( self ):

    self._hash_lookup = dict()

  #-----------------------------------------------------------------------------
  def get_by_hash( self,
    hash ):
    """Find schema by the schema_hash

    Parameters
    ----------
    hash : str
      Value corresponding to that returned by a schema's 'schema_hash' property.

    Returns
    -------
    list[Schema]
      List of schemas matching the hash, or an empty list if none are found.
    """

    self.ensure_loaded()

    if hash not in self._hash_lookup:
      return list()

    return self._hash_lookup[ hash ]

  #-----------------------------------------------------------------------------
  def register_plugin( self,
    plugin ):

    if not isinstance( plugin, SchemaPluginGroup ):
      raise SchemaPluginError(
        f'plugin must be SchemaPluginGroup: {type(plugin)}')

    for schema in plugin.schemas.values():
      hash = schema.schema_hash

      if hash not in self._hash_lookup:
        self._hash_lookup[ hash ] = list()

      self._hash_lookup[ hash ].append( schema )

  #-----------------------------------------------------------------------------
  def ensure_loaded( self ):
    plugin_manager.ensure_loaded()

  #-----------------------------------------------------------------------------
  def load_plugins( self ):

    plugin_manager.load_plugins()

    for plugin in plugin_manager.plugins( SchemaPluginGroup ):
      self.register_plugin( plugin )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
schema_plugins = SchemaPluginManager()
