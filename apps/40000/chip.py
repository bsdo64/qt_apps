from PyQt5.QtCore import QRectF, QRect, Qt, QLineF
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget, QGraphicsSceneMouseEvent, QStyle
import numpy as np

class Chip(QGraphicsItem):
    def __init__(self, color: QColor, x, y):
        super().__init__()

        self.stuff = []
        self.x = x
        self.y = y
        self.color = color
        self.setZValue((x + y) % 2)

        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(0, 0, 110, 70)

    def shape(self):
        path = QPainterPath()
        path.addRect(14, 14, 82, 42)
        return path

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget=None):
        fillColor = self.color.darker(150) if (option.state & QStyle.State_Selected) else self.color

        if option.state & QStyle.State_MouseOver:
            fillColor = fillColor.lighter(125)

        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        if lod < 0.2:
            if lod < 0.125:
                painter.fillRect(QRectF(0, 0, 110, 70), fillColor)
                return

            b = painter.brush()
            painter.setBrush(fillColor)
            painter.drawRect(13, 13, 97, 57)
            painter.setBrush(b)
            return

        oldPen = painter.pen()
        pen = oldPen
        width = 0
        if option.state & QStyle.State_Selected:
            width += 2

        pen.setWidth(width)
        b = painter.brush()
        f = 120 if option.state & QStyle.State_Sunken else 100
        painter.setBrush(QBrush(fillColor.darker(f)))
        painter.drawRect(QRect(14, 14, 79, 39))
        painter.setBrush(b)

        if lod >= 1:
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawLine(15, 54, 94, 54)
            painter.drawLine(94, 53, 94, 15)
            painter.setPen(QPen(Qt.black, 0))

        if lod >= 2:
            font = QFont("Times", 10)
            font.setStyleStrategy(QFont.ForceOutline)
            painter.setFont(font)
            painter.save()
            painter.scale(0.1, 0.1)
            painter.drawText(170, 180, "Model: VSC-2000 (Very Small Chip) at {}x{}".format(self.x, self.y))
            painter.drawText(170, 200, "Serial number: DLWR-WEER-123L-ZZ33-SDSJ")
            painter.drawText(170, 220, "﻿Manufacturer: Chip Manufacturer")

        lines = []
        if lod >= 0.5:
            for i in np.arange(0, 10, 1 if lod > 0.5 else 2):
                lines.append(QLineF(18 + 7 * i, 13, 18 + 7 * i, 5))
                lines.append(QLineF(18 + 7 * i, 54, 18 + 7 * i, 62))

            for i in np.arange(0, 6, 1 if lod > 0.5 else 2):
                lines.append(QLineF(5,18 + 5 * i, 13, 18 + 5 * i))
                lines.append(QLineF(94, 18 + 5 * i, 102, 18 + 5 * i))

        if lod >= 0.4:
            lineData = [
                QLineF(25, 35, 35, 35),
                QLineF(35, 30, 35, 40),
                QLineF(35, 30, 45, 35),
                QLineF(35, 40, 45, 35),
                QLineF(45, 30, 45, 40),
                QLineF(45, 35, 55, 35),
            ]
            lines.extend(lineData)

        painter.drawLines(lines)

        if len(self.stuff) > 1:
            p = painter.pen()
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.setBrush(Qt.NoBrush)
            path = QPainterPath()
            path.moveTo(self.stuff[0])
            for i in np.arange(len(self.stuff)):
                path.lineTo(self.stuff[i])
            painter.drawPath(path)
            painter.setPen(p)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        super().mousePressEvent(event)
        self.update()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.modifiers() and Qt.ShiftModifier:
            print(event.pos())
            self.stuff.append(event.pos())
            self.update()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        super().mouseReleaseEvent(event)
        self.update()
