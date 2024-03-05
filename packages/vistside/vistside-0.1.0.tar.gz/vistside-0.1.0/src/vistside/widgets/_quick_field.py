"""QuickField provides a descriptor class requiring the owner to
explicitly decorate  the getter function and the creator function."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable


class DescriptorException(Exception):
  """DescriptorException should be raised by getters that require the
  creator function to run. They try-except block in the descriptor
  implementation will catch this exception and run the creator function. """

  def __init__(self, *args, **kwargs) -> None:
    allArgs = [*args, None, None, None, None][:4]
    ownerClass, instanceName, fieldName, descriptorClass = allArgs
    e = """Instance '%s' of type: '%s' has not yet any support for the 
    field at name: '%s', but the getter-function of the '%s' descriptor 
    class was still invoked. The creator function will now run to create 
    the missing value. The getter is then called again, but  with a 
    recursion flag that raises a recursion error if again, the name is not 
    ready. """ % (instanceName, ownerClass, fieldName, descriptorClass)
    Exception.__init__(e)


class QuickField:
  """QuickField provides a descriptor class requiring the owner to
  explicitly decorate  the getter function and the creator function. """

  __field_name__ = None
  __field_owner__ = None
  __instance_creator__ = None
  __instance_getter__ = None

  def __set_name__(self, owner: type, name: str) -> None:
    """Set the name of the field and the owner. """
    self.__field_name__ = name
    self.__field_owner__ = owner

  def _setCreator(self, creator: Callable) -> Callable:
    """Set the creator function for the field. """
    self.__instance_creator__ = creator
    return creator

  def _getCreator(self) -> Callable:
    """Get the creator function for the field. """
    return self.__instance_creator__

  def _setGetter(self, getter: Callable) -> Callable:
    """Set the getter function for the field. """
    self.__instance_getter__ = getter
    return getter

  def _getGetter(self, ) -> Callable:
    """Get the getter function for the field. """
    return self.__instance_getter__

  def __get__(self, instance: object, owner: type, **kwargs) -> object:
    """Get the field from the instance. """
    getter = self._getGetter()
    if getter is None:
      e = f"""Getter not defined for field {self.__field_name__}"""
      raise AttributeError(e)
    try:
      return getter(instance)
    except DescriptorException as d:
      creator = self._getCreator()
      if kwargs.get('_recursion', False):
        raise RecursionError(d)
      if creator is None:
        e = f"""Creator not defined for field {self.__field_name__}"""
        raise AttributeError(e)
      if callable(creator):
        creator(instance)
      return getter(instance)
