"""VerticalLayout wraps the QVBoxLayout."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout

from ezros.gui.shortnames import parseParent


class VerticalLayout(QVBoxLayout):
  """VerticalLayout wraps the QVBoxLayout."""

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    QVBoxLayout.__init__(self, parent)
    self.setContentsMargins(2, 2, 2, 2, )
    self.setSpacing(2)
