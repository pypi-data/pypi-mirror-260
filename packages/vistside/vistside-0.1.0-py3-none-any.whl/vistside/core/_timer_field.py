"""TimerField provides QTimer typed descriptor class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any
from warnings import warn

from PySide6.QtCore import QTimer
from icecream import ic
from vistutils.text import stringList, monoSpace
from vistutils.waitaminute import typeMsg

from morevistside.core import parseTimer
from morevistutils import FlexField

ic.configureOutput(includeContext=True)


class TimerField(FlexField):
  """TimerField provides QTimer typed descriptor class"""

  def __class_getitem__(cls, item) -> Never:
    """Disabled"""
    raise TypeError("TimerField does not support __class_getitem__")

  def _setCreator(self, *_) -> Never:
    """Decorator for setting the creator method for the field. """
    raise TypeError("TimerField does not support custom creators")

  def _getCreator(self, *_) -> Never:
    """Decorator for setting the creator method for the field. """
    raise TypeError("TimerField does not support custom creators")

  def _instantiate(self, instance: object, owner: type = None) -> Any:
    """Instantiates the field on the instance. """
    args = self._getArgs(instance)
    kwargs = self._getKwargs(instance)
    pvtName = self._getPrivateName()
    obj = parseTimer(instance, *args, **kwargs)
    setattr(instance, pvtName, self._typeGuard(obj))
