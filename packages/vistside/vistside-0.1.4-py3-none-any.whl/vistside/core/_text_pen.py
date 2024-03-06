"""TextPenField provides a descriptor for the QPen used to print text."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtGui import QColor, QPen
from vistutils.fields import StaticField
from vistutils.parse import maybe
from vistutils.waitaminute import typeMsg

from vistside.core import parseColor, SolidLine


class TextPen(StaticField):
  """TextPenField provides a descriptor for the QPen used to print text."""

  __font_color__ = None
  __fallback_color__ = QColor(0, 0, 0, 255)

  def __init__(self, *args, **kwargs) -> None:
    col = maybe(parseColor(*args, **kwargs), self.__fallback_color__)
    if isinstance(col, QColor):
      self.__font_color__ = col
    else:
      e = typeMsg('col', col, QColor)
      raise TypeError(e)
    pen = QPen()
    pen.setStyle(SolidLine)
    pen.setColor(self.__font_color__)
    pen.setWidth(1)
    StaticField.__init__(self, pen)

  def __set__(self, instance: object, value: Any) -> None:
    if isinstance(value, QColor):
      self.__font_color__ = value
      pen = self.__field_value__
      if isinstance(pen, QPen):
        pen.setColor(self.__font_color__)
      else:
        e = typeMsg('pen', pen, QPen)
        raise TypeError(e)
      pen.setColor(self.__font_color__)
      setattr(self, '__field_value__', pen)
    else:
      try:
        self.__set__(instance, parseColor(value))
      except Exception as exception:
        e = typeMsg('value', value, QColor)
        raise TypeError(e) from exception
