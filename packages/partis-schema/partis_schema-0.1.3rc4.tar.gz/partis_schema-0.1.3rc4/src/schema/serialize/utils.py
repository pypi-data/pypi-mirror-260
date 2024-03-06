from partis.schema_meta.base import (
  Loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def as_load( loads ):

  def load(
    file,
    *args,
    **kwargs ):

    if 'loc' not in kwargs:
      kwargs['loc'] = Loc(
        filename = file )

    with open( file, 'rb' ) as fp:
      src = fp.read()

    src = src.decode( 'utf-8', errors = 'replace' )

    return loads( src, *args, **kwargs )

  return load

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def as_dump( dumps ):

  def dump(
    file,
    *args,
    **kwargs ):

    src = dumps(
      *args,
      **kwargs )

    src = src.encode( 'utf-8', errors = 'replace' )

    with open( file, 'wb' ) as fp:
      fp.write( src )

  return dump
