"""ClockWidget provides a clock widget for the main application window"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from datetime import datetime

from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QLabel, QVBoxLayout, QLCDNumber

from morevistside.core import TimerField, Coarse, parseParent
from morevistside.widgets import BaseWidget, LCDField


class ClockWidget(BaseWidget):
  """ClockWidget provides a clock widget for the main application window"""

  baseLayout = None
  lcd = None
  label = None
  recentTime = None
  timer = TimerField(200, Coarse, singleShot=False)

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    BaseWidget.__init__(self, parent)
    self.setMinimumWidth(128)
    self.setMinimumHeight(32)

  def _clockStep(self, *args, **kwargs) -> None:
    """Updates the clock"""
    rightNow = datetime.now()
    if rightNow != self.recentTime:
      # self.lcd.display(rightNow.strftime('%H:%M:%S'))
      self.label.setText('Time: %s' % rightNow.strftime('%H:%M:%S'))
      self.label.update()
      self.recentTime = rightNow

  def show(self) -> None:
    """Shows the widget"""
    self.baseLayout = QVBoxLayout()
    self.lcd = QLCDNumber(8, )
    self.label = QLabel('Time: ', self)
    self.label.setFixedSize(128, 32)
    self.baseLayout.addWidget(self.label)
    self.setLayout(self.baseLayout)
    self.timer.timeout.connect(self._clockStep)
    self.timer.start()
    BaseWidget.show(self)

  def getDefault(self, *args, **kwargs, ) -> ClockWidget:
    """Creates a default instance"""
    return ClockWidget(*args, **kwargs)
