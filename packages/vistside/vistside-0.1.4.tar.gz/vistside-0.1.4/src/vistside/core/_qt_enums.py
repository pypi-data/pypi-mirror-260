"""Common names from Qt."""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QSizePolicy

#  Timer types
Precise = Qt.TimerType.PreciseTimer
Coarse = Qt.TimerType.CoarseTimer
VeryCoarse = Qt.TimerType.VeryCoarseTimer
#  Alignments
Left = Qt.AlignmentFlag.AlignLeft
Right = Qt.AlignmentFlag.AlignRight
Top = Qt.AlignmentFlag.AlignTop
Bottom = Qt.AlignmentFlag.AlignBottom
Center = Qt.AlignmentFlag.AlignCenter
HCenter = Qt.AlignmentFlag.AlignHCenter
VCenter = Qt.AlignmentFlag.AlignVCenter
#  Pen styles
SolidLine = Qt.PenStyle.SolidLine
DashLine = Qt.PenStyle.DashLine
DotLine = Qt.PenStyle.DotLine
DashDotLine = Qt.PenStyle.DashDotLine
DashDotDotLine = Qt.PenStyle.DashDotDotLine
EmptyLine = Qt.PenStyle.NoPen
RoundCap = Qt.PenCapStyle.RoundCap
FlatCap = Qt.PenCapStyle.FlatCap
SquareCap = Qt.PenCapStyle.SquareCap
#  Brush styles
SolidFill = Qt.BrushStyle.SolidPattern
#  Size policy
Spread = QSizePolicy.Policy.MinimumExpanding
Fixed = QSizePolicy.Policy.Fixed
Tight = QSizePolicy.Policy.Maximum
#  Mouse buttons
MouseBtn = Qt.MouseButton
NoBtn = Qt.MouseButton.NoButton
LeftBtn = Qt.MouseButton.LeftButton
RightBtn = Qt.MouseButton.RightButton
MiddleBtn = Qt.MouseButton.MiddleButton
NextBtn = Qt.MouseButton.ForwardButton
BackBtn = Qt.MouseButton.BackButton
#  Mouse events
Mouse = QMouseEvent
BtnDown = QEvent.Type.MouseButtonPress
BtnUp = QEvent.Type.MouseButtonRelease
MouseMove = QEvent.Type.MouseMove

__all__ = ['Precise', 'Coarse', 'VeryCoarse', 'Left', 'Right', 'Top',
           'Bottom', 'Center', 'HCenter', 'VCenter', 'SolidLine', 'DashLine',
           'DotLine', 'DashDotLine', 'DashDotDotLine', 'EmptyLine',
           'RoundCap', 'FlatCap', 'SquareCap', 'SolidFill', 'Spread',
           'Fixed', 'Tight', 'NoBtn', 'MouseBtn', 'LeftBtn', 'RightBtn',
           'MiddleBtn', 'NextBtn', 'BackBtn']
