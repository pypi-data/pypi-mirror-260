"""MainStatusBar provides the status bar for the main application window. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Callable

from PySide6.QtWidgets import QStatusBar
from icecream import ic

from morevistside.core import parseParent
from morevistside.widgets import ClockWidget
from morevistutils import FlexField


class DO:
  """Connects an action to the getter on the instance ."""

  __call_function__ = None

  def __init__(self, getCall: Callable = None) -> None:
    self.__call_function__ = getCall

  def __get__(self, instance, owner) -> None:
    self.__call_function__()

  def __call__(self, callMeMaybe: Callable) -> Callable:
    """Decorator for setting the creator method for the field. """
    self.__call_function__ = callMeMaybe
    return callMeMaybe


class MainStatusBar(QStatusBar):
  """MainStatusBar provides the status bar for the main application
  window. """

  clock = FlexField(ClockWidget.getDefault)

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    QStatusBar.__init__(self, parent)

  def addPermanentWidget(self, widget: ClockWidget) -> None:
    """Adds a permanent widget to the status bar."""
    QStatusBar.addPermanentWidget(self, widget)
    ic(widget.width(), widget.height(), )
