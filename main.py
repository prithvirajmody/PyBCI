import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QDialog, QLineEdit
)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRectF

#Import custom created files
from Backend.data_backend import create_project, add_new_project, show_saved_projects, delete_project, get_project_filepath
from project_homepage import ProjectWindow


### DO NOT DELETE THIS this widget has different dimensions from the other progressbar
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

#Window for when new project button is clicked
class CreateProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")

        # Layout
        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Please enter the project's name:")
        layout.addWidget(self.label)

        # Text entry field
        self.text_entry = QLineEdit(self)
        layout.addWidget(self.text_entry)

        # OK button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)  # Accept the dialog
        layout.addWidget(self.ok_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)  # Reject the dialog
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_input(self):
        return self.text_entry.text()  # Return the text entered by the user

#Window for when delete project button is clicked
class DeleteProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Project")

        # Layout
        layout = QVBoxLayout()

        # Label
        self.label = QLabel("Are you sure you want to delete your project?")
        layout.addWidget(self.label)

        self.next_line = QLabel("This action is irreversible once confirmed.")
        layout.addWidget(self.next_line)

        self.instruction_line = QLabel("To confirm this action type out the project name below:")
        layout.addWidget(self.instruction_line)

        self.project_name_line = QLineEdit()
        layout.addWidget(self.project_name_line)

        #Confirm button
        self.ok_button = QPushButton("Confirm")
        self.ok_button.clicked.connect(self.accept)  # Accept the dialog
        layout.addWidget(self.ok_button)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)  # Reject the dialog
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_input(self):
        return self.project_name_line.text()  # Return the text entered by the user

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

        # Read main.json and get projects
        all_projects = show_saved_projects()

        for name, progress in all_projects:
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

        self.new_project_button.clicked.connect(self.on_click_new)
        self.open_project_button.clicked.connect(self.on_click_open)
        self.delete_project_button.clicked.connect(self.on_click_delete)
        
        button_layout.addWidget(self.new_project_button)
        button_layout.addWidget(self.open_project_button)
        button_layout.addWidget(self.delete_project_button)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # This function will open a dialog asking for a project name
    def on_click_new(self):
        dialog = CreateProjectDialog(self)  # Pass self as the parent
        if dialog.exec_() == QDialog.Accepted:  # Execute the dialog and check if accepted
            project_name = dialog.get_input()  # Get the project name from the dialog
            project_filepath = create_project(project_name)  # Create the project
            add_new_project(project_name, project_filepath)  # Add the project to main.json
            self.update_project_list()  # Update the project list in the main window

    def on_click_delete(self):
        dialog = DeleteProjectDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            project_name = dialog.get_input()
            delete_project(project_name)
            self.update_project_list()

    #THis function is responsible for opening the selected project
    def on_click_open(self):
        current_item = self.project_list.currentItem()  # Get the currently selected item
        if current_item is not None:
            # Get the associated widget to access the project name
            project_widget = self.project_list.itemWidget(current_item)
            project_name = project_widget.project_label.text()  # Get the project name
            filepath = get_project_filepath(project_name)
            self.project_window = ProjectWindow(filepath)
            self.project_window.show()
        else:
            print("No project selected.")

    def update_project_list(self):
        """Refresh the project list from main.json."""
        self.project_list.clear()  # Clear the current list
        all_projects = show_saved_projects()  # Get updated projects

        for name, progress in all_projects:
            item_widget = ProjectItemWidget(name, progress)
            list_item = QListWidgetItem(self.project_list)
            list_item.setSizeHint(item_widget.sizeHint())
            self.project_list.addItem(list_item)
            self.project_list.setItemWidget(list_item, item_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()  # Open in maximized mode by default
    sys.exit(app.exec_())