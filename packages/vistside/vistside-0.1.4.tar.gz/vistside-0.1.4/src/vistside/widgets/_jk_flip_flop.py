"""JKFlipFlop implementing a toggle button with separate clickable areas
for activation and deactivation."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QBrush, QColor

from ezros.gui.widgets import BaseWidget


class JKFlipFlop(BaseWidget):
  """
  A toggle button widget that acts like a JK flip-flop,
  with separate buttons for activation and deactivation.
  """

  stateChanged = Signal()
  turnOn = Signal()
  turnOff = Signal()

  def __init__(self, *args, **kwargs) -> None:
    BaseWidget.__init__(self, *args, **kwargs)
    self.activateButton = QPushButton("Activate", self)
    self.deactivateButton = QPushButton("Deactivate", self)
    self.activateButton.clicked.connect(self.activate)
    self.activateButton.clicked.connect(self.turnOn.emit)
    self.activateButton.clicked.connect(self.stateChanged.emit)
    self.deactivateButton.clicked.connect(self.turnOff.emit)
    self.deactivateButton.clicked.connect(self.deactivate)
    self.deactivateButton.clicked.connect(self.stateChanged.emit)
    self.state: bool = False
    self.initUI()

  def initUI(self) -> None:
    """Initializes the user interface."""
    layout = QVBoxLayout()
    layout.addWidget(self.activateButton)
    layout.addWidget(self.deactivateButton)
    self.setLayout(layout)
    self.deactivate()

  def activate(self) -> None:
    """Activates the toggle."""
    self.state = True
    self.activateButton.setDisabled(True)
    self.deactivateButton.setDisabled(False)
    self.update()

  def deactivate(self) -> None:
    """Deactivates the toggle."""
    self.state = False
    self.activateButton.setDisabled(False)
    self.deactivateButton.setDisabled(True)
    self.update()

  def paintEvent(self, event: Any) -> None:
    """Custom paint event to visually represent the toggle state."""
    painter = QPainter(self)
    if self.state:
      painter.setBrush(QBrush(QColor(0, 255, 0)))  # Green for active
    else:
      painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red for inactive
    painter.drawRoundedRect(painter.viewport(), 8, 8)
