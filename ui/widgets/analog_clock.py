# ui/widgets/analog_clock.py
# Self-contained Analog Clock widget (PySide6)

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QRectF, Qt
from PySide6.QtGui import QPainter, QColor, QPen
from datetime import datetime


class AnalogClock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(65, 65)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        side = min(self.width(), self.height())
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 65.0, side / 65.0)

        painter.setPen(QPen(QColor("#1e40af"), 2.5))
        painter.setBrush(QColor("#f8fafc"))
        painter.drawEllipse(QRectF(-30, -30, 60, 60))

        time = datetime.now()
        hour = time.hour % 12
        minute = time.minute
        second = time.second

        painter.setPen(QPen(QColor("#1e40af"), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.save()
        painter.rotate(30.0 * (hour + minute / 60.0))
        painter.drawLine(0, 0, 0, -16)
        painter.restore()

        painter.setPen(QPen(QColor("#334155"), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.save()
        painter.rotate(6.0 * minute)
        painter.drawLine(0, 0, 0, -22)
        painter.restore()

        painter.setPen(QPen(QColor("#ef4444"), 1.5))
        painter.save()
        painter.rotate(6.0 * second)
        painter.drawLine(0, 4, 0, -25)
        painter.restore()

        painter.setBrush(QColor("#1e40af"))
        painter.drawEllipse(QRectF(-2.5, -2.5, 5, 5))