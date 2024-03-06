"""GridLayout wraps the QGridLayout."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QGridLayout

from ezros.gui.shortnames import parseParent


class GridLayout(QGridLayout):
  """GridLayout wraps the QGridLayout."""

  __field_name__ = None
  __field_owner__ = None

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    QGridLayout.__init__(self, parent)
    self.setContentsMargins(2, 2, 2, 2, )
    self.setSpacing(2)

  def __set_name__(self, owner: type, name: str) -> None:
    self.__field_owner__ = owner
    self.__field_name__ = name
