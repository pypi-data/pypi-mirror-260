"""DataPaint paints data points on the widget"""
#  MIT Licence
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from math import ceil, floor
from typing import Any

from PySide6.QtCore import Qt, QRect, QPoint, QLine
from PySide6.QtGui import QPainter, QPaintEvent

from ezros.gui.factories import emptyBrush, parsePen, parseFont, parseBrush
from ezros.gui.factories import emptyPen
from ezros.gui.paint import AbstractPaint
from ezros.gui.shortnames import Silver, Black, RoundCap, SolidLine
from ezros.gui.shortnames import AliceBlue, SolidFill, OliveDrab
from ezros.rosutils import Wait, DataEcho


class DataPaint(AbstractPaint):
  """DataPaint paints data points on the widget"""

  __fallback_pen__ = None

  pointPen = Wait(parsePen, Black, 4, SolidLine, RoundCap)
  majorGridPen = Wait(parsePen, Silver, 1, SolidLine, RoundCap)
  minorGridPen = Wait(parsePen, Silver, 1, Qt.PenStyle.DashLine, RoundCap)
  borderPen = Wait(parsePen, Black, 1, SolidLine, RoundCap)
  tickLabelFont = Wait(parseFont, 'Cambria', 6, )
  tickLabelPen = Wait(parsePen, Black, 1, SolidLine, RoundCap)
  fillBrush = Wait(parseBrush, AliceBlue, SolidFill)
  tickFillBrush = Wait(parseBrush, OliveDrab, SolidFill)

  def __init__(self, *args) -> None:
    self.dataEcho = DataEcho(128)

  def callback(self, data: Any) -> None:
    """Callback for data update"""
    self.dataEcho.append(data.data)

  def _paintOp(self, event: QPaintEvent, painter: QPainter) -> None:
    """Applies the paint operation"""
    widget = painter.device()
    minorGridPen = parsePen(Silver, 1, Qt.PenStyle.DashLine)
    majorGridPen = parsePen(Silver, 1, Qt.PenStyle.SolidLine)
    borderPen = parsePen(Black, 1, Qt.PenStyle.SolidLine)
    rect = event.rect()
    width = rect.width()
    height = rect.height()
    gridSquareSize = 8
    gridWidth = width - (width % gridSquareSize)
    gridHeight = height - (height % gridSquareSize)
    leftGrid = rect.left() + ceil((width % gridSquareSize) / 2)
    rightGrid = rect.right() - floor((width % gridSquareSize) / 2)
    topGrid = rect.top() + ceil((height % gridSquareSize) / 2)
    bottomGrid = rect.bottom() - floor((height % gridSquareSize) / 2)
    painter.setBrush(emptyBrush())
    painter.setPen(borderPen)
    painter.drawRect(rect)

    data = self.dataEcho @ event.rect()
    painter.setPen(self.pointPen)
    for (i, point) in enumerate(data):
      painter.drawPoint(point)

    painter.setPen(minorGridPen)
    t = rect.left() + ceil((width % gridSquareSize) / 2)
    x = rect.top() + ceil((height % gridSquareSize) / 2)
    _c = 0
    maxRight = rect.right() - floor((width % gridSquareSize) / 2)
    maxBottom = rect.bottom() - floor((height % gridSquareSize) / 2)
    while t < maxRight or x < maxBottom:
      if not _c % 5:
        painter.setPen(majorGridPen)
      if t < rect.right() - floor((width % gridSquareSize) / 2):
        painter.drawLine(t, rect.top(), t, rect.bottom())
      if x < rect.bottom() - floor((height % gridSquareSize) / 2):
        painter.drawLine(rect.left(), x, rect.right(), x)
      if not _c % 5:
        painter.setPen(minorGridPen)
      t += gridSquareSize
      x += gridSquareSize
      _c += 1

    bottomMargin = painter.viewport().height() - rect.bottom()
    horizontalTickHeight = bottomMargin - 4
    horizontalTickWidth = rect.width()
    horizontalTickLeft = rect.left()
    horizontalTickVLine = rect.bottom() + bottomMargin / 2
    hTicks = self.dataEcho.horizontalTicks(8, rect.width(), rect.left())
    for tick in hTicks:
      label = '%.3f' % tick[0]
      place = tick[1]

  def paintOpFill(self, event: QPaintEvent, painter: QPainter) -> None:
    """Fills background"""
    rect = event.rect()
    painter.setPen(emptyPen())
    painter.setBrush(self.fillBrush)
    painter.drawRect(rect)

  def paintOpBorder(self, event: QPaintEvent, painter: QPainter) -> None:
    """Draws border on background"""
    rect = event.rect()
    painter.setPen(self.borderPen)
    painter.setBrush(emptyBrush())
    painter.drawRect(rect)

  def paintOpGrid(self, event: QPaintEvent, painter: QPainter) -> None:
    """Paints the gridlines"""
    rect = event.rect()
    width = rect.width()
    height = rect.height()
    gridSquareSize = 8
    gridWidth = width - (width % gridSquareSize)
    gridHeight = height - (height % gridSquareSize)
    leftGrid = rect.left() + ceil((width % gridSquareSize) / 2)
    rightGrid = rect.right() - floor((width % gridSquareSize) / 2)
    topGrid = rect.top() + ceil((height % gridSquareSize) / 2)
    bottomGrid = rect.bottom() - floor((height % gridSquareSize) / 2)
    painter.setPen(self.minorGridPen)
    t = rect.left() + ceil((width % gridSquareSize) / 2)
    x = rect.top() + ceil((height % gridSquareSize) / 2)
    _c = 0
    maxRight = rect.right() - floor((width % gridSquareSize) / 2)
    maxBottom = rect.bottom() - floor((height % gridSquareSize) / 2)
    while t < maxRight or x < maxBottom:
      if not _c % 5:
        painter.setPen(self.majorGridPen)
      if t < rect.right() - floor((width % gridSquareSize) / 2):
        painter.drawLine(t, rect.top(), t, rect.bottom())
      if x < rect.bottom() - floor((height % gridSquareSize) / 2):
        painter.drawLine(rect.left(), x, rect.right(), x)
      if not _c % 5:
        painter.setPen(self.minorGridPen)
      t += gridSquareSize
      x += gridSquareSize
      _c += 1

  def paintOpData(self, event: QPaintEvent, painter: QPainter) -> None:
    """Paints the data points"""
    rect = event.rect()
    data = self.dataEcho @ event.rect()
    painter.setPen(self.pointPen)
    for (i, point) in enumerate(data):
      painter.drawPoint(point)

  def paintOpHTick(self, event: QPaintEvent, painter: QPainter) -> None:
    """Paints the ticks"""
    painter.setFont(self.tickLabelFont)
    rect = event.rect()
    bottomMargin = painter.viewport().height() - rect.bottom()
    horizontalTickHeight = bottomMargin - 4
    horizontalTickWidth = rect.width()
    horizontalTickLeft = rect.left()
    horizontalTickVLine = rect.bottom() + bottomMargin / 2
    hTicks = self.dataEcho.horizontalTicks(8, rect.width(), rect.left())
    labelSize = painter.fontMetrics().boundingRect('%.2fs' % 69).size()
    for tick in hTicks:
      label = '%.2fs' % tick[0]
      labelRect = QRect(QPoint(0, 0), labelSize)
      labelRect.moveCenter(QPoint(tick[1], horizontalTickVLine))
      painter.setPen(self.tickLabelPen)
      painter.setFont(self.tickLabelFont)
      tickTop = labelRect.top()
      rect.bottom()
      tickLine = QLine(tick[1], rect.bottom(), tick[1], tickTop)
      painter.drawLine(tickLine)
      painter.drawText(labelRect, label)

  def paintOpVTick(self, event: QPaintEvent, painter: QPainter) -> None:
    """Paints the ticks"""
    painter.setFont(self.tickLabelFont)
    labelSize = painter.fontMetrics().boundingRect('%.2f' % 420).size()
    rect = event.rect()
    verticalTickLine = rect.left() - labelSize.width()
    vTicks = self.dataEcho.verticalTicks(4, rect.height(), rect.top())
    for tick in vTicks:
      label = '%.2f' % tick[0]
      labelRect = QRect(QPoint(0, 0), labelSize)
      labelRect.moveCenter(QPoint(verticalTickLine, tick[1]))
      painter.setPen(self.tickLabelPen)
      painter.setFont(self.tickLabelFont)
      tickLine = QLine(rect.left(), tick[1], labelRect.right(), tick[1])
      painter.setBrush(self.tickFillBrush)
      painter.drawLine(tickLine)
      painter.drawText(labelRect, label)

  def paintOp(self, event: QPaintEvent, painter: QPainter) -> None:
    """Applies the paint operation"""
    self.paintOpFill(event, painter)
    self.paintOpBorder(event, painter)
    self.paintOpGrid(event, painter)
    self.paintOpData(event, painter)
    self.paintOpHTick(event, painter)
    self.paintOpVTick(event, painter)
