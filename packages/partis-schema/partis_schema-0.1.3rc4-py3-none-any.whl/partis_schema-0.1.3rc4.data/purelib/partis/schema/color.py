
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
  StrPrim,
  StrValued )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ColorValued( StrValued ):
  #-----------------------------------------------------------------------------
  @property
  def rgb(self):
    return int(self[1:3], 16), int(self[3:5], 16), int(self[5:7], 16)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Color(StrPrim):
  #-----------------------------------------------------------------------------
  def __new__( mcls,
    name,
    bases,
    namespace,
    default_val,
    **kwargs ):

    if default_val is None:
      default_val = '#000000'

    return super().__new__( mcls,
      name = name,
      bases = bases,
      namespace = namespace,
      char_case = 'upper',
      strip = True,
      pattern = r"#[0-9A-F]{6}",
      nonempty = True,
      max_lines = 1,
      max_cols = 7,
      valued_type = ColorValued,
      default_val = default_val,
      **kwargs )
