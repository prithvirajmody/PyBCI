from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit,
    QGroupBox, QListWidget, QProgressBar, QFileDialog, QListWidgetItem
)
from PyQt5.QtCore import pyqtSignal, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class MLDeepLearningPageWidget(QWidget):
    trainRequested = pyqtSignal(dict)  # Signal for training actions
    saveModelRequested = pyqtSignal(str)  # Signal for saving model weights

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Status label
        self.status_label = QLabel("No model trained")
        layout.addWidget(self.status_label)

        # Model selection section
        model_group = QGroupBox("Model Selection")
        model_layout = QVBoxLayout()
        model_label = QLabel("Select Machine Learning Algorithm:")
        model_layout.addWidget(model_label)

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "Linear Discriminant Analysis (LDA)", "Support Vector Machine (SVM)", "Random Forest",
            "Gradient Boosting Machine (GBM)", "Neural Network (MLP)", "Convolutional Neural Network (CNN)",
            "Recurrent Neural Network (RNN)", "LSTM Network", "K-means Clustering", "Gaussian Mixture Model (GMM)",
            "Principal Component Analysis (PCA)", "t-SNE", "Autoencoder", "Generative Adversarial Network (GAN)"
        ])
        model_layout.addWidget(self.model_combo)

        # Hyperparameter inputs (example for SVM)
        self.svm_kernel = QComboBox()
        self.svm_kernel.addItems(["Linear", "RBF"])
        self.svm_c = QLineEdit("1.0")
        svm_hbox = QHBoxLayout()
        svm_hbox.addWidget(QLabel("Kernel:"))
        svm_hbox.addWidget(self.svm_kernel)
        svm_hbox.addWidget(QLabel("C:"))
        svm_hbox.addWidget(self.svm_c)
        model_layout.addLayout(svm_hbox)

        # Add model to pipeline
        add_model_button = QPushButton("Add Model to Pipeline")
        add_model_button.clicked.connect(self.add_model_to_pipeline)
        model_layout.addWidget(add_model_button)
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)

        # Pipeline builder
        pipeline_group = QGroupBox("ML Pipeline")
        pipeline_layout = QVBoxLayout()
        pipeline_label = QLabel("Selected Models (drag to reorder):")
        pipeline_layout.addWidget(pipeline_label)
        self.pipeline_list = QListWidget()
        self.pipeline_list.setDragDropMode(QListWidget.InternalMove)
        pipeline_layout.addWidget(self.pipeline_list)
        train_button = QPushButton("Train Pipeline")
        train_button.clicked.connect(self.train_pipeline)
        pipeline_layout.addWidget(train_button)
        pipeline_group.setLayout(pipeline_layout)
        layout.addWidget(pipeline_group)

        # Training progress

        #Estimated Time Label
        estimated_time = "blahblahblah" #Replace with actual value from scikit learn later
        self.estimated_time_label = QLabel(f"Estimated Time to Finish Training:{estimated_time}")
        layout.addWidget(self.estimated_time_label)
        #Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_bar)

        # Visualization section
        vis_group = QGroupBox("Model Visualizations")
        vis_layout = QVBoxLayout()
        self.vis_canvas = FigureCanvas(Figure())
        vis_layout.addWidget(self.vis_canvas)
        vis_buttons = QHBoxLayout()
        vis_buttons.addWidget(QPushButton("Plot Confusion Matrix", clicked=self.plot_confusion_matrix))
        vis_buttons.addWidget(QPushButton("Plot ROC Curve", clicked=self.plot_roc_curve))
        vis_buttons.addWidget(QPushButton("Plot Topographic Map", clicked=self.plot_topomap))
        vis_layout.addLayout(vis_buttons)
        vis_group.setLayout(vis_layout)
        layout.addWidget(vis_group)

        # Save model
        save_model_button = QPushButton("Save Model Weights")
        save_model_button.clicked.connect(self.save_model)
        layout.addWidget(save_model_button)

        self.setLayout(layout)

    def add_model_to_pipeline(self):
        model = self.model_combo.currentText()
        params = {}
        if model == "Support Vector Machine (SVM)":
            params = {"kernel": self.svm_kernel.currentText(), "C": float(self.svm_c.text())}
        item = QListWidgetItem(f"{model}: {params}")
        item.setData(Qt.UserRole, {"model": model, "params": params})
        self.pipeline_list.addItem(item)
        self.status_label.setText(f"Added {model} to pipeline")

    def train_pipeline(self):
        pipeline = []
        for i in range(self.pipeline_list.count()):
            item = self.pipeline_list.item(i)
            pipeline.append(item.data(Qt.UserRole))
        self.trainRequested.emit(pipeline)
        self.status_label.setText("Training pipeline...")

    def plot_confusion_matrix(self):
        self.status_label.setText("Displaying confusion matrix")

    def plot_roc_curve(self):
        self.status_label.setText("Displaying ROC curve")

    def plot_topomap(self):
        self.status_label.setText("Displaying topographic map")

    def save_model(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Model Weights", "", "Pickle files (*.pkl)")
        if file_name:
            self.saveModelRequested.emit(file_name)
            self.status_label.setText(f"Model saved to {file_name}")