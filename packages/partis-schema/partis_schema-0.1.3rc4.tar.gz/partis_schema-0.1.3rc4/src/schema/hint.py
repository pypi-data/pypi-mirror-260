
import os
import subprocess
import shutil
from timeit import default_timer as timer

import logging
log = logging.getLogger(__name__)

from partis.schema import (
  Loc,
  required,
  optional,
  derived,
  is_sequence,
  is_mapping,
  is_evaluated,
  is_valued,
  is_valued_type,
  is_optional,
  PyEvaluated,
  CheetahEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
  schema_declared,
  EvaluatedContext )

from partis.utils import (
  ModelHint,
  Loc,
  HINT_LEVELS_DESC,
  indent_lines )

from partis.utils.hint import (
  DATA_FORMATS )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
hint_declared = schema_declared( tag = 'hint' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HintList = SeqPrim(
  doc = "List of hints",
  item = hint_declared,
  default_val = list() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintLoc( StructValued ):
  """A schema for serializing ModelHints
  """

  schema = dict(
    tag = 'loc',
    default_val = derived,
    struct_proxy = 'filename' )

  filename = StrPrim(
    doc = "Referenced location",
    default_val = "",
    max_lines = 1 )

  line = IntPrim( default_val = 0 )
  col = IntPrim( default_val = 0 )

  path = SeqPrim(
    default_val = list(),
    item = UnionPrim(
      cases = [
        IntPrim(),
        StrPrim(
          max_lines = 1 )] ) )

  owner = StrPrim(
    doc = "Owner of reference",
    default_val = "",
    max_lines = 1 )

  time = FloatPrim( default_val = 0 )

  #-----------------------------------------------------------------------------
  def _cast( self ):
    """Converts instance of this to instance of a regular ModelHint

    Returns
    :class:`ModelHint <partis.utils.hint.ModelHint>`
    """
    d = self._schema.encode(
      val = self,
      loc = self._loc,
      no_defaults = True )

    return Loc.from_dict(d)

  #-----------------------------------------------------------------------------
  def __rich__( self ):
    return self._cast().fmt( with_rich = True )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Hint( StructValued ):
  """A schema for serializing ModelHints
  """

  schema = dict(
    declared = hint_declared,
    default_val = optional,
    struct_proxy = 'msg' )

  level = StrPrim(
    char_case = 'upper',
    default_val = "INFO",
    restricted = [ k.upper() for k,v in HINT_LEVELS_DESC.items() ],
    doc = "\n".join([ f"- ``'{k.upper()}'``: {indent_lines(2, v, start = 1)}" for k,v in HINT_LEVELS_DESC.items() ]) )

  msg = StrPrim(
    doc = "Message",
    default_val = "" )

  data = StrPrim(
    doc = "Data",
    default_val = "" )

  format = StrPrim(
    doc = "Data format",
    default_val = DATA_FORMATS[0],
    restricted = DATA_FORMATS )


  loc = HintLoc

  hints = HintList

  #-----------------------------------------------------------------------------
  def model_hint( self ):
    """Converts instance of this to instance of a regular ModelHint

    Returns
    :class:`ModelHint <partis.utils.hint.ModelHint>`
    """
    d = self._schema.encode(
      val = self,
      loc = self._loc,
      no_defaults = True )

    if d is None:
      return d

    return ModelHint.from_dict(d)
