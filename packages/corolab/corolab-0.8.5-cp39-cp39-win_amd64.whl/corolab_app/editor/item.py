# Copyright 2023-2024 Parker Owan.  All rights reserved.

from __future__ import annotations
import numpy as np
from typing import List, Any, _GenericAlias
from enum import Enum
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QTableWidget,
)

import corolab

from corolab_app.container import CLProjectContainer
from corolab_app.editor.widget import (
    CLMissingOptionWidget,
    CLStrWidget,
    CLIntWidget,
    CLIntUnboundedWidget,
    CLFloatWidget,
    CLFloatUnboundedWidget,
    CLComboWidget,
)

# TODO: These should not come from here, they should come from the property or
# workspace global variables.
PROPERTY_MAX_POS_M = 2
PROPERTY_MIN_POS_M = -2
PROPERTY_MAX_ROT_RAD = 3.14
PROPERTY_MIN_ROT_RAD = -3.14
PROPERTY_MAX_JOINT = 3.14
PROPERTY_MIN_JOINT = -3.14
PROPERTY_MAX_INT = 60
PROPERTY_MIN_INT = 0
PROPERTY_MIN_FLOAT = 0
PROPERTY_MAX_FLOAT = 10.0


class CLTableItem(QWidget):

    def __init__(self, table: QTableWidget):
        super(CLTableItem, self).__init__(table)
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(10, 5, 10, 5)
        self._layout.setSpacing(5)
        self.setLayout(self._layout)


class CLNotImplementedItem(CLTableItem):

    def __init__(self, table: QTableWidget, property: corolab.Property):
        super(CLNotImplementedItem, self).__init__(table)
        message = f"Property '{property.name}' is not implemented"
        prop_name = QLabel(message, parent=self)
        self._layout.addWidget(prop_name)


class CLImmutableNameItem(CLTableItem):

    def __init__(self, table: QTableWidget, name: str, ptype: str):
        super(CLImmutableNameItem, self).__init__(table)
        prop_name = QLabel(f"{name} ({ptype})", parent=self)
        prop_name.setStyleSheet("QWidget { font: bold 12px; }")
        self._layout.addWidget(prop_name)


class CLImmutableBasicItem(CLTableItem):

    def __init__(self, table: QTableWidget, property: corolab.Property):
        super(CLImmutableBasicItem, self).__init__(table)
        units = ""
        if property.units:
            units = f" ({property.units})"
        label = f"{property.name}{units}: {property.value}"
        prop_name = QLabel(label, parent=self)
        self._layout.addWidget(prop_name)


class CLMissingOptionItem(CLTableItem):

    def __init__(self, table: QTableWidget, property: corolab.Property):
        super(CLMissingOptionItem, self).__init__(table)
        self._layout.addWidget(
            CLMissingOptionWidget(parent=self, name=property.name))


class CLMutableBoolItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutableBoolItem, self).__init__(table)
        self._property = property
        self._container = container
        label = f"{property.name}"
        if property.units:
            label += f" ({property.units})"
        prop_name = QCheckBox(label, parent=self)
        prop_name.setCheckState(self.toCheckState(property.value))
        self._layout.addWidget(prop_name)
        prop_name.stateChanged.connect(self.setChecked)

    def setChecked(self, state: int):
        if state == 0:
            self._property.value = False
        else:
            self._property.value = True
        self._container.rebuildViewer()

    @staticmethod
    def toCheckState(flag: bool) -> Qt.CheckState:
        if flag:
            return Qt.CheckState.Checked
        return Qt.CheckState.Unchecked


class CLMutableEnumItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutableEnumItem, self).__init__(table)
        self._property = property
        self._container = container
        label = f"{property.name}"
        if property.units:
            label += f" ({property.units})"
        self._layout.addWidget(
            CLComboWidget(parent=self,
                          name=label,
                          value=property.value.name,
                          options=[e.name for e in type(property.value)],
                          callback=self.setValue))

    def setValue(self, value: str):
        self._property.value = self._property.type[value]
        self._container.rebuildViewer()


class CLMutableStrWithOptionsItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutableStrWithOptionsItem, self).__init__(table)
        self._property = property
        self._container = container
        label = f"{property.name}"
        if property.units:
            label += f" ({property.units})"
        self._layout.addWidget(
            CLComboWidget(parent=self,
                          name=label,
                          value=property.value,
                          options=property.options,
                          callback=self.setValue))

    def setValue(self, value: str):
        self._property.value = value
        self._container.rebuildViewer()


class CLMutableStrItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutableStrItem, self).__init__(table)
        self._property = property
        self._container = container
        label = f"{property.name}"
        if property.units:
            label += f" ({property.units})"
        self._layout.addWidget(
            CLStrWidget(parent=self,
                        name=label,
                        value=property.value,
                        callback=self.setValue))

    def setValue(self, value: str):
        self._property.value = value
        self._container.viewer().render()


class CLMutableIntItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutableIntItem, self).__init__(table)
        self._property = property
        self._container = container
        label = f"{property.name}"
        if property.units:
            label += f" ({property.units})"
        if property.bounded:
            self._layout.addWidget(
                CLIntWidget(parent=self,
                            name=label,
                            value=property.value,
                            callback=self.setValue,
                            min=property.min,
                            max=property.max))
        else:
            self._layout.addWidget(
                CLIntUnboundedWidget(parent=self,
                                     name=label,
                                     value=property.value,
                                     callback=self.setValue))

    def setValue(self, value: int):
        self._property.value = value
        self._container.viewer().render()


class CLMutableFloatItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutableFloatItem, self).__init__(table)
        self._property = property
        self._container = container
        label = f"{property.name}"
        if property.units:
            label += f" ({property.units})"
        if property.bounded:
            self._layout.addWidget(
                CLFloatWidget(parent=self,
                              name=label,
                              value=property.value,
                              callback=self.setValue,
                              min=property.min,
                              max=property.max))
        else:
            self._layout.addWidget(
                CLFloatUnboundedWidget(parent=self,
                                       name=label,
                                       value=property.value,
                                       callback=self.setValue))

    def setValue(self, value: float):
        self._property.value = value
        self._container.viewer().render()


class CLMutablePoseItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutablePoseItem, self).__init__(table)
        self._property = property
        self._container = container
        self._pose = property.value

        prop_name = QLabel(property.name, parent=self)
        self._layout.addWidget(prop_name)
        for i, key in enumerate(["X", "Y", "Z"]):
            self._layout.addWidget(
                CLFloatWidget(parent=self,
                              name=f"Position {key} (m)",
                              value=self._pose.position()[i],
                              callback=self.makeSetPosCallback(i),
                              min=PROPERTY_MIN_POS_M,
                              max=PROPERTY_MAX_POS_M))
        for i, key in enumerate(["X", "Y", "Z"]):
            self._layout.addWidget(
                CLFloatWidget(parent=self,
                              name=f"Rotation {key} (rad)",
                              value=self._pose.orientation()[i],
                              callback=self.makeSetRotCallback(i),
                              min=PROPERTY_MIN_ROT_RAD,
                              max=PROPERTY_MAX_ROT_RAD))

    def setPos(self, i: int, value: float):
        self._pose._pos_xyz[i] = value
        self._property.value = self._pose
        self._container.viewer().render()

    def setRot(self, i: int, value: float):
        self._pose._rot_xyz[i] = value
        self._property.value = self._pose
        self._container.viewer().render()

    def makeSetPosCallback(self, i: int):

        def callback(v):
            self.setPos(i, v)

        return callback

    def makeSetRotCallback(self, i: int):

        def callback(v):
            self.setRot(i, v)

        return callback


class CLMutableArrayItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLMutableArrayItem, self).__init__(table)
        self._property = property
        self._container = container
        self._vector = property.value

        prop_name = QLabel(property.name, parent=self)
        self._layout.addWidget(prop_name)
        for i in range(len(self._vector)):
            if property.bounded:
                _min = property.min
                if isinstance(property.min, (list, np.ndarray)):
                    _min = property.min[i]
                _max = property.max
                if isinstance(property.max, (list, np.ndarray)):
                    _max = property.max[i]
                self._layout.addWidget(
                    CLFloatWidget(parent=self,
                                  name=f"Axis {i} ({property.units})",
                                  value=self._vector[i],
                                  callback=self.makeSetPosCallback(i),
                                  min=_min,
                                  max=_max))
            else:
                self._layout.addWidget(
                    CLFloatUnboundedWidget(
                        parent=self,
                        name=f"Axis {i} ({property.units})",
                        value=self._vector[i],
                        callback=self.makeSetPosCallback(i)))

    def setPos(self, i: int, value: float):
        self._vector[i] = value
        self._property.value = self._vector
        self._container.viewer().render()

    def makeSetPosCallback(self, i: int):

        def callback(v):
            self.setPos(i, v)

        return callback


