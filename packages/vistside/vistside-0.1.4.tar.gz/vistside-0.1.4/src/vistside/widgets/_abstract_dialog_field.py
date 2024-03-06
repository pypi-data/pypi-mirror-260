"""DialogField provides a descriptor class for dialog boxes. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable

from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QDialog
from vistutils.waitaminute import typeMsg


class AbstractDialogField(QObject):
  """DialogField provides a descriptor class for dialog boxes. """

  __field_name__: str = None
  __field_owner__: type = None
  __positional_args__: list = None
  __keyword_args__: dict = None

  finished = Signal(int)

  def __set_name__(self, owner: type, name: str) -> None:
    """Invoked automatically after the owner is created, but before the
    owner is initiated. Let Owner be a class derived from a custom
    metaclass Meta, let Field be a descriptor derived from type and let
    field be an instance of Field owned by owner. Then the following
    ordering of events occur:
    1.  namespace = Meta.__prepare__(mcls, name, bases, ) creates the
        namespace object
    2.  field = Field() creates the field instance
    3   Owner = type.__new__(mcls, name, bases, namespace) creates the
        owner class
    4.  field.__set_name__(Owner, name) sets the field name and owner
    5.  type.__init__(Owner, name, bases, namespace) initiates the owner
        class"""
    self.__field_name__ = name
    self.__field_owner__ = owner
    setattr(owner, self._getSlotName(), Signal())

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the descriptor."""
    QObject.__init__(self, *args, **kwargs)
    self.__positional_args__ = [*args, ]
    self.__keyword_args__ = {**kwargs, }

  def getArgs(self) -> list:
    """Returns the positional arguments."""
    return self.__positional_args__

  def getKwargs(self) -> dict:
    """Returns the keyword arguments."""
    return self.__keyword_args__

  def _getFieldName(self) -> str:
    """Getter-function for getting the field name."""
    if self.__field_name__ is None:
      e = """Field name not defined!"""
      raise AttributeError(e)
    if isinstance(self.__field_name__, str):
      return self.__field_name__
    e = typeMsg('__field_name__', self.__field_name__, str)
    raise TypeError(e)

  def _getFieldOwner(self) -> type:
    """Getter-function for getting the field owner."""
    if self.__field_owner__ is None:
      e = """Field owner not defined!"""
      raise AttributeError(e)
    if isinstance(self.__field_owner__, type):
      return self.__field_owner__
    e = typeMsg('__field_owner__', self.__field_owner__, type)
    raise TypeError(e)

  def _getPrivateName(self) -> str:
    """Getter-function for getting the private name."""
    return '_%s' % self._getFieldName()

  def _getSlotName(self) -> str:
    """Getter-function for getting the slot name."""
    return '__%s_finished__' % self._getFieldName()

  def __get__(self, instance: object, owner: type) -> Any:
    """Returns the class type."""
    if instance is None:
      return self
    pvtName = self._getPrivateName()
    args = [instance, *self.getArgs()]
    kwargs = self.getKwargs()
    dialog = self._createDialog(*args, **kwargs)
    dialog.finished.connect()
    return getattr(instance, pvtName, None)

  @abstractmethod
  def _createDialog(self, instance: Any, callMeMaybe: Callable) -> QDialog:
    """Creates the dialog box."""
