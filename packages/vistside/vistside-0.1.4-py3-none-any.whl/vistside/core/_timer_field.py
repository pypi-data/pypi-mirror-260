"""TimerField provides QTimer typed descriptor class"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import QTimer
from icecream import ic
from vistutils.fields import CoreDescriptor
from vistutils.waitaminute import typeMsg

from vistside.core import parseTimer

ic.configureOutput(includeContext=True)


class TimerField(CoreDescriptor):
  """TimerField provides QTimer typed descriptor class"""

  def _instantiate(self, instance: object, owner: type = None) -> Any:
    """Instantiates the field on the instance. """
    args = self._getArgs(instance)
    kwargs = self._getKwargs(instance)
    pvtName = self._getPrivateName()
    obj = parseTimer(instance, *args, **kwargs)
    if isinstance(obj, QTimer):
      return setattr(instance, pvtName, obj)
    e = typeMsg('obj', obj, QTimer)
    raise TypeError(e)
