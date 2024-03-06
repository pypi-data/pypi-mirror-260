"""ToggleButton implements a toggle button that is easy to deactivate but
slow to activate. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import QTimer, Qt, QPointF

from ezros.gui.shortnames import parseParent
from ezros.gui.widgets import BaseWidget


class SafetyToggleButton(BaseWidget):
  """SafetyToggleButton implements a toggle button that is easy to
  deactivate, but difficult to activate."""

  __activate_time__ = 1000  # Time in ms to activate
  __time_steps__ = 50  # Number of steps to activate

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    BaseWidget.__init__(self, parent)
    self.isHigh = False  # Toggle state
    self.progress = 0.0  # Progress of the timer
    self.timer = QTimer(self)  # Timer for delay
    self.timer.setInterval(self.getStepTime())  # Update every 100 ms
    self.timer.timeout.connect(self.updateProgress)
    self.setMinimumSize(100, 100)

  def getStepTime(self) -> int:
    """Getter-function for the step time"""
    return int(round(self.__activate_time__ / self.__time_steps__))

  def getFullTime(self) -> int:
    """Getter-function for the full time"""
    return self.__activate_time__

  def mousePressEvent(self, event) -> None:
    """Starts the timer on mouse press."""
    if event.button() == Qt.LeftButton:
      self.progress = 0.0
      self.timer.start()

  def mouseReleaseEvent(self, event) -> None:
    """Stops the timer and toggles state if held long enough."""
    if self.isHigh:
      self.isHigh = False
      self.timer.stop()
      return self.update()
    if self.progress >= 1.0:
      self.isHigh = not self.isHigh
    self.progress = 0.0
    self.update()

  def updateProgress(self) -> None:
    """Updates the progress and repaints the widget."""
    self.progress += self.getStepTime()
    if self.progress >= self.getFullTime():
      self.timer.stop()
    self.update()

  def getProgression(self, ) -> float:
    """Getter for progression."""
    return min(1.00, self.progress / self.getFullTime())

  def paintEvent(self, event) -> None:
    """Draws the toggle button with progress indication."""
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)

    # Draw the circle around the button
    pen = QPen(Qt.black, 2)
    brush = QBrush(Qt.white)
    painter.setPen(pen)
    radius = min(self.width(), self.height()) / 2 - 10
    center = QPointF(self.width() / 2, self.height() / 2)
    painter.drawEllipse(center, radius, radius)

    # Draw progress
    if self.getProgression() > 0:
      pen.setColor(Qt.green)
      painter.setPen(pen)
      brush = QBrush(Qt.green)
      painter.setBrush(brush)
      angle = 360 * self.getProgression()
      painter.drawPie(center.x() - radius, center.y() - radius, radius * 2,
                      radius * 2, 90 * 16, -angle * 16)

    # Draw the toggle state
    pen.setColor(Qt.blue if self.isHigh else Qt.red)
    painter.setPen(pen)
    brush.setColor(Qt.blue if self.isHigh else Qt.red)
    painter.setBrush(brush)
    painter.drawEllipse(center, radius / 2, radius / 2)
