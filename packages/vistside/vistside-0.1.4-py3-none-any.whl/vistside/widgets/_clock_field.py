"""ClockField provides a widget showing the time"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QLCDNumber
from vistutils.fields import CoreDescriptor
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg


class ClockField(CoreDescriptor):
  """ClockField provides a widget showing the time"""

  def _instantiate(self, instance: object, owner: type = None) -> Any:
    """Instantiate the field."""
    args = [instance, self._getPrivateArgs(instance)]
    kwargs = self._getPrivateKwargs(instance)
    pvtName = self._getPrivateName()
    val = QLCDNumber()
    digitKeys = stringList("""digits, count, n, digitCount""")
    digitDefault = 4
    for key in digitKeys:
      if key in kwargs:
        if isinstance(kwargs[key], int):
          val.setDigitCount(kwargs[key])
          break
    else:
      for arg in args:
        if isinstance(arg, int):
          val.setDigitCount(arg)
          break
      else:
        val.setDigitCount(digitDefault)
    setattr(instance, pvtName, val)

  def __set__(self, instance: Any, value: Any) -> None:
    """Set the field."""
    pvtName = self._getPrivateName()
    existingLCD = getattr(instance, pvtName, None)
    if existingLCD is None:
      raise AttributeError('ClockField not instantiated!')
    if isinstance(existingLCD, QLCDNumber):
      return existingLCD.display(value)
    e = typeMsg(pvtName, existingLCD, QLCDNumber)
    raise TypeError(e)
