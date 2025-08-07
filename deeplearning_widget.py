from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit,
    QListWidget, QDialog, QListWidgetItem, QStackedWidget, QSplitter, QScrollArea, 
    QSpinBox, QDoubleSpinBox, QMessageBox, QGroupBox, QFileDialog
)
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData
from PyQt5.QtGui import QDrag
import json

class DeepLearningConfigWidget(QDialog):
    """Unified deep learning model configuration widget with drag-and-drop layer design and enhanced flexibility."""
    
    modelConfigured = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Deep Learning Model")
        self.setMinimumSize(1000, 700)
        
        # Configuration data with expanded layers and hyperparameters
        self.model_configs = {
            "Multi-layer Perceptron": {
                "hyperparams": [
                    ("learning_rate", "float", 0.001, 0.0001, 0.1),
                    ("batch_size", "int", 32, 1, 1024),
                    ("epochs", "int", 100, 1, 1000),
                    ("optimizer", "combo", ["SGD", "Adam", "RMSprop", "AdamW", "Lookahead"]),
                    ("weight_decay", "float", 0.01, 0.0, 1.0)
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
                    ("learning_rate", "float", 0.001, 0.0001, 0.1),
                    ("batch_size", "int", 16, 1, 1024),
                    ("epochs", "int", 50, 1, 1000),
                    ("optimizer", "combo", ["SGD", "Adam", "RMSprop", "AdamW", "Lookahead"]),
                    ("early_stopping", "int", 10, 1, 100)
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
                    "AveragePooling2D Layer": {
                        "pool_size": {"type": "int", "default": 2, "min": 1, "max": 8},
                        "strides": {"type": "int", "default": 2, "min": 1, "max": 8}
                    },
                    "DepthwiseConv2D Layer": {
                        "kernel_size": {"type": "int", "default": 3, "min": 1, "max": 11},
                        "activation": {"type": "combo", "default": "relu", "options": ["relu", "sigmoid", "tanh", "linear"]},
                        "padding": {"type": "combo", "default": "same", "options": ["same", "valid"]}
                    },
                    "LayerNormalization": {},
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
                    ("learning_rate", "float", 0.001, 0.0001, 0.1),
                    ("batch_size", "int", 32, 1, 1024),
                    ("epochs", "int", 100, 1, 1000),
                    ("optimizer", "combo", ["SGD", "Adam", "RMSprop", "AdamW", "Lookahead"]),
                    ("gradient_clipping", "float", 0.5, 0.0, 10.0)
                ],
                "layers": {
                    "SimpleRNN Layer": {
                        "units": {"type": "int", "default": 50, "min": 1, "max": 512},
                        "activation": {"type": "combo", "default": "tanh", "options": ["tanh", "relu", "sigmoid"]},
                        "return_sequences": {"type": "combo", "default": "False", "options": ["True", "False"]}
                    },
                    "GRU Layer": {
                        "units": {"type": "int", "default": 50, "min": 1, "max": 512},
                        "activation": {"type": "combo", "default": "tanh", "options": ["tanh", "relu", "sigmoid"]},
                        "return_sequences": {"type": "combo", "default": "False", "options": ["True", "False"]}
                    },
                    "Attention Layer": {
                        "units": {"type": "int", "default": 64, "min": 1, "max": 512}
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
                    ("learning_rate", "float", 0.001, 0.0001, 0.1),
                    ("batch_size", "int", 32, 1, 1024),
                    ("epochs", "int", 100, 1, 1000),
                    ("optimizer", "combo", ["SGD", "Adam", "RMSprop", "AdamW", "Lookahead"]),
                    ("gradient_clipping", "float", 0.5, 0.0, 10.0)
                ],
                "layers": {
                    "LSTM Layer": {
                        "units": {"type": "int", "default": 50, "min": 1, "max": 512},
                        "activation": {"type": "combo", "default": "tanh", "options": ["tanh", "relu", "sigmoid"]},
                        "return_sequences": {"type": "combo", "default": "False", "options": ["True", "False"]}
                    },
                    "GRU Layer": {
                        "units": {"type": "int", "default": 50, "min": 1, "max": 512},
                        "activation": {"type": "combo", "default": "tanh", "options": ["tanh", "relu", "sigmoid"]},
                        "return_sequences": {"type": "combo", "default": "False", "options": ["True", "False"]}
                    },
                    "Attention Layer": {
                        "units": {"type": "int", "default": 64, "min": 1, "max": 512}
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
        self.custom_layers = {}
        self.input_shape = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface with enhanced features."""
        main_layout = QVBoxLayout()
        
        # Input Shape Configuration
        input_shape_group = QGroupBox("Input Shape Configuration")
        input_shape_layout = QHBoxLayout()
        self.input_format_combo = QComboBox()
        self.input_format_combo.addItems([
            "Custom", 
            "EEG Time Series (channels, time_steps)", 
            "EEG Spectrogram (channels, freq, time)"
        ])
        self.input_format_combo.currentTextChanged.connect(self.update_input_shape)
        input_shape_layout.addWidget(QLabel("Input Format:"))
        input_shape_layout.addWidget(self.input_format_combo)
        self.input_shape_input = QLineEdit()
        input_shape_layout.addWidget(QLabel("Input Shape:"))
        input_shape_layout.addWidget(self.input_shape_input)
        input_shape_group.setLayout(input_shape_layout)
        main_layout.addWidget(input_shape_group)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Select Deep Learning Model:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(self.model_configs.keys())
        self.model_combo.currentTextChanged.connect(self.on_model_changed)
        model_layout.addWidget(self.model_combo)
        main_layout.addLayout(model_layout)
        
        # Hyperparameter stack
        self.hyperparam_stack = QStackedWidget()
        main_layout.addWidget(self.hyperparam_stack)
        
        # Create hyperparameter widgets for each model
        for model_name, config in self.model_configs.items():
            hyperparam_widget = self.create_hyperparam_widget(config["hyperparams"])
            self.hyperparam_stack.addWidget(hyperparam_widget)
        
        # Layer design area with splitter
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
        
        # Save and Load buttons
        save_load_layout = QHBoxLayout()
        save_load_layout.addWidget(QPushButton("Save Configuration", clicked=self.save_configuration))
        save_load_layout.addWidget(QPushButton("Load Configuration", clicked=self.load_configuration))
        main_layout.addLayout(save_load_layout)
        
        # Add model button
        main_layout.addWidget(QPushButton("Add Model to Pipeline", clicked=self.add_model))
        
        self.setLayout(main_layout)
        
        # Initialize with first model
        self.on_model_changed(self.model_combo.currentText())
    
    def create_hyperparam_widget(self, hyperparam_config):
        """Create a widget for hyperparameter configuration with flexible inputs."""
        widget = QWidget()
        layout = QVBoxLayout()
        inputs = {}
        
        for param_config in hyperparam_config:
            param_name, param_type, default = param_config[:3]
            min_val = max_val = None
            if len(param_config) == 5:
                min_val, max_val = param_config[3:]

            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{param_name.replace('_', ' ').title()}:"))
            
            if param_type == "combo":
                input_widget = QComboBox()
                input_widget.addItems(default)
                input_widget.setCurrentText(default[0] if isinstance(default, list) else str(default))
            elif param_type == "int":
                input_widget = QSpinBox()
                input_widget.setRange(min_val or 0, max_val or 1000)
                input_widget.setValue(int(default))
            elif param_type == "float":
                input_widget = QDoubleSpinBox()
                input_widget.setRange(min_val or 0.0, max_val or 1.0)
                input_widget.setDecimals(4)
                input_widget.setValue(float(default))
            else:
                input_widget = QLineEdit(str(default))
            
            hbox.addWidget(input_widget)
            layout.addLayout(hbox)
            inputs[param_name] = input_widget
        
        widget.setLayout(layout)
        widget.inputs = inputs
        return widget
    
    def on_model_changed(self, model_name):
        """Update UI when model type changes."""
        model_index = list(self.model_configs.keys()).index(model_name)
        self.hyperparam_stack.setCurrentIndex(model_index)
        self.update_layer_palette(model_name)
    
    def update_layer_palette(self, model_name):
        """Populate layer palette with available layers."""
        for widget in self.layer_widgets:
            widget.setParent(None)
        self.layer_widgets.clear()
        
        layers = self.model_configs[model_name]["layers"]
        for layer_type, layer_config in layers.items():
            layer_widget = LayerWidget(layer_type, layer_config)
            self.layer_widgets.append(layer_widget)
            self.palette_layout.addWidget(layer_widget)
        
        self.palette_layout.addStretch()
    
    def remove_layer(self):
        """Remove the selected layer from the architecture."""
        current_row = self.architecture_list.currentRow()
        if current_row >= 0:
            self.architecture_list.takeItem(current_row)
            self.validate_architecture(self.model_combo.currentText(), self.get_architecture())
    
    def get_hyperparameters(self):
        """Retrieve current hyperparameter values."""
        current_widget = self.hyperparam_stack.currentWidget()
        params = {}
        for param_name, widget in current_widget.inputs.items():
            if isinstance(widget, QComboBox):
                params[param_name] = widget.currentText()
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                params[param_name] = widget.value()
            else:
                try:
                    value = widget.text()
                    params[param_name] = float(value) if '.' in value else int(value)
                except ValueError:
                    params[param_name] = value
        return params
    
    def get_architecture(self):
        """Retrieve current model architecture."""
        architecture = []
        for i in range(self.architecture_list.count()):
            item = self.architecture_list.item(i)
            architecture.append(item.data(Qt.UserRole))
        return architecture
    
    def validate_architecture(self, model_name, architecture):
        """Validate the architecture based on model-specific rules."""
        if model_name == "Convolutional Neural Network":
            has_flatten = False
            for i, layer in enumerate(architecture):
                if layer["layer_type"] == "Flatten Layer":
                    has_flatten = True
                elif layer["layer_type"] == "Dense Layer" and not has_flatten:
                    QMessageBox.warning(self, "Invalid Architecture", 
                                       "In a CNN, a Flatten layer must precede any Dense layer.")
                    return False
        return True
    
    def add_model(self):
        """Emit the configured model with validation."""
        model_name = self.model_combo.currentText()
        hyperparams = self.get_hyperparameters()
        architecture = self.get_architecture()
        input_shape = self.input_shape_input.text().strip()
        
        if not architecture:
            QMessageBox.warning(self, "Error", "Please add at least one layer to the architecture.")
            return
        
        if not input_shape:
            QMessageBox.warning(self, "Error", "Please specify an input shape.")
            return
        
        if not self.validate_architecture(model_name, architecture):
            return
        
        config = {
            "model": model_name,
            "input_shape": input_shape,
            "params": {**hyperparams, "architecture": architecture}
        }
        
        self.modelConfigured.emit(config)
        self.accept()
    
    def save_configuration(self):
        """Save current configuration to a JSON file."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Configuration", "", "JSON Files (*.json)")
        if file_name:
            config = {
                "model": self.model_combo.currentText(),
                "input_shape": self.input_shape_input.text(),
                "hyperparams": self.get_hyperparameters(),
                "architecture": self.get_architecture()
            }
            with open(file_name, 'w') as f:
                json.dump(config, f, indent=4)
            QMessageBox.information(self, "Saved", f"Configuration saved to {file_name}")
    
    def load_configuration(self):
        """Load a configuration from a JSON file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Configuration", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as f:
                config = json.load(f)
            
            self.model_combo.setCurrentText(config["model"])
            self.input_shape_input.setText(config["input_shape"])
            
            current_widget = self.hyperparam_stack.currentWidget()
            for param_name, value in config["hyperparams"].items():
                widget = current_widget.inputs.get(param_name)
                if widget:
                    if isinstance(widget, QComboBox):
                        widget.setCurrentText(str(value))
                    elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                        widget.setValue(value)
                    else:
                        widget.setText(str(value))
            
            self.architecture_list.clear()
            for layer in config["architecture"]:
                display_text = f"{layer['layer_type']}: {', '.join(f'{k}={v}' for k, v in layer['parameters'].items())}"
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, layer)
                self.architecture_list.addItem(item)
            
            QMessageBox.information(self, "Loaded", f"Configuration loaded from {file_name}")
    
    def update_input_shape(self, format_name):
        """Update input shape based on selected format."""
        if format_name == "EEG Time Series (channels, time_steps)":
            self.input_shape_input.setText("(channels, 1000)")
        elif format_name == "EEG Spectrogram (channels, freq, time)":
            self.input_shape_input.setText("(channels, 128, 128)")
        else:
            self.input_shape_input.setText("")

class LayerWidget(QLabel):
    """Draggable widget representing a layer."""
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
        self.setAlignment(Qt.AlignCenter)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start = event.pos()
    
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if (event.pos() - self.drag_start).manhattanLength() > 30:
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setText(json.dumps({"layer_type": self.layer_type, "layer_config": self.layer_config}))
                drag.setMimeData(mime_data)
                drag.setPixmap(self.grab())
                drag.exec_(Qt.CopyAction)

class ArchitectureList(QListWidget):
    """List widget for designing model architecture with drag-and-drop."""
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)
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
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasText():
            data = json.loads(event.mimeData().text())
            params = self.configure_layer(data["layer_type"], data["layer_config"])
            if params is not None:
                param_str = ", ".join(f"{k}={v}" for k, v in params.items()) if params else ""
                display_text = f"{data['layer_type']}" + (f" ({param_str})" if param_str else "")
                item = QListWidgetItem(display_text)
                item.setData(Qt.UserRole, {"layer_type": data["layer_type"], "parameters": params})
                
                drop_index = self.indexAt(event.pos()).row()
                if drop_index == -1:
                    self.addItem(item)
                else:
                    self.insertItem(drop_index, item)
                
                event.accept()
        else:
            super().dropEvent(event)
    
    def configure_layer(self, layer_type, layer_config):
        """Configure layer parameters with tooltips."""
        if not layer_config:
            return {}
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Configure {layer_type}")
        layout = QVBoxLayout()
        widgets = {}
        
        for param_name, param_info in layer_config.items():
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(f"{param_name.replace('_', ' ').title()}:"))
            
            param_type = param_info.get("type", "line")
            default = param_info.get("default", "")
            
            if param_type == "combo":
                widget = QComboBox()
                widget.addItems(param_info.get("options", []))
                widget.setCurrentText(str(default))
            elif param_type == "int":
                widget = QSpinBox()
                widget.setRange(param_info.get("min", 0), param_info.get("max", 1000))
                widget.setValue(default or param_info.get("min", 0))
            elif param_type == "float":
                widget = QDoubleSpinBox()
                widget.setRange(param_info.get("min", 0.0), param_info.get("max", 1.0))
                widget.setDecimals(4)
                widget.setValue(default or param_info.get("min", 0.0))
            else:
                widget = QLineEdit(str(default))
            
            widget.setToolTip(self.get_parameter_tooltip(layer_type, param_name))
            hbox.addWidget(widget)
            layout.addLayout(hbox)
            widgets[param_name] = widget
        
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
                        params[param_name] = float(value) if "." in value else int(value)
                    except ValueError:
                        params[param_name] = value
            return params
        return None
    
    def get_parameter_tooltip(self, layer_type, param_name):
        """Provide tooltips for layer parameters."""
        tooltips = {
            "Dense Layer": {
                "units": "Number of neurons in the layer",
                "activation": "Activation function applied to the output"
            },
            "Dropout Layer": {
                "rate": "Fraction of input units to drop during training (0 to 1)"
            },
            "Conv2D Layer": {
                "filters": "Number of output filters in the convolution",
                "kernel_size": "Size of the convolution window",
                "activation": "Activation function applied to the output",
                "padding": "Padding mode: 'same' or 'valid'"
            },
            "MaxPooling2D Layer": {
                "pool_size": "Size of the pooling window",
                "strides": "Step size of the pooling operation"
            },
            "AveragePooling2D Layer": {
                "pool_size": "Size of the pooling window",
                "strides": "Step size of the pooling operation"
            },
            "DepthwiseConv2D Layer": {
                "kernel_size": "Size of the depthwise convolution window",
                "activation": "Activation function applied to the output",
                "padding": "Padding mode: 'same' or 'valid'"
            },
            "LayerNormalization": {},
            "Flatten Layer": {},
            "SimpleRNN Layer": {
                "units": "Number of recurrent units",
                "activation": "Activation function applied to the output",
                "return_sequences": "Whether to return the full sequence or last output"
            },
            "GRU Layer": {
                "units": "Number of recurrent units",
                "activation": "Activation function applied to the output",
                "return_sequences": "Whether to return the full sequence or last output"
            },
            "LSTM Layer": {
                "units": "Number of recurrent units",
                "activation": "Activation function applied to the output",
                "return_sequences": "Whether to return the full sequence or last output"
            },
            "Attention Layer": {
                "units": "Dimensionality of the attention mechanism"
            }
        }
        return tooltips.get(layer_type, {}).get(param_name, "")
