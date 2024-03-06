"""AbstractPaint provides the abstract baseclass for the encapsulated
painting operations"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Self

from PySide6.QtGui import QPainter, QPaintEvent
from vistutils.fields import Field

if TYPE_CHECKING:
  from ezros.gui.widgets import PaintWidget

  PW = PaintWidget

Sig = tuple[type]


class AbstractPaint(Field):
  """AbstractPaint provides the abstract baseclass for the encapsulated
  painting operations"""

  @abstractmethod
  def paintOp(self, event: QPaintEvent, painter: QPainter) -> None:
    """Applies the paint operation"""

  def __set_name__(self, owner: PaintWidget, name: str) -> None:
    owner.appendHookedPaint(self)

  def __get__(self, instance: PW, owner: type[PW]) -> Self:
    return self
