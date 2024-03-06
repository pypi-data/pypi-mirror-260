"""AlignmentEnum specifies alignments"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self

from enum import Enum

from PySide6.QtCore import QRect, QRectF, Qt, QPoint


class AlignmentEnum(Enum):
  """Specifies alignments"""

  @classmethod
  def prime_factors(cls, n: int) -> list:
    """Return the prime factors of a positive integer"""
    if n == 1:
      return []
    if n < 0:
      return [-1, *cls.prime_factors(-n)]
    if n == 0:
      raise ValueError('0 has no prime factors')
    i = 2
    factors = []
    while i * i <= n:
      if n % i:
        i += 1
      else:
        n //= i
        factors.append(i)
    if n > 1:
      factors.append(n)
    return factors

  LEFT = 2
  RIGHT = 3
  TOP = 5
  BOTTOM = 7
  TOP_LEFT = 2 * 5
  TOP_RIGHT = 3 * 5
  BOTTOM_LEFT = 2 * 7
  BOTTOM_RIGHT = 3 * 7

  def __str__(self) -> str:
    """String Representation"""
    return self.name.lower().replace('_', ', ')

  def __add__(self, other: Any) -> Self:
    """Addition"""
    if isinstance(other, AlignmentEnum):
      return AlignmentEnum(self.value * other.value)
    if isinstance(other, int):
      return AlignmentEnum(self.value * other)
    try:
      return self + AlignmentEnum(other)
    except ValueError as valueError:
      raise TypeError from valueError

  def apply(self, sourceRect: QRect, targetRect: QRect) -> QRect:
    """Moves sourceRect to align with targetRect as defined by the enum"""
    sourceSize = sourceRect.size()
    targetSize = targetRect.size()
    sourceHeight, sourceWidth = sourceSize.height(), sourceSize.width()
    targetHeight, targetWidth = targetSize.height(), targetSize.width()
    targetCenter = targetRect.center()
    targetX, targetY = targetCenter.x(), targetCenter.y()
    sourceCenter = sourceRect.center()
    sourceX, sourceY = sourceCenter.x(), sourceCenter.y()
    if self.value % 2 == 0:  # Left
      left = 0
      right = sourceWidth
    elif self.value % 3 == 0:
      left = targetWidth - sourceWidth
      right = targetWidth
    else:
      left = targetWidth / 2 - sourceWidth / 2
      right = targetWidth / 2 + sourceWidth / 2
    if self.value % 5 == 0:  # Top
      top = 0
      bottom = sourceHeight
    elif self.value % 7 == 0:
      top = targetHeight - sourceHeight
      bottom = targetHeight
    else:
      top = targetHeight / 2 - sourceHeight / 2
      bottom = targetHeight / 2 + sourceHeight / 2
    left += targetRect.left()
    right += targetRect.left()
    top += targetRect.top()
    bottom += targetRect.top()
    return QRect(QPoint(left, top), QPoint(right, bottom))

  def toQt(self) -> Qt.AlignmentFlag:
    """Returns the equivalent Qt.AlignmentFlag"""
    if self == AlignmentEnum.LEFT:
      return Qt.AlignmentFlag.AlignLeft
    if self == AlignmentEnum.RIGHT:
      return Qt.AlignmentFlag.AlignRight
    if self == AlignmentEnum.TOP:
      return Qt.AlignmentFlag.AlignTop
    if self == AlignmentEnum.BOTTOM:
      return Qt.AlignmentFlag.AlignBottom
    if self == AlignmentEnum.TOP_LEFT:
      return Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
    if self == AlignmentEnum.TOP_RIGHT:
      return Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
    if self == AlignmentEnum.BOTTOM_LEFT:
      return Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
    if self == AlignmentEnum.BOTTOM_RIGHT:
      return Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
    raise ValueError
