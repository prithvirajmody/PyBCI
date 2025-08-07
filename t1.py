from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit,
    QListWidget, QDialog, QListWidgetItem, QStackedWidget, QSplitter, QScrollArea, 
    QSpinBox, QDoubleSpinBox, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData
from PyQt5.QtGui import QDrag, QPainter
import json


class DeepLearningConfigWidget(QDialog):
    """Unified deep learning model configuration widget with drag-and-drop layer design."""
    
    modelConfigured = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Deep Learning Model")
        self.setMinimumSize(1000, 700)
        
        # Configuration data
        self.model_configs = {
            "Multi-layer Perceptron": {
                "hyperparams": [
                    ("learning_rate", "line", "0.001"),
                    ("batch_size", "combo", ["32", "64", "128", "256"]),
                    ("epochs", "line", "100"),
                    ("optimizer", "combo", ["SGD", "Adam", "RMSprop"]),
                    ("weight_decay", "line", "0.01")
                ],
                "layers": {
                    "Dense Layer": {
                        "units": {"type": "int", "default": 64, "min": 1, "max": 2048},
                        "activation": {"type": "combo", "default": "relu", "options": ["relu", "sigmoid", "tanh", "linear"]}
                    },
                    "Dropout Layer": {
                        "rate": {"type": "float", "default": 0.2, "min": 0.0, "max": 1.0}
                    },
                    "Batch Normalization": {}
                }
            },
            "Convolutional Neural Network": {
                "hyperparams": [
                    ("learning_rate", "line", "0.001"),
                    ("batch_size", "combo", ["16", "32", "64", "128"]),
                    ("epochs", "line", "50"),
                    ("optimizer", "combo", ["SGD", "Adam", "Ranger"]),
                    ("early_stopping", "line", "10")
                ],
                "layers": {
                    "Conv2D Layer": {
                        "filters": {"type": "int", "default": 32, "min": 1, "max": 512},
                        "kernel_size": {"type": "int", "default": 3, "min": 1, "max": 11},
                        "activation": {"type": "combo", "default": "relu", "options": ["relu", "sigmoid", "tanh", "linear"]},
                        "padding": {"type": "combo", "default": "same", "options": ["same", "valid"]}
                    },
                    "MaxPooling2D Layer": {
                        "pool_size": {"type": "int", "default": 2, "min": 1, "max": 8},
                        "strides": {"type": "int", "default": 2, "min": 1, "max": 8}
                    },
                    "Flatten Layer": {},
                    "Dense Layer": {
                        "units": {"type": "int", "default": 64, "min": 1, "max": 2048},
                        "activation": {"type": "combo", "default": "relu", "options": ["relu", "sigmoid", "tanh", "linear"]}
                    },
                    "Dropout Layer": {
                        "rate": {"type": "float", "default": 0.2, "min": 0.0, "max": 1.0}
                    }
                }
            },
            "Recurrent Neural Network": {
                "hyperparams": [
                    ("learning_rate", "line", "0.001"),
                    ("batch_size", "combo", ["32", "64", "128", "256"]),
                    ("epochs", "line", "100"),
                    ("optimizer", "combo", ["SGD", "Adam", "RMSprop"]),
                    ("gradient_clipping", "line", "0.5")
                ],
                "layers": {
                    "SimpleRNN Layer": {
                        "units": {"type": "int", "default": 50, "min": 1, "max": 512},
                        "activation": {"type": "combo", "default": "tanh", "options": ["tanh", "relu", "sigmoid"]},
                        "return_sequences": {"type": "combo", "default": "False", "options": ["True", "False"]}
                    },
                    "Dense Layer": {
                        "units": {"type": "int", "default": 64, "min": 1, "max": 2048},
                        "activation": {"type": "combo", "default": "relu", "options": ["relu", "sigmoid", "tanh", "linear"]}
                    },
                    "Dropout Layer": {
                        "rate": {"type": "float", "default": 0.2, "min": 0.0, "max": 1.0}
                    }
                }
            },
            "LSTM Network": {
                "hyperparams": [
                    ("learning_rate", "line", "0.001"),
                    ("batch_size", "combo", ["32", "64", "128", "256"]),
                    ("epochs", "line", "100"),
                    ("optimizer", "combo", ["SGD", "Adam", "RMSprop"]),
                    ("gradient_clipping", "line", "0.5"),
                    ("sequence_length", "line", "10")
                ],
                "layers": {
                    "LSTM Layer": {
                        "units": {"type": "int", "default": 50, "min": 1, "max": 512},
                        "activation": {"type": "combo", "default": "tanh", "options": ["tanh", "relu", "sigmoid"]},
                        "return_sequences": {"type": "combo", "default": "False", "options": ["True", "False"]},
                        "dropout": {"type": "float", "default": 0.0, "min": 0.0, "max": 1.0},
                        "recurrent_dropout": {"type": "float", "default": 0.0, "min": 0.0, "max": 1.0}
                    },
                    "Dense Layer": {
                        "units": {"type": "int", "default": 64, "min": 1, "max": 2048},
                        "activation": {"type": "combo", "default": "relu", "options": ["relu", "sigmoid", "tanh", "linear"]}
                    },
                    "Dropout Layer": {
                        "rate": {"type": "float", "default": 0.2, "min": 0.0, "max": 1.0}
                    }
                }
            }
        }
        
        self.hyperparam_widgets = {}
        self.layer_widgets = []
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout()
        
        # Model selection
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.model_configs.keys())
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        main_layout.addWidget(QLabel("Select Deep Learning Model:"))
        main_layout.addWidget(self.model_combo)
        
        # Hyperparameter stack
        self.hyperparam_stack = QStackedWidget()
        main_layout.addWidget(self.hyperparam_stack)
        
        # Create hyperparameter widgets for each model
        for model_name, config in self.model_configs.items():
            hyperparam_widget = self.create_hyperparam_widget(config["hyperparams"])
            self.hyperparam_stack.addWidget(hyperparam_widget)
        
        # Layer design area
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: Available layers
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Available Layers (Drag to Model):"))
        
        scroll_area = QScrollArea()
        self.layer_palette = QWidget()
        self.palette_layout = QVBoxLayout()
        self.layer_palette.setLayout(self.palette_layout)
        scroll_area.setWidget(self.layer_palette)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumWidth(250)
        
        left_layout.addWidget(scroll_area)
        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)
        
        # Right: Model architecture
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Model Architecture:"))
        
        self.architecture_list = ArchitectureList()
        right_layout.addWidget(self.architecture_list)
        
        # Architecture management buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Remove Selected", clicked=self.remove_layer))
        btn_layout.addWidget(QPushButton("Clear All", clicked=self.architecture_list.clear))
        right_layout.addLayout(btn_layout)
        
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)
        
        main_layout.addWidget(splitter)
        
        # Add model button
        main_layout.addWidget(QPushButton("Add Model to Pipeline", clicked=self.add_model))
        
        self.setLayout(main_layout)
        
        # Initialize with first model
        self.on_model_changed(self.model_combo.currentText())
    
    def create_hyperparam_widget(self, hyperparam_config):
        """Create hyperparameter configuration widget."""
        widget = QWidget()
        layout = QVBoxLayout()
        inputs = {}
        
        for param_name, param_type, default in hyperparam_config:
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{param_name}:"))
            
            if param_type == "combo":
                input_widget = QComboBox()
                input_widget.addItems(default)
            else:  # line
                input_widget = QLineEdit(str(default))
            
            hbox.addWidget(input_widget)
            layout.addLayout(hbox)
            inputs[param_name] = input_widget
        
        widget.setLayout(layout)
        widget.inputs = inputs  # Store inputs as widget attribute
        return widget
    
    def on_model_changed(self, model_name):
        """Handle model selection change."""
        # Update hyperparameter stack
        model_index = list(self.model_configs.keys()).index(model_name)
        self.hyperparam_stack.setCurrentIndex(model_index)
        
        # Update layer palette
        self.update_layer_palette(model_name)
    
    def update_layer_palette(self, model_name):
        """Update available layers for the selected model."""
        # Clear existing widgets
        for widget in self.layer_widgets:
            widget.setParent(None)
        self.layer_widgets.clear()
        
        # Add new layer widgets
        layer_configs = self.model_configs[model_name]["layers"]
        for layer_type, layer_config in layer_configs.items():
            layer_widget = LayerWidget(layer_type, layer_config)
            self.layer_widgets.append(layer_widget)
            self.palette_layout.addWidget(layer_widget)
        
        self.palette_layout.addStretch()
    
    def remove_layer(self):
        """Remove selected layer from architecture."""
        current_row = self.architecture_list.currentRow()
        if current_row >= 0:
            self.architecture_list.takeItem(current_row)
    
    def get_hyperparameters(self):
        """Get current hyperparameter values."""
        current_widget = self.hyperparam_stack.currentWidget()
        params = {}
        
        for param_name, widget in current_widget.inputs.items():
            if isinstance(widget, QComboBox):
                params[param_name] = widget.currentText()
            else:
                value = widget.text()
                try:
                    params[param_name] = float(value) if '.' in value else int(value)
                except ValueError:
                    params[param_name] = value
        
        return params
    
    def get_architecture(self):
        """Get current model architecture."""
        architecture = []
        for i in range(self.architecture_list.count()):
            item = self.architecture_list.item(i)
            architecture.append(item.data(Qt.UserRole))
        return architecture
    
    def add_model(self):
        """Add configured model to pipeline."""
        model_name = self.model_combo.currentText()
        hyperparams = self.get_hyperparameters()
        architecture = self.get_architecture()
        
        if not architecture:
            QMessageBox.warning(self, "No Architecture", 
                              "Please add at least one layer to your model.")
            return
        
        config = {
            "model": model_name,
            "params": {**hyperparams, "architecture": architecture}
        }
        
        self.modelConfigured.emit(config)
        self.accept()


