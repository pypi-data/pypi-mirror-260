"""LCDField provides a descriptor for QLCDNumber objects."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QLCDNumber
from vistutils.waitaminute import typeMsg

from morevistutils import FlexField


class LCDField(FlexField):
  """LCDField provides a descriptor for QLCDNumber objects."""

  def _instantiate(self, instance: object, owner: type = None) -> Any:
    """Instantiate the field."""
    args = [instance, self._getPrivateArgs(instance)]
    kwargs = self._getPrivateKwargs(instance)
    pvtName = self._getPrivateName()
    lcd = QLCDNumber(instance, *args, **kwargs)
    lcd.setDigitCount(7)
    setattr(instance, pvtName, lcd)

  def __set__(self, instance: Any, value: Any) -> None:
    kwargs = self._getPrivateKwargs(instance)
    """Set the field."""
    pvtName = self._getPrivateName()
    existingLCD = getattr(instance, pvtName, None)
    if existingLCD is None:
      raise AttributeError('LCDField not instantiated!')
    if isinstance(existingLCD, QLCDNumber):
      return existingLCD.display(value)
    e = typeMsg(pvtName, existingLCD, QLCDNumber)
    raise TypeError(e)

  def __get__(self, instance: object, owner: type, **kwargs) -> QLCDNumber:
    """Get the field."""
    pvtName = self._getPrivateName()
    existingLCD = getattr(instance, pvtName, None)
    if existingLCD is None:
      raise AttributeError('LCDField not instantiated!')
    if isinstance(existingLCD, QLCDNumber):
      return existingLCD
    e = typeMsg(pvtName, existingLCD, QLCDNumber)
    raise TypeError(e)
