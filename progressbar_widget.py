import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget,
    QTextEdit, QLineEdit, QMessageBox, QFormLayout, QFileDialog, QCheckBox, QComboBox
)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


# Defines the Progress bar
class ProgressBarWidget(QWidget):
    def __init__(self, progress=0, parent=None):
        super().__init__(parent)
        self.progress = progress
        self.stages = ["Input", "Preprocessing", "AI Model", "Visualization", "Output"]
        self.setMinimumHeight(100)

    # Paints the progress bar
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        num_stages = len(self.stages)
        circle_diameter = min(40, height * 0.4)
        connector_height = circle_diameter / 4
        spacing = (width - num_stages * circle_diameter) / (num_stages + 1)  # Space between circles

        # Colors
        completed_color = QColor(0, 150, 0)  # Green for completed
        pending_color = QColor(200, 200, 200)  # Gray for pending
        text_color = QColor(0, 0, 0)  # Black for text

        # Draw connectors between circles
        for i in range(num_stages - 1):
            x1 = spacing * (i + 1) + circle_diameter * (i + 0.5)  # Starting x coordinate of line
            x2 = spacing * (i + 2) + circle_diameter * (i + 1.5)  # Ending x coordinate of line
            y = height / 2  # Vertically centered
            if i + 1 < self.progress:
                pen = QPen(completed_color, connector_height, Qt.SolidLine)  # Completed
            else:
                pen = QPen(pending_color, connector_height, Qt.DashLine)  # Pending
            painter.setPen(pen)
            painter.drawLine(int(x1), int(y), int(x2), int(y))

        # Draw circles and labels
        for i in range(num_stages):
            x = spacing * (i + 1) + circle_diameter * i
            y = height / 2 - circle_diameter / 2
            rect = QRectF(x, y, circle_diameter, circle_diameter)

            # Fill circle if stage is completed
            if i < self.progress:
                painter.setBrush(QBrush(completed_color))
            else:
                painter.setBrush(QBrush(Qt.NoBrush))
            painter.setPen(QPen(Qt.black, 1))
            painter.drawEllipse(rect)

            # Draw label below circle
            label_rect = QRectF(x, y + circle_diameter + 5, circle_diameter + 69, 25)
            painter.setPen(QPen(text_color))
            painter.drawText(label_rect, Qt.AlignLeft, self.stages[i])