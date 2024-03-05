"""EmptyBrush provides a descriptor returning the empty brush"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush

from morevistutils import StaticField


class EmptyBrush(StaticField):
  """EmptyBrush provides a descriptor returning the empty brush"""

  def __init__(self, ) -> None:
    brush = QBrush()
    brush.setColor(QColor(0, 0, 0, 0, ))
    brush.setStyle(Qt.BrushStyle.NoBrush)
    StaticField.__init__(self, brush)
