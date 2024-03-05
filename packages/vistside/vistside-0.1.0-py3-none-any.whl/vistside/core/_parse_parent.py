"""The parseParent function parses positional arguments and returns the
first instance of QWidget encountered if any."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtWidgets import QWidget


def parseParent(*args) -> Optional[QWidget]:
  """The parseParent function parses positional arguments and returns the
  first instance of QWidget encountered if any."""

  for arg in args:
    if isinstance(arg, QWidget):
      return arg
