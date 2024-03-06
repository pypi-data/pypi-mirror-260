from abc import ABCMeta

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ValuedMeta( ABCMeta ):
  """Meta class for values
  """
  
  #-----------------------------------------------------------------------------
  @classmethod
  def __prepare__( mcls, name, bases, *args, **kwargs ):

    return dict()