class CLListItem(CLTableItem):

    def __init__(
        self,
        table: QTableWidget,
        property: corolab.Property,
        container: CLProjectContainer,
    ):
        super(CLListItem, self).__init__(table)
        self._property = property
        self._container = container
        self._values = property.value

        prop_name = QLabel(property.name, parent=self)
        prop_name.setStyleSheet("QWidget { font: bold 12px; }")
        self._layout.addWidget(prop_name)
        for i in range(len(self._values)):
            # TODO: Fix this brute force double nesting, improve encapsulation
            if type(self._values[i]) == str and property.options:
                self._layout.addWidget(
                    CLComboWidget(parent=self,
                                  name=f"Item {i}: ",
                                  value=self._values[i],
                                  options=property.options,
                                  callback=self.makeSetValueCallback(i)))
            elif type(self._values[i]) == str:
                widget = CLMissingOptionWidget(parent=self, name=property.name)
                self._layout.addWidget(widget)
            elif type(self._values[i]) == float:
                self._layout.addWidget(
                    CLFloatUnboundedWidget(
                        parent=self,
                        name=f"Item {i}: ",
                        value=self._values[i],
                        callback=self.makeSetValueCallback(i)))
            else:
                msg = f"Item {i}: Unsupported type {type(self._values[i])}"
                self._layout.addWidget(QLabel(msg))

    def setValue(self, i: int, value: Any):
        self._values[i] = value
        self._property.value = self._values
        self._container.viewer().render()

    def makeSetValueCallback(self, i: int):

        def callback(v):
            self.setValue(i, v)

        return callback


def createWidgetsFromProperties(
    table: QTableWidget,
    container: CLProjectContainer,
    item: corolab.WithProperties,
    name: str,
    ptype: str,
) -> List[QWidget]:
    properties = item.getProperties()
    widgets = []
    widgets.append(CLImmutableNameItem(table=table, name=name, ptype=ptype))
    for property in properties.values():
        widgets.extend(
            createWidgetsFromProperty(table=table,
                                      container=container,
                                      property=property))
    return widgets


def isList(ptype: Any) -> bool:
    return isinstance(ptype, _GenericAlias) and ptype.__origin__ == list


def createWidgetsFromProperty(
    table: QTableWidget,
    container: CLProjectContainer,
    property: corolab.Property,
) -> List[QWidget]:
    widget = None
    if isList(property.type) and property.mutable:
        widget = CLListItem(table=table,
                            container=container,
                            property=property)
    elif isinstance(property.value, corolab.WithProperties):
        return createWidgetsFromProperties(table=table,
                                           container=container,
                                           item=property.value,
                                           name=property.name,
                                           ptype=property.value.type())
    elif property.type in (int, float, str) and not property.mutable:
        widget = CLImmutableBasicItem(table=table, property=property)
    elif isinstance(property.value, Enum) and property.mutable:
        widget = CLMutableEnumItem(table=table,
                                   property=property,
                                   container=container)
    elif property.type == bool and property.mutable:
        widget = CLMutableBoolItem(table=table,
                                   property=property,
                                   container=container)
    elif property.type == str and property.mutable and property.options:
        widget = CLMutableStrWithOptionsItem(table=table,
                                             property=property,
                                             container=container)
    elif (property.type == str and property.mutable
          and property.options is not None):
        widget = CLMissingOptionItem(table=table, property=property)
    elif property.type == str and property.mutable:
        widget = CLMutableStrItem(table=table,
                                  property=property,
                                  container=container)
    elif property.type == int and property.mutable:
        widget = CLMutableIntItem(table=table,
                                  property=property,
                                  container=container)
    elif property.type == float and property.mutable:
        widget = CLMutableFloatItem(table=table,
                                    property=property,
                                    container=container)
    elif property.type == corolab.Pose and property.mutable:
        widget = CLMutablePoseItem(table=table,
                                   property=property,
                                   container=container)
    elif property.type == np.ndarray and property.mutable:
        widget = CLMutableArrayItem(table=table,
                                    property=property,
                                    container=container)
    else:
        widget = CLNotImplementedItem(table=table, property=property)
    return [widget]
