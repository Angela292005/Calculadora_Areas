import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox
)
from PyQt5.QtCore import Qt


class ShapeSelector(QWidget):
    """
    Interfaz gráfica para seleccionar un tipo de figura geométrica y
    proporcionar sus dimensiones correspondientes.

    Permite seleccionar entre círculo, triángulo, rectángulo y cuadrado,
    y captura los valores necesarios para cada figura.
    """

    def __init__(self):
        """Inicializa la ventana principal y los componentes UI."""
        super().__init__()
        self.setWindowTitle("Selector de Figuras Geométricas")
        self.setGeometry(100, 100, 400, 200)
        self._init_ui()

    def _init_ui(self):
        """Configura la interfaz gráfica de usuario."""
        main_layout = QVBoxLayout()

        # Selector de tipo de figura
        self.shape_label = QLabel("Seleccione la figura:")
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Círculo", "Triángulo", "Rectángulo", "Cuadrado"])
        self.shape_combo.currentTextChanged.connect(self._update_input_fields)

        # Área para inputs dinámicos según figura
        self.input_area = QVBoxLayout()

        # Botón para confirmar selección
        self.confirm_btn = QPushButton("Confirmar")
        self.confirm_btn.clicked.connect(self._on_confirm)

        # Estado / Resultado
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)

        # Agregar widgets al layout principal
        main_layout.addWidget(self.shape_label)
        main_layout.addWidget(self.shape_combo)
        main_layout.addLayout(self.input_area)
        main_layout.addWidget(self.confirm_btn)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

        # Inicializar campos de entrada para la figura seleccionada
        self._update_input_fields(self.shape_combo.currentText())

    def _clear_input_area(self):
        """
        Elimina todos los widgets y layouts dentro del área de inputs
        para evitar superposición al cambiar la figura seleccionada.
        """
        while self.input_area.count():
            item = self.input_area.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def _clear_layout(self, layout):
        """
        Limpia recursivamente todos los widgets dentro de un layout.

        Args:
            layout (QLayout): Layout a limpiar.
        """
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self._clear_layout(child.layout())

    def _update_input_fields(self, shape: str):
        """
        Actualiza los campos de entrada según la figura seleccionada.

        Args:
            shape (str): Nombre de la figura seleccionada.
        """
        self._clear_input_area()

        if shape == "Círculo":
            self._add_input_field("Radio")
        elif shape == "Triángulo":
            self._add_input_field("Base")
            self._add_input_field("Altura")
        elif shape == "Rectángulo":
            self._add_input_field("Ancho")
            self._add_input_field("Altura")
        elif shape == "Cuadrado":
            self._add_input_field("Lado")

    def _add_input_field(self, label_text: str):
        """
        Agrega una fila con una etiqueta y un campo de texto para input.

        Args:
            label_text (str): Texto para la etiqueta del input.
        """
        container = QHBoxLayout()
        label = QLabel(label_text + ":")
        input_field = QLineEdit()
        input_field.setPlaceholderText("Ingrese un valor numérico")
        input_field.setObjectName(label_text.lower())  # para referencia posterior
        container.addWidget(label)
        container.addWidget(input_field)
        self.input_area.addLayout(container)

    def _get_input_values(self) -> dict:
        """
        Obtiene los valores ingresados en los campos de entrada.

        Returns:
            dict: Diccionario con nombre del campo y valor (float) ingresado.
        """
        values = {}
        for i in range(self.input_area.count()):
            layout = self.input_area.itemAt(i)
            if layout is not None and layout.count() == 2:
                label_widget = layout.itemAt(0).widget()
                input_widget = layout.itemAt(1).widget()
                if label_widget and input_widget:
                    key = label_widget.text().replace(":", "").lower()
                    try:
                        val = float(input_widget.text())
                        values[key] = val
                    except ValueError:
                        values[key] = None
        return values

    def _on_confirm(self):
        """Manejador para el evento click del botón Confirmar."""
        shape = self.shape_combo.currentText()
        inputs = self._get_input_values()

        # Validar que todos los inputs sean numéricos y mayores a 0
        for key, val in inputs.items():
            if val is None or val <= 0:
                self.result_label.setText(f"Error: '{key}' debe ser un número positivo.")
                return

        self.result_label.setText(f"Figura: {shape} con valores {inputs}")


def main():
    """Función principal para ejecutar la aplicación."""
    app = QApplication(sys.argv)
    window = ShapeSelector()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
