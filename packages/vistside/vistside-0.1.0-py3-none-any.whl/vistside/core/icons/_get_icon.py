"""Getter-function for the icon of the application."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import os

from PySide6.QtGui import QIcon, QPixmap


def _getPath(actionName: str) -> str:
  """Parses the file path"""
  here = os.path.dirname(os.path.abspath(__file__))
  name = actionName.lower().replace(' ', '_')
  name = os.path.splitext(name)[0]
  fileName = '%s.png' % name
  filePath = os.path.join(here, fileName)
  if os.path.exists(filePath):
    return filePath
  return _getPath('risitas')


def getPixmap(actionName: str) -> QIcon:
  """Returns the icon of the given action."""
  filePath = _getPath(actionName)
  return QPixmap(filePath)


def getIcon(actionName: str) -> QIcon:
  """Returns the icon of the given action."""
  return QIcon(getPixmap(actionName))
