"""HelpMenu provides the help menu of the main application window"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from morevistside.windows.actions import AbstractMenu


class HelpMenu(AbstractMenu):
  """HelpMenu provides the help menu of the main application window"""

  def setupActions(self, ) -> None:
    """setupActions creates the actions for the menu."""
    self.parent().aboutAction = self.addAction('About', )
    self.parent().helpAction = self.addAction('Help', )
    self.parent().aboutQtAction = self.addAction('About Qt', )
