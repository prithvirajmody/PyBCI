from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit,
    QGroupBox, QListWidget, QProgressBar, QFileDialog, QDialog, QListWidgetItem, QStackedWidget
)
from PyQt5.QtCore import pyqtSignal, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

#Custom classes and scripts
from deeplearning_widget import DeepLearningConfigWidget

class ModelConfigWidget:
    """Base class for model configuration widgets."""
    
    def setup_model_selection(self, layout, models, label_text):
        """Set up model selection UI and hyperparameter stack."""
        self.model_combo = QComboBox()
        self.model_combo.addItems(models)
        layout.addWidget(QLabel(label_text))
        layout.addWidget(self.model_combo)
        
        self.hyperparam_stack = QStackedWidget()
        layout.addWidget(self.hyperparam_stack)
        
        self.hyperparam_widgets = {}
        self.hyperparam_inputs = {}
        for model, config in self.hyperparam_config.items():
            widget, inputs = self.create_hyperparams_widget(config)
            self.hyperparam_widgets[model] = widget
            self.hyperparam_inputs[model] = inputs
            self.hyperparam_stack.addWidget(widget)
        
        self.model_combo.currentTextChanged.connect(self.update_hyperparameters)
        self.update_hyperparameters(self.model_combo.currentText())

    def create_hyperparams_widget(self, config):
        """Create a widget with hyperparameter inputs based on the config."""
        widget = QWidget()
        layout = QVBoxLayout()
        inputs = {}
        #Making sure the only types that get printed out in this config are combo and line
        for param_name, param_type, default in config:
            if param_type == "combo" or "line":
                hbox = QHBoxLayout()
                label = QLabel(f"{param_name}:")
                hbox.addWidget(label)
                if param_type == "combo":
                    input_widget = QComboBox()
                    input_widget.addItems(default)
                elif param_type == "line":
                    input_widget = QLineEdit(str(default))
            #Make the cases for layer and layer_combo
            if param_type == "layer" or "layer_combo":
                pass
            hbox.addWidget(input_widget)
            layout.addLayout(hbox)
            inputs[param_name] = input_widget
        widget.setLayout(layout)
        return widget, inputs

    def update_hyperparameters(self, selected_model):
        """Update the displayed hyperparameter widgets based on the selected model."""
        widget = self.hyperparam_widgets.get(selected_model)
        if widget:
            self.hyperparam_stack.setCurrentWidget(widget)

    def get_model_params(self, selected_model):
        """Collect hyperparameters for the selected model."""
        inputs = self.hyperparam_inputs.get(selected_model, {})
        params = {}
        for param, widget in inputs.items():
            if isinstance(widget, QComboBox):
                params[param] = widget.currentText()
            elif isinstance(widget, QLineEdit):
                value = widget.text()
                try:
                    params[param] = float(value)
                except ValueError:
                    params[param] = value
        return params

class MLPageWidget(QWidget, ModelConfigWidget):
    trainRequested = pyqtSignal(list)  # Signal for training actions (corrected to list)
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
        self.hyperparam_config = {
            "Linear Discriminant Analysis (LDA)": [
                ("Solver", "combo", ["svd", "lsqr", "eigen"]),
                ("Shrinkage", "line", "auto"),
                ("n_components", "line", "None")
            ],
            "Support Vector Machine (SVM)": [
                ("Kernel", "combo", ["linear", "poly", "rbf", "sigmoid"]),
                ("C", "line", "1.0"),
                ("Gamma", "line", "scale")
            ],
            "Random Forest": [
                ("n_estimators", "line", "100"),
                ("max_depth", "line", "None"),
                ("min_samples_split", "line", "2"),
                ("min_samples_leaf", "line", "1"),
                ("max_features", "combo", ["auto", "sqrt", "log2"])
            ],
            "Gradient Boosting Machine (GBM)": [
                ("n_estimators", "line", "100"),
                ("learning_rate", "line", "0.1"),
                ("max_depth", "line", "3"),
                ("min_samples_split", "line", "2"),
                ("subsample", "line", "1.0")
            ],
            "K-means Clustering": [
                ("n_clusters", "line", "8"),
                ("init", "combo", ["k-means++", "random"])
            ],
            "Gaussian Mixture Model (GMM)": [
                ("n_components", "line", "1"),
                ("covariance_type", "combo", ["full", "tied", "diag", "spherical"])
            ],
        }
        self.setup_model_selection(model_layout, self.hyperparam_config.keys(), "Select Machine Learning Algorithms:")
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)

        # Buttons for adding models
        add_model_layout = QHBoxLayout()
        self.add_model_button = QPushButton("Add Model to Pipeline")
        self.add_DL_algo_button = QPushButton("Add a Deep Learning Model")
        add_model_layout.addWidget(self.add_model_button)
        add_model_layout.addWidget(self.add_DL_algo_button)
        layout.addLayout(add_model_layout)

        # Connect buttons
        self.add_model_button.clicked.connect(self.add_model_to_pipeline)
        self.add_DL_algo_button.clicked.connect(self.open_deep_learning_page)

        # Pipeline builder
        pipeline_group = QGroupBox("ML Pipeline")
        pipeline_layout = QVBoxLayout()
        pipeline_layout.addWidget(QLabel("Selected Models (drag to reorder):"))
        self.pipeline_list = QListWidget()
        self.pipeline_list.setDragDropMode(QListWidget.InternalMove)
        pipeline_layout.addWidget(self.pipeline_list)
        train_button = QPushButton("Train Pipeline")
        train_button.clicked.connect(self.train_pipeline)
        pipeline_layout.addWidget(train_button)
        pipeline_group.setLayout(pipeline_layout)
        layout.addWidget(pipeline_group)

        # Estimated time label
        self.estimated_time_label = QLabel("Estimated Time to Finish Training: TBD")
        layout.addWidget(self.estimated_time_label)

        # Progress bar
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

    def open_deep_learning_page(self):
        """Open the DeepLearningPageWidget as a dialog."""
        dialog = DeepLearningConfigWidget(self)
        dialog.modelConfigured.connect(self.add_deep_learning_model)
        dialog.exec_()

    def add_model_to_pipeline(self):
        """Add selected ML model to the pipeline."""
        selected_model = self.model_combo.currentText()
        params = self.get_model_params(selected_model)
        item = QListWidgetItem(f"{selected_model}: {params}")
        item.setData(Qt.UserRole, {"model": selected_model, "params": params})
        self.pipeline_list.addItem(item)
        self.status_label.setText(f"Added {selected_model} to pipeline")

    def add_deep_learning_model(self, model_config):
        """Add deep learning model to the pipeline."""
        item = QListWidgetItem(f"{model_config['model']}: {model_config['params']}")
        item.setData(Qt.UserRole, model_config)
        self.pipeline_list.addItem(item)
        self.status_label.setText(f"Added {model_config['model']} to pipeline")

    def train_pipeline(self):
        """Emit the pipeline for training."""
        pipeline = [self.pipeline_list.item(i).data(Qt.UserRole) for i in range(self.pipeline_list.count())]
        self.trainRequested.emit(pipeline)
        self.status_label.setText("Training pipeline...")

    def plot_confusion_matrix(self):
        self.status_label.setText("Displaying confusion matrix")

    def plot_roc_curve(self):
        self.status_label.setText("Displaying ROC curve")

    def plot_topomap(self):
        self.status_label.setText("Displaying topographic map")

    def save_model(self):
        """Save the trained model weights."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Model Weights", "", "Pickle files (*.pkl)")
        if file_name:
            self.saveModelRequested.emit(file_name)
            self.status_label.setText(f"Model saved to {file_name}")