"""BorderRect draws an outline on the update rectangle, without fill."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QPainter

from ezros.gui.factories import emptyBrush, parsePen
from ezros.gui.paint import AbstractPaint
from ezros.gui.shortnames import Black


# from _dep.morevistutils import Wait


class BorderRect(AbstractPaint):
  """BorderRect draws an outline on the update rectangle, without fill."""

  # pen = Wait(parsePen, Black, 2)

  def paintOp(self, event: QPaintEvent, painter: QPainter) -> None:
    """Applies the paint operation"""
    painter.setPen(self.pen)
    painter.setBrush(emptyBrush())
    painter.drawRect(event.rect())

  def __init__(self, *args, **kwargs) -> None:
    self.pen = parsePen(*args, Black, 2, **kwargs)
