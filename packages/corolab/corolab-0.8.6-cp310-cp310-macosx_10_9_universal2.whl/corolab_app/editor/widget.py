# Copyright 2023-2024 Parker Owan.  All rights reserved.

from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QSpinBox,
    QAbstractSpinBox,
    QSlider,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
)

COL_0_MIN_WIDTH = 140
COL_0_STRETCH = 0
COL_1_MIN_WIDTH = 80
COL_1_STRETCH = 1
COL_2_MIN_WIDTH = 100

MAX_INT = 2**32 / 2 - 1


class CLMissingOptionWidget(QLabel):

    def __init__(self, parent: QWidget, name: str):
        super(CLMissingOptionWidget, self).__init__(
            f"No {name} in this Project",
            parent=parent,
        )
        self.setStyleSheet("QWidget { color: rgb(255, 41, 41); }")


class CLStrWidget(QWidget):

    def __init__(self, parent: QWidget, name: str, value: str,
                 callback: callable):
        super(CLStrWidget, self).__init__(parent)
        grid = QGridLayout()
        grid.setColumnMinimumWidth(0, COL_0_MIN_WIDTH)
        grid.setColumnStretch(0, COL_0_STRETCH)
        grid.setColumnMinimumWidth(1, COL_1_MIN_WIDTH)
        grid.setColumnStretch(1, COL_1_STRETCH)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)
        self.setLayout(grid)

        label = QLabel(name, parent=self)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(label, 0, 0)

        self._line_edit = QLineEdit(value, parent)
        grid.addWidget(self._line_edit, 0, 1)

        self._line_edit.textEdited.connect(callback)


class CLComboWidget(QWidget):

    def __init__(self, parent: QWidget, name: str, value: str,
                 options: List[str], callback: callable):
        super(CLComboWidget, self).__init__(parent)
        grid = QGridLayout()
        grid.setColumnMinimumWidth(0, COL_0_MIN_WIDTH)
        grid.setColumnStretch(0, COL_0_STRETCH)
        grid.setColumnMinimumWidth(1, COL_1_MIN_WIDTH)
        grid.setColumnStretch(1, COL_1_STRETCH)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)
        self.setLayout(grid)

        label = QLabel(name, parent=self)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(label, 0, 0)

        self._combo_box = QComboBox(parent)
        self._combo_box.addItems(options)
        grid.addWidget(self._combo_box, 0, 1)

        self._combo_box.currentTextChanged.connect(callback)
        if value in options:
            self._combo_box.setCurrentText(value)
        elif len(options) > 0:
            self._combo_box.setCurrentText(options[0])
            callback(self._combo_box.currentText())


class CLIntWidget(QWidget):

    def __init__(self, parent: QWidget, name: str, value: int,
                 callback: callable, min: int, max: int):
        super(CLIntWidget, self).__init__(parent)
        grid = QGridLayout()
        grid.setColumnMinimumWidth(0, COL_0_MIN_WIDTH)
        grid.setColumnStretch(0, COL_0_STRETCH)
        grid.setColumnMinimumWidth(1, COL_1_MIN_WIDTH)
        grid.setColumnStretch(1, COL_1_STRETCH)
        grid.setColumnMinimumWidth(2, COL_2_MIN_WIDTH)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)
        self.setLayout(grid)

        label = QLabel(name, parent=self)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(label, 0, 0)

        self._slider = QSlider(Qt.Horizontal, parent)
        self._slider.setFocusPolicy(Qt.StrongFocus)
        self._slider.wheelEvent = lambda event: None
        self._slider.setRange(min, max)
        grid.addWidget(self._slider, 0, 1)

        self._spin_box = QSpinBox(parent)
        self._spin_box.setFocusPolicy(Qt.StrongFocus)
        self._spin_box.wheelEvent = lambda event: None
        self._spin_box.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self._spin_box.setRange(min, max)
        self._spin_box.setSingleStep(1)
        grid.addWidget(self._spin_box, 0, 2)

        self._slider.sliderMoved.connect(self._spin_box.setValue)
        self._spin_box.valueChanged.connect(callback)
        self._spin_box.valueChanged.connect(self._slider.setValue)
        self._spin_box.setValue(value)


