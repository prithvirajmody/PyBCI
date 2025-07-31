import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton
)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF

class ProgressBarWidget(QWidget):
    def __init__(self, progress=0, parent=None):
        super().__init__(parent)
        self.progress = progress
        self.stages = ["Input", "Preprocessing", "AI Model", "Visualization", "Output"]
        self.setMinimumHeight(100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        num_stages = len(self.stages)
        circle_diameter = min(40, height * 0.4)
        connector_height = circle_diameter / 4
        spacing = (width - num_stages * circle_diameter) / (num_stages + 1)

        # Colors
        completed_color = QColor(0, 150, 0)  # Green for completed
        pending_color = QColor(200, 200, 200)  # Gray for pending
        text_color = QColor(0, 0, 0)  # Black for text

        # Draw connectors
        for i in range(num_stages - 1):
            x1 = spacing * (i + 1) + circle_diameter * (i + 0.5)
            x2 = spacing * (i + 2) + circle_diameter * (i + 1.5)
            y = height / 2
            if i + 1 < self.progress:
                pen = QPen(completed_color, connector_height, Qt.SolidLine)
            else:
                pen = QPen(pending_color, connector_height, Qt.DashLine)
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

class ProjectItemWidget(QWidget):
    def __init__(self, project_name, progress, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.project_label = QLabel(project_name)
        self.progress_bar = ProgressBarWidget(progress)
        layout.addWidget(self.project_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BCI Project Manager")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Recent projects list with implicit scrollbar support
        self.project_list = QListWidget()
        # Sample projects for demonstration
        sample_projects = [
            ("Project Alpha", 2),  # Input and Preprocessing completed
            ("Project Beta", 4),   # Up to Visualization completed
            ("Project Gamma", 0),  # No progress
            ("Project Theta", 1),
            ("Project Epsilon", 5),
        ]
        for name, progress in sample_projects:
            item_widget = ProjectItemWidget(name, progress)
            list_item = QListWidgetItem(self.project_list)
            list_item.setSizeHint(item_widget.sizeHint())
            self.project_list.addItem(list_item)
            self.project_list.setItemWidget(list_item, item_widget)

        layout.addWidget(self.project_list)

        # Buttons for new, open, and delete project
        button_layout = QHBoxLayout()
        self.new_project_button = QPushButton("New Project")
        self.open_project_button = QPushButton("Open Project")
        self.delete_project_button = QPushButton("Delete Project")
        self.delete_project_button.clicked.connect(self.delete_project)
        button_layout.addWidget(self.new_project_button)
        button_layout.addWidget(self.open_project_button)
        button_layout.addWidget(self.delete_project_button)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def delete_project(self):
        """Remove the selected project from the list."""
        selected_items = self.project_list.selectedItems()
        for item in selected_items:
            self.project_list.takeItem(self.project_list.row(item))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()  # Open in maximized mode by default
    sys.exit(app.exec_())