class LayerWidget(QLabel):
    """Draggable layer widget."""
    
    def __init__(self, layer_type, layer_config):
        super().__init__(layer_type)
        self.layer_type = layer_type
        self.layer_config = layer_config
        
        self.setStyleSheet("""
            QLabel {
                background-color: #e1f5fe; border: 2px solid #0277bd;
                border-radius: 8px; padding: 8px; margin: 2px; font-weight: bold;
            }
            QLabel:hover { background-color: #b3e5fc; border-color: #01579b; }
        """)
        self.setMinimumSize(120, 40)
        self.setAlignment(Qt.AlignCenter)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start = event.pos()
    
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton and 
            (event.pos() - self.drag_start).manhattanLength() > 30):
            
            drag = QDrag(self)
            mimeData = QMimeData()
            mimeData.setText(json.dumps({
                'layer_type': self.layer_type,
                'layer_config': self.layer_config
            }))
            drag.setMimeData(mimeData)
            drag.setPixmap(self.grab())
            drag.exec_(Qt.CopyAction)


class ArchitectureList(QListWidget):
    """List widget for model architecture with drag-and-drop support."""
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setMinimumHeight(300)
        self.setStyleSheet("""
            QListWidget {
                background-color: #f5f5f5; border: 2px dashed #ccc;
                border-radius: 8px; padding: 10px;
            }
            QListWidget::item {
                background-color: white; border: 1px solid #ddd;
                border-radius: 4px; padding: 8px; margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd; border-color: #2196f3;
            }
        """)
    
    def dragEnterEvent(self, event):
        event.accept() if event.mimeData().hasText() else event.ignore()
    
    def dragMoveEvent(self, event):
        event.accept() if event.mimeData().hasText() else event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasText():
            try:
                data = json.loads(event.mimeData().text())
                params = self.configure_layer(data['layer_type'], data['layer_config'])
                
                if params is not None:
                    # Create display text
                    param_str = ", ".join(f"{k}={v}" for k, v in params.items()) if params else ""
                    display_text = f"{data['layer_type']}" + (f" ({param_str})" if param_str else "")
                    
                    # Create list item
                    item = QListWidgetItem(display_text)
                    item.setData(Qt.UserRole, {'layer_type': data['layer_type'], 'parameters': params})
                    
                    # Insert at drop position
                    drop_index = self.indexAt(event.pos()).row()
                    if drop_index == -1:
                        self.addItem(item)
                    else:
                        self.insertItem(drop_index, item)
                
                event.accept()
            except (json.JSONDecodeError, KeyError):
                event.ignore()
        else:
            super().dropEvent(event)
    
    def configure_layer(self, layer_type, layer_config):
        """Open configuration dialog for layer parameters."""
        if not layer_config:
            return {}
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Configure {layer_type}")
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel(f"Layer Type: {layer_type}"))
        
        widgets = {}
        for param_name, param_info in layer_config.items():
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{param_name}:"))
            
            param_type = param_info.get('type', 'line')
            default = param_info.get('default', '')
            
            if param_type == 'combo':
                widget = QComboBox()
                widget.addItems([str(opt) for opt in param_info.get('options', [])])
                if default in param_info.get('options', []):
                    widget.setCurrentText(str(default))
            elif param_type == 'int':
                widget = QSpinBox()
                widget.setRange(param_info.get('min', 0), param_info.get('max', 1000))
                widget.setValue(int(default) if default else param_info.get('min', 0))
            elif param_type == 'float':
                widget = QDoubleSpinBox()
                widget.setRange(param_info.get('min', 0.0), param_info.get('max', 1.0))
                widget.setDecimals(4)
                widget.setValue(float(default) if default else param_info.get('min', 0.0))
            else:
                widget = QLineEdit(str(default))
            
            hbox.addWidget(widget)
            layout.addLayout(hbox)
            widgets[param_name] = widget
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("OK", clicked=dialog.accept))
        btn_layout.addWidget(QPushButton("Cancel", clicked=dialog.reject))
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            params = {}
            for param_name, widget in widgets.items():
                if isinstance(widget, QComboBox):
                    params[param_name] = widget.currentText()
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    params[param_name] = widget.value()
                else:
                    value = widget.text()
                    try:
                        params[param_name] = float(value) if '.' in value else int(value)
                    except ValueError:
                        params[param_name] = value
            return params
        
        return None