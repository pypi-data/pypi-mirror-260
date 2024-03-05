"""EmptyPen provides a descriptor returning the empty pen"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QColor

from morevistutils import StaticField


class EmptyPen(StaticField):
  """EmptyPen provides a descriptor returning the empty pen"""

  def __init__(self, ) -> None:
    pen = QPen()
    pen.setColor(QColor(0, 0, 0, 0, ))
    pen.setStyle(Qt.PenStyle.NoPen)
    StaticField.__init__(self, pen)
