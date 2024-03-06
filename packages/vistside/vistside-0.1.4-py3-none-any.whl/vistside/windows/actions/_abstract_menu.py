"""AbstractMenu provides a base class for the menus of the main
application window. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from vistutils.parse import maybe
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from morevistside.core import KeyboardShortcuts, parseParent
from morevistside.core.icons import getIcon


class AbstractMenu(QMenu):
  """AbstractMenu provides a base class for the menus of the main
  application window. """

  @staticmethod
  def _parseTitle(*args, **kwargs) -> str:
    """Parses argument to find title"""
    titleKeys = stringList("""title, menuTitle, menu, name, titleName""")
    titleKwarg = None
    for key in titleKeys:
      if key in kwargs:
        val = kwargs.get(key)
        if isinstance(val, str):
          titleKwarg = val
          break
    titleArg = [*[arg for arg in args if isinstance(arg, str)], None][0]
    title = maybe(titleKwarg, titleArg, )
    if isinstance(title, str):
      return title
    e = typeMsg('title', title, str)
    raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args)
    title = self._parseTitle(*args, **kwargs)
    QMenu.__init__(self, title, parent)
    self.menuAction().setIconText('title')

  def addAction(self, *args, ) -> QAction:
    """addAction creates a new action and adds it to the menu. """
    name = args[0]
    try:
      icon = getIcon(name)
    except FileNotFoundError as e:
      icon = getIcon('risitas')
    keyboard = KeyboardShortcuts[name.replace(' ', '_').lower()]
    action = QAction(icon, name, self)
    action.setShortcut(keyboard)
    action.setShortcutVisibleInContextMenu(True)
    QMenu.addAction(self, action)
    return action
