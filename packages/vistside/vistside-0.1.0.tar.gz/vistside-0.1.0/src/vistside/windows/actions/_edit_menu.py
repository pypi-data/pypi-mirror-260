"""EditMenu provides the edit menu of the main application window"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from morevistside.windows.actions import AbstractMenu

if TYPE_CHECKING:
  pass


class EditMenu(AbstractMenu):
  """EditMenu provides the edit menu of the main application window"""

  def setupActions(self, ) -> None:
    """setupActions creates the actions for the menu."""
    self.parent().selectAllAction = self.addAction('Select All', )
    self.parent().cutAction = self.addAction('Cut', )
    self.parent().copyAction = self.addAction('Copy', )
    self.parent().pasteAction = self.addAction('Paste', )
    self.parent().undoAction = self.addAction('Undo', )
    self.parent().redoAction = self.addAction('Redo', )
