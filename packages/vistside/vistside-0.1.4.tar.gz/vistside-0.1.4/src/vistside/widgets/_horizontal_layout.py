"""HorizontalLayout wraps the QHBoxLayout."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout

from ezros.gui.shortnames import parseParent


class HorizontalLayout(QHBoxLayout):
  """HorizontalLayout wraps the QHBoxLayout."""

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    QHBoxLayout.__init__(self, parent)
    self.setContentsMargins(2, 2, 2, 2, )
    self.setSpacing(2)
