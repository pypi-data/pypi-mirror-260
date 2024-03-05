"""ConfirmDialog provides a descriptor class that inherits from QObject
enabling it to emit signals. Use the apply decorator on methods that
should require confirmation before being allowed to run. """
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Any

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog

from morevistside.widgets import AbstractDialogField


class ConfirmDialog(AbstractDialogField):
  """ConfirmDialog provides a descriptor class that inherits from QObject
  enabling it to emit signals. Use the apply decorator on methods that
  should require confirmation before being allowed to run. """

  accepted = Signal()
  rejected = Signal()

  def trustMeBro(self, *args, **kwargs) -> Callable:
    """The most outer function is called in the line above the method. """

    def decorator(callMeMaybe: Callable) -> Callable:
      """The next level receives the decorated function."""

      def wrapper(instance: object, *args2, **kwargs2) -> None:
        """The wrapper replaces the decorated function. The wrapper
        creates a dialog, connects its accepted signal to the decorated
        function. Then opens the dialog. """

        def callception() -> None:
          """Calls the method that should require confirmation."""
          return callMeMaybe(*args2, **kwargs2)

        dialog = self._createDialog(instance, callMeMaybe)
        dialog.accepted.connect(callception)
        dialog.open()

      return wrapper

    return decorator

  def _createDialog(self, instance: Any, callMeMaybe: Callable) -> QDialog:
    """Creates the dialog for the field. Please note that the dialog
    receives only the instance under consideration. """
    insName = str(instance)
    funcName = callMeMaybe.__name__
    msg = """Object: '%s' is asking for permission to invoke callable: 
    '%s'. """ % (insName, funcName)
    title = '%s.%s' % (insName, funcName)
    dialog = QDialog()
    dialog.setWindowTitle(title)
    layout = GridLayout()
    header = LabelWidget(msg)
