from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, QHBoxLayout
import sys
import random
import pandas as pd
from warehouse_test import test
from charts import plot_analysis
import os

class WarehouseApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Генерация данных склада")
        self.setGeometry(100, 100, 500, 800)  # Adjusted height for additional inputs
        layout = QVBoxLayout()

        self.num_tests_label = QLabel("Количество тестов:")
        layout.addWidget(self.num_tests_label)
        self.num_tests_input = QLineEdit()
        self.num_tests_input.setText("10")  # Default value
        layout.addWidget(self.num_tests_input)

        self.seed_label = QLabel("Ключ генерации:")
        layout.addWidget(self.seed_label)
        self.seed_input = QLineEdit()
        self.seed_input.setText("42")  # Default value
        layout.addWidget(self.seed_input)
        self.random_seed_checkbox = QCheckBox("Использовать случайное значение")
        layout.addWidget(self.random_seed_checkbox)

        self.num_shelves_label = QLabel("Количество стеллажей:")
        layout.addWidget(self.num_shelves_label)
        self.num_shelves_layout = QHBoxLayout()
        self.num_shelves_min_input = QLineEdit()
        self.num_shelves_min_input.setPlaceholderText("Минимум")
        self.num_shelves_min_input.setText("10")  # Default value
        self.num_shelves_layout.addWidget(self.num_shelves_min_input)
        self.num_shelves_max_input = QLineEdit()
        self.num_shelves_max_input.setPlaceholderText("Максимум")
        self.num_shelves_max_input.setText("50")  # Default value
        self.num_shelves_layout.addWidget(self.num_shelves_max_input)
        layout.addLayout(self.num_shelves_layout)

        self.num_types_label = QLabel("Количество типов товаров:")
        layout.addWidget(self.num_types_label)
        self.num_types_layout = QHBoxLayout()
        self.num_types_min_input = QLineEdit()
        self.num_types_min_input.setPlaceholderText("Минимум")
        self.num_types_min_input.setText("5")  # Default value
        self.num_types_layout.addWidget(self.num_types_min_input)
        self.num_types_max_input = QLineEdit()
        self.num_types_max_input.setPlaceholderText("Максимум")
        self.num_types_max_input.setText("20")  # Default value
        self.num_types_layout.addWidget(self.num_types_max_input)
        layout.addLayout(self.num_types_layout)

        self.num_types_on_shelf_label = QLabel("Количество товаров на стеллаже:")
        layout.addWidget(self.num_types_on_shelf_label)
        self.num_types_on_shelf_layout = QHBoxLayout()
        self.num_types_on_shelf_min_input = QLineEdit()
        self.num_types_on_shelf_min_input.setPlaceholderText("Минимум")
        self.num_types_on_shelf_min_input.setText("5")  # Default value
        self.num_types_on_shelf_layout.addWidget(self.num_types_on_shelf_min_input)
        self.num_types_on_shelf_max_input = QLineEdit()
        self.num_types_on_shelf_max_input.setPlaceholderText("Максимум")
        self.num_types_on_shelf_max_input.setText("20")  # Default value
        self.num_types_on_shelf_layout.addWidget(self.num_types_on_shelf_max_input)
        layout.addLayout(self.num_types_on_shelf_layout)

        self.weight_range_label = QLabel("Диапазон веса:")
        layout.addWidget(self.weight_range_label)
        self.weight_range_layout = QHBoxLayout()

        self.weight_min_label = QLabel("Нижняя граница веса:")
        self.weight_range_layout.addWidget(self.weight_min_label)
        self.weight_min_lower_input = QLineEdit()
        self.weight_min_lower_input.setPlaceholderText("Минимум")
        self.weight_min_lower_input.setText("0.1")  # Default value
        self.weight_range_layout.addWidget(self.weight_min_lower_input)

        self.weight_min_upper_input = QLineEdit()
        self.weight_min_upper_input.setPlaceholderText("Максимум")
        self.weight_min_upper_input.setText("10.0")  # Default value
        self.weight_range_layout.addWidget(self.weight_min_upper_input)

        layout.addLayout(self.weight_range_layout)

        self.weight_upper_range_layout = QHBoxLayout()

        self.weight_upper_label = QLabel("Верхняя граница веса:")
        self.weight_upper_range_layout.addWidget(self.weight_upper_label)
        self.weight_max_lower_input = QLineEdit()
        self.weight_max_lower_input.setPlaceholderText("Минимум")
        self.weight_max_lower_input.setText("10.1")  # Default value
        self.weight_upper_range_layout.addWidget(self.weight_max_lower_input)

        self.weight_max_upper_input = QLineEdit()
        self.weight_max_upper_input.setPlaceholderText("Максимум")
        self.weight_max_upper_input.setText("50.0")  # Default value
        self.weight_upper_range_layout.addWidget(self.weight_max_upper_input)

        layout.addLayout(self.weight_upper_range_layout)

        self.error_range_label = QLabel("Погрешность:")
        layout.addWidget(self.error_range_label)
        self.error_range_layout = QHBoxLayout()

        self.error_min_input = QLineEdit()
        self.error_min_input.setPlaceholderText("Минимум")
        self.error_min_input.setText("0.01")  # Default value
        self.error_range_layout.addWidget(self.error_min_input)

        self.error_max_input = QLineEdit()
        self.error_max_input.setPlaceholderText("Максимум")
        self.error_max_input.setText("0.05")  # Default value
        self.error_range_layout.addWidget(self.error_max_input)

        layout.addLayout(self.error_range_layout)

        self.run_button = QPushButton("Запустить тест")
        self.run_button.clicked.connect(self.run_test)
        layout.addWidget(self.run_button)

        # Additional button for plotting charts
        self.plot_button = QPushButton("Построить диаграммы")
        self.plot_button.clicked.connect(self.plot_charts)
        layout.addWidget(self.plot_button)

        self.setLayout(layout)

    def plot_charts(self):
        try:
            file_name = "test_results.csv"

            if not os.path.exists(file_name):
                QMessageBox.warning(self, "Файл не найден", f"Файл '{file_name}' не найден. Сначала выполните тест.")
                return

            data = pd.read_csv(file_name)
            analysis_params = [
                'Кол-во товаров на стеллаже',
                'Кол-во стеллажей',
                'Минимальный вес товаров ',
                'Максимальный вес товаров'
            ]

            plot_analysis()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при построении диаграмм: {e}")

    def run_test(self):
        try:
            num_tests = int(self.num_tests_input.text())
            seed_value = int(self.seed_input.text()) if not self.random_seed_checkbox.isChecked() else random.randint(1, 100000)
            num_shelves_range = (int(self.num_shelves_min_input.text()), int(self.num_shelves_max_input.text()))
            num_types_of_goods_range = (int(self.num_types_min_input.text()), int(self.num_types_max_input.text()))
            num_types_of_goods_on_shelf_range = (int(self.num_types_on_shelf_min_input.text()), int(self.num_types_on_shelf_max_input.text()))


            weight_lower_range = (
                float(self.weight_min_lower_input.text()),
                float(self.weight_min_upper_input.text())
            )

            weight_upper_range = (
                float(self.weight_max_lower_input.text()),
                float(self.weight_max_upper_input.text())
            )

            error_range = (
                float(self.error_min_input.text()),
                float(self.error_max_input.text())
            )

            results_df = test(
                num_tests=num_tests,
                seed_value=seed_value,
                detailed_tests=[],
                num_shelves_range=num_shelves_range,
                num_types_of_goods_range=num_types_of_goods_range,
                weight_lower_range=weight_lower_range,
                weight_upper_range= weight_upper_range,
                num_goods_per_shelf=num_types_of_goods_on_shelf_range,
                error_range=error_range
            )

            results_df.to_csv("test_results.csv", index=False)
            QMessageBox.information(self, "Успех", "Тест завершен. Результаты сохранены в 'test_results.csv'.")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при выполнении теста: {e}")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = WarehouseApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
