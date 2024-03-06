"""The FillRect factory creates a function applying solid paint to the
underlying device"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Self

from PySide6.QtGui import QPainter, QPaintEvent

from ezros.gui.factories import emptyPen, parseBrush, parseColor
from ezros.gui.paint import AbstractPaint
from ezros.gui.shortnames import Silver
from ezros.rosutils import Wait


# from _dep.morevistutils import Wait


class FillRect(AbstractPaint):
  """The FillRect factory creates a function applying solid paint to the
  underlying device"""

  brush = Wait(parseBrush, Silver, )

  def __init__(self, *args, **kwargs) -> None:
    pass
    # color = parseColor(*args, **kwargs)

  def paintOp(self, event: QPaintEvent, painter: QPainter) -> None:
    """Fills the rect with the given brush"""
    painter.setBrush(self.brush)
    painter.setPen(emptyPen())
    painter.drawRect(event.rect())

  def update(self, *args, **kwargs) -> Self:
    """Updates the paint settings. """
    if args:
      color = parseColor(*args, **kwargs)
      self.brush = parseBrush(color)
    return self
