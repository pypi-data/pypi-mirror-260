"""LabelWidget provides a widget for displaying labels. This is intended
for short names or descriptions rather than longer text."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor, QPaintEvent, QPainter

from morevistside.core import FontField, \
  PenField, \
  Black, \
  SolidLine, \
  BrushField, Orange, SolidFill
from morevistside.widgets import FillWidget
from morevistutils import TextField


class LabelWidget(FillWidget):
  """LabelWidget provides a widget for displaying labels. This is intended
  for short names or descriptions rather than longer text."""

  innerText = TextField('innerText', str, 'Label')
  textFont = FontField('Courier', 18)
  fontPen = PenField(Black, 1, SolidLine)
  fillBrush = BrushField(Orange, SolidFill)
  borderPen = PenField(QColor(0, 144, 255, 255), 2, SolidLine)

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the LabelWidget."""
    FillWidget.__init__(self, *args, **kwargs)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Paints the widget."""
    painter = QPainter()
    painter.begin(self)
    painter.setPen(self.emptyPen)
    painter.setBrush(self.fillBrush)
    painter.drawRoundedRect(self.rect(), 4, 4, )
    painter.setPen(self.borderPen)
    painter.setBrush(self.emptyBrush)
    painter.drawRoundedRect(self.rect(), 4, 4, )
    painter.setFont(self.textFont)
    painter.setPen(self.fontPen)
    
    painter.end()
