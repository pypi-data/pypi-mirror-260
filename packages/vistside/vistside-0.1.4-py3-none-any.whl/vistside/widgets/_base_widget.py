"""BaseWidget provides the lowest level of abstraction for a QWidget. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

from vistside.core import TextPen, EmptyPen, EmptyBrush, parseParent


class BaseWidget(QWidget):
  """BaseWidget provides the lowest level of abstraction for a QWidget. """

  hover = Signal()
  leave = Signal()
  leftClick = Signal()
  rightClick = Signal()
  middleClick = Signal()
  forwardClick = Signal()
  backwardClick = Signal()
  doubleClick = Signal()
  leftPressHold = Signal()
  rightPressHold = Signal()

  textPen = TextPen()
  emptyPen = EmptyPen()
  emptyBrush = EmptyBrush()

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    QWidget.__init__(self, parent)

  @staticmethod
  def getDefault(self, *args, **kwargs) -> BaseWidget:
    """Creates a default instance"""
    return BaseWidget()