class CLIntUnboundedWidget(QWidget):

    def __init__(self, parent: QWidget, name: str, value: int,
                 callback: callable):
        super(CLIntUnboundedWidget, self).__init__(parent)

        grid = QGridLayout()
        grid.setColumnMinimumWidth(0, COL_0_MIN_WIDTH)
        grid.setColumnStretch(0, COL_0_STRETCH)
        grid.setColumnMinimumWidth(1, COL_1_MIN_WIDTH)
        grid.setColumnStretch(1, COL_1_STRETCH)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)
        self.setLayout(grid)

        label = QLabel(name, parent=self)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(label, 0, 0)

        self._spin_box = QSpinBox(parent)
        self._spin_box.setFocusPolicy(Qt.StrongFocus)
        self._spin_box.wheelEvent = lambda event: None
        self._spin_box.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self._spin_box.setRange(-MAX_INT, MAX_INT)
        self._spin_box.setSingleStep(1)
        grid.addWidget(self._spin_box, 0, 1)

        self._spin_box.valueChanged.connect(callback)
        self._spin_box.setValue(value)


class CLFloatWidget(QWidget):

    def __init__(self, parent: QWidget, name: str, value: float,
                 callback: callable, min: float, max: float):
        super(CLFloatWidget, self).__init__(parent)
        grid = QGridLayout()
        grid.setColumnMinimumWidth(0, COL_0_MIN_WIDTH)
        grid.setColumnStretch(0, COL_0_STRETCH)
        grid.setColumnMinimumWidth(1, COL_1_MIN_WIDTH)
        grid.setColumnStretch(1, COL_1_STRETCH)
        grid.setColumnMinimumWidth(2, COL_2_MIN_WIDTH)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)
        self.setLayout(grid)

        label = QLabel(name, parent=self)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(label, 0, 0)

        self._slider = QSlider(Qt.Horizontal, parent)
        self._slider.setFocusPolicy(Qt.StrongFocus)
        self._slider.wheelEvent = lambda event: None
        self._slider.setRange(-1000, 1000)
        grid.addWidget(self._slider, 0, 1)

        self._spin_box = QDoubleSpinBox(parent)
        self._spin_box.setFocusPolicy(Qt.StrongFocus)
        self._spin_box.wheelEvent = lambda event: None
        self._spin_box.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self._spin_box.setRange(min, max)
        self._spin_box.setDecimals(4)
        self._spin_box.setSingleStep(0.01)
        grid.addWidget(self._spin_box, 0, 2)

        self._slider.sliderMoved.connect(self.setSpinValue)
        self._spin_box.valueChanged.connect(callback)
        self._spin_box.valueChanged.connect(self.setSliderValue)
        self._spin_box.setValue(value)

    def setSliderValue(self, x: float):
        xmax = self._spin_box.maximum()
        ymax = float(self._slider.maximum())
        xmin = self._spin_box.minimum()
        ymin = float(self._slider.minimum())
        K = (ymax - ymin) / (xmax - xmin)
        y = ymin + K * (x - xmin)
        self._slider.setValue(int(y))

    def setSpinValue(self, y: int):
        xmax = self._spin_box.maximum()
        ymax = float(self._slider.maximum())
        xmin = self._spin_box.minimum()
        ymin = float(self._slider.minimum())
        K = (ymax - ymin) / (xmax - xmin)
        x = xmin + (y - ymin) / K
        self._spin_box.setValue(x)


class CLFloatUnboundedWidget(QWidget):

    def __init__(self, parent: QWidget, name: str, value: float,
                 callback: callable):
        super(CLFloatUnboundedWidget, self).__init__(parent)
        grid = QGridLayout()
        grid.setColumnMinimumWidth(0, COL_0_MIN_WIDTH)
        grid.setColumnStretch(0, COL_0_STRETCH)
        grid.setColumnMinimumWidth(1, COL_1_MIN_WIDTH)
        grid.setColumnStretch(1, COL_1_STRETCH)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(10)
        self.setLayout(grid)

        label = QLabel(name, parent=self)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        grid.addWidget(label, 0, 0)

        self._spin_box = QDoubleSpinBox(parent)
        self._spin_box.setFocusPolicy(Qt.StrongFocus)
        self._spin_box.wheelEvent = lambda event: None
        self._spin_box.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self._spin_box.setRange(-1e12, 1e12)
        self._spin_box.setDecimals(4)
        self._spin_box.setSingleStep(0.01)
        grid.addWidget(self._spin_box, 0, 1)

        self._spin_box.valueChanged.connect(callback)
        self._spin_box.setValue(value)
