"""TextRect places text on the given rectangle"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPaintEvent, QPainter, QFontMetricsF, QPaintDevice
from vistutils.waitaminute import typeMsg

from ezros.gui.factories import textPen, parseFont, parseColor
from ezros.gui.paint import AbstractPaint
from ezros.gui.shortnames import Black
from ezros.rosutils import Wait


class TextRect(AbstractPaint):
  """TextRect places text on the given rectangle"""

  __self_font_metrics__ = None
  __recent_painter__ = None

  textLine = Wait(textPen, )
  textFont = Wait(parseFont, 'Arial', 10)
  fontMetrics = Wait()

  def paintOp(self,
              event: QPaintEvent,
              painter: QPainter,
              text: str = None) -> None:
    """Prints text found in the painter device"""
    if text is None:
      if getattr(painter.device(), 'innerText', None) is not None:
        text = painter.device().innerText
        if not isinstance(text, str):
          text = str(text)
    painter.setPen(self.textLine)
    painter.setFont(self.textFont)
    painter.drawText(event.rect(), text)

  @fontMetrics.CREATE
  def _getFontMetrics(self, **kwargs) -> QFontMetricsF:
    """Getter for the font metrics"""
    if self.__self_font_metrics__ is None:
      if kwargs.get('recursion', False):
        raise RecursionError
      self.__self_font_metrics__ = QFontMetricsF(self.textFont)
      return self._getFontMetrics(recursion=True)
    return self.__self_font_metrics__

  def __init__(self, *args, **kwargs) -> None:
    color, font = None, None
    color = parseColor(*args, **kwargs, strict=False)
    font = parseFont(*args, **kwargs, strict=False)
