"""MouseAware subclasses BaseWidget and provides methods relating to mouse
events"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QMouseEvent

from ezros.gui.shortnames import NoBtn
from ezros.gui.widgets import BaseWidget, ButtonField
from _dep.morevistutils import Flag, IntField
from ezros.gui.shortnames import MouseBtn, LeftBtn, RightBtn, \
  MiddleBtn, NextBtn, BackBtn


class MouseAware(BaseWidget):
  """The MouseAware class provides methods relating to mouse events"""

  buttonClick = Signal(MouseBtn)
  doubleClick = Signal(MouseBtn)
  mouseEnter = Signal()
  mouseLeave = Signal()
  underMouse = Flag(False)
  pressedButton = ButtonField(NoBtn)
  DoubleButton = ButtonField(NoBtn)
  mouseLocalX = IntField(0)
  mouseLocalY = IntField(0)

  leftSingleClick = Signal()
  middleSingleClick = Signal()
  rightSingleClick = Signal()
  nextSingleClick = Signal()
  backSingleClick = Signal()
  leftDoubleClick = Signal()
  rightDoubleClick = Signal()
  middleDoubleClick = Signal()
  nextDoubleClick = Signal()
  backDoubleClick = Signal()

  @Slot(MouseBtn)
  def emitSingleClick(self, button: MouseBtn) -> None:
    """Filter click signals."""
    if button == LeftBtn:
      self.leftSingleClick.emit()
    if button == RightBtn:
      self.rightSingleClick.emit()
    if button == MiddleBtn:
      self.middleSingleClick.emit()
    if button == BackBtn:
      self.backSingleClick.emit()
    if button == NextBtn:
      self.nextSingleClick.emit()

  @Slot(MouseBtn)
  def emitDoubleClick(self, button: MouseBtn) -> None:
    """Filter double click signals."""
    if button == LeftBtn:
      self.leftDoubleClick.emit()
    if button == RightBtn:
      self.rightDoubleClick.emit()
    if button == MiddleBtn:
      self.middleDoubleClick.emit()
    if button == BackBtn:
      self.backDoubleClick.emit()
    if button == NextBtn:
      self.nextDoubleClick.emit()

  def mousePressEvent(self, event: QMouseEvent) -> None:
    """Mouse press event handler."""
    if not self.underMouse:
      return
    self.pressedButton = event.button()

  def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
    """Mouse double click event handler."""
    if not self.underMouse:
      return
    if event.button() == self.pressedButton:
      self.DoubleButton = event.button()
    else:
      self.DoubleButton = NoBtn

  def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Mouse release event handler."""
    if not self.underMouse or event.button() == NoBtn:
      return
    if event.button() == self.DoubleButton:
      self.DoubleButton = NoBtn
      self.doubleClick.emit(event.button())
    if event.button() == self.pressedButton:
      self.buttonClick.emit(event.button())
    self.pressedButton = NoBtn

  def enterEvent(self, event: QMouseEvent) -> None:
    """Mouse enter event handler."""
    self.underMouse = True
    self.mouseEnter.emit()
    mousePos = event.pos()
    self.mouseLocalX = mousePos.x()
    self.mouseLocalY = mousePos.y()

  def leaveEvent(self, event: QMouseEvent) -> None:
    """Mouse leave event handler."""
    self.underMouse = False
    self.mouseLeave.emit()
    mousePos = event.pos()
    self.mouseLocalX = -mousePos.x()
    self.mouseLocalY = -mousePos.y()

  def mouseMoveEvent(self, event) -> None:
    """Mouse move event handler."""
    mousePos = event.pos()
    self.mouseLocalX = mousePos.x()
    self.mouseLocalY = mousePos.y()
