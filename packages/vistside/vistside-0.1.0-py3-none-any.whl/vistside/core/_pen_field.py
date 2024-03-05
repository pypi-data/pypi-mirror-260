"""PenField provides a descriptor class for instances of QPen."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QPen

from morevistutils import CoreDescriptor


class PenField(CoreDescriptor):
  """The PenField class provides a descriptor for instances of QPen."""

  def _instantiate(self, instance: object) -> None:
    """Instantiates the field."""
    pen = QPen(*self._getArgs(), **self._getKwargs())
    setattr(instance, self._getPrivateName(), pen)

  def __set__(self, instance: object, value: Any) -> None:
    """Sets the field."""

    if not isinstance(value, QPen):
      e = """Value must be an instance of QPen!"""
      raise TypeError(e)
    setattr(instance, self._getPrivateName(), value)
