"""This file provides standard keyboard shortcuts. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QKeySequence


class KeyboardShortcuts:
  """This class provides standard keyboard shortcuts. """

  __output_mode__ = str

  # File menu
  new = "Ctrl+N"
  open = "Ctrl+O"
  save = "Ctrl+S"
  save_as = "Ctrl+Shift+S"
  close = "Ctrl+W"
  quit = "Ctrl+Q"

  # Edit menu
  undo = "Ctrl+Z"
  redo = "Ctrl+Y"
  cut = "Ctrl+X"
  copy = "Ctrl+C"
  paste = "Ctrl+V"
  select_all = "Ctrl+A"

  # Help menu
  debug01 = 'F1'
  debug02 = 'F2'
  debug03 = 'F3'
  debug04 = 'F4'
  debug05 = 'F5'
  debug06 = 'F6'
  debug07 = 'F7'
  debug08 = 'F8'
  debug09 = 'F9'
  debug10 = 'F10'

  about = 'F11'
  about_qt = 'F12'

  @classmethod
  def getQKey(cls, name: str, **kwargs) -> QKeySequence:
    """getQKey returns the QKeySequence for a keyboard shortcut. """
    shortcutString = getattr(cls, name, '')
    out = QKeySequence.fromString(shortcutString)
    if out:
      return out
    if kwargs.get('_recursion', False):
      raise RecursionError
    return cls.getQKey(name.lower(), _recursion=True)

  @classmethod
  def __class_getitem__(cls, *args, **kwargs) -> QKeySequence:
    """__call__ returns the QKeySequence for a keyboard shortcut. """
    return cls.getQKey(*args, **kwargs)
