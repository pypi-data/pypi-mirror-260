"""FilesMenu subclasses QMenu and provides a menu for file actions. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from morevistside.windows.actions import AbstractMenu

if TYPE_CHECKING:
  pass


class FilesMenu(AbstractMenu):
  """FilesMenu subclasses QMenu and provides a menu for file actions. """

  def setupActions(self, ) -> None:
    """setupActions creates the actions for the menu."""
    self.parent().newAction = self.addAction('New', )
    self.parent().openAction = self.addAction('Open', )
    self.parent().saveAction = self.addAction('Save', )
    self.parent().saveAsAction = self.addAction('Save As', )
    self.parent().exitAction = self.addAction('Exit', )
