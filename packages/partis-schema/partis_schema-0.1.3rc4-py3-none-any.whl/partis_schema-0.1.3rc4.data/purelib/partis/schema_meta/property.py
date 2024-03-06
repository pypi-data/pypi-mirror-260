
import logging
log = logging.getLogger(__name__)

from partis.utils import (
  fmt_class_name )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaProperty:

  #-----------------------------------------------------------------------------
  def __init__( self, schema, name = None ):

    self._name = name
    self._schema = schema

  #-----------------------------------------------------------------------------
  def __set_name__(self, owner, name):
    self._name = name

  #-----------------------------------------------------------------------------
  def __get__( self, obj, owner = None ):
    """
    Note
    ----
    If accessor is called on the class, instead of the instance, this will
    return the schema for the value instead of the value.
    """
    if obj is None:
      return self._schema

    return obj[ self._name ]

  #-----------------------------------------------------------------------------
  def __set__( self, obj, value ):
    if obj is None:
      raise AttributeError(f"Re-defining schema property not allowed: {self._name}")

    obj[ self._name ] = value

  #-----------------------------------------------------------------------------
  def __delete__(self, obj):
    raise AttributeError(f"Deleting schema property not allowed: {self._name}")

  #-----------------------------------------------------------------------------
  def getter(self, fget):
      raise ValueError(f"Changing getter not allowed")

  #-----------------------------------------------------------------------------
  def setter(self, fset):
      raise ValueError(f"Changing setter not allowed")

  #-----------------------------------------------------------------------------
  def deleter(self, fdel):
      raise ValueError(f"Changing deleter not allowed")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ConstProperty:

  #-----------------------------------------------------------------------------
  def __init__( self, name = None ):

    self._name = name

  #-----------------------------------------------------------------------------
  def __set_name__(self, owner, name):
    self._name = name

  #-----------------------------------------------------------------------------
  def __get__( self, obj, owner = None ):
    if obj is None:
      return self

    return obj[ self._name ]

  #-----------------------------------------------------------------------------
  def __set__( self, obj, value ):
    raise AttributeError(f"Setting schema property not allowed: {self._name}")

  #-----------------------------------------------------------------------------
  def __delete__(self, obj):
    raise AttributeError(f"Deleting schema property not allowed: {self._name}")

  #-----------------------------------------------------------------------------
  def getter(self, fget):
      raise ValueError(f"Changing getter not allowed")

  #-----------------------------------------------------------------------------
  def setter(self, fset):
      raise ValueError(f"Changing setter not allowed")

  #-----------------------------------------------------------------------------
  def deleter(self, fdel):
      raise ValueError(f"Changing deleter not allowed")
