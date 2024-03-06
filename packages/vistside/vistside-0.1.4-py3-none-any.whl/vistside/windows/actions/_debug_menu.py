"""DebugMenu provides a debug menu for development purposes."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from morevistside.windows.actions import AbstractMenu


class DebugMenu(AbstractMenu):
  """DebugMenu provides a debug menu for development purposes."""

  def setupActions(self, ) -> None:
    """setupActions creates the actions for the menu."""
    self.parent().debug01Action = self.addAction('Debug01', )
    self.parent().debug02Action = self.addAction('Debug02', )
    self.parent().debug03Action = self.addAction('Debug03', )
    self.parent().debug04Action = self.addAction('Debug04', )
    self.parent().debug05Action = self.addAction('Debug05', )
    self.parent().debug06Action = self.addAction('Debug06', )
    self.parent().debug07Action = self.addAction('Debug07', )
    self.parent().debug08Action = self.addAction('Debug08', )
    self.parent().debug09Action = self.addAction('Debug09', )
    self.parent().debug10Action = self.addAction('Debug10', )
