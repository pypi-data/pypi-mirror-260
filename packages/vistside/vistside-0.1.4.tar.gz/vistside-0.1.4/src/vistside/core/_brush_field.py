"""BrushField provides a descriptor class for instances of QBrush."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QBrush
from vistutils.fields import CoreDescriptor

from vistside.core import parseBrush


class BrushField(CoreDescriptor):
  """The BrushField class provides a descriptor for instances of QBrush."""

  def _instantiate(self, instance: object) -> None:
    """Instantiates the field."""
    brush = parseBrush(*self._getArgs(), **self._getKwargs())
    setattr(instance, self._getPrivateName(), brush)

  def __set__(self, instance: object, value: Any) -> None:
    """Sets the field."""

    if not isinstance(value, QBrush):
      e = """Value must be an instance of QBrush!"""
      raise TypeError(e)
    setattr(instance, self._getPrivateName(), value)
