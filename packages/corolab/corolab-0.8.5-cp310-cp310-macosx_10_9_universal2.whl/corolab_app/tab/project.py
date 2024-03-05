# Copyright 2023-2024 Parker Owan.  All rights reserved.

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QButtonGroup, QMenu)

from corolab_app.content import CLContentHandler
from corolab_app.actions import CLActions
from corolab_app.tab.button import CLToolButton
from corolab_app.tab.separator import CLSeparator

QMENU_STYLE_SHEET = """
    QMenu {
        background-color: rgba(238, 239, 246, 235);
        border-radius: 5px;
        border: 1px solid rgb(250, 250, 250);
        font: 13px;
        color: rgb(42, 44, 46);
    }

    QMenu::item { 
        height: 30px;
        width: 240px;
        margin: 2px;
        padding-left: 5px;
        border-radius: 5px;
    }

    QMenu::icon {
        padding-left: 10px;
    }
    
    QMenu::item:selected {
        border-color: rgb(147, 148, 165);
        background: rgba(186, 219, 245, 150);
    }

    QMenu::separator {
        height: 1px;
        background: rgb(228, 229, 241);
        margin-left: 5px;
        margin-right: 5px;
    }
"""


class CLProjectTab(QWidget):

    def __init__(self, contents: CLContentHandler, actions: CLActions):
        super(CLProjectTab, self).__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)
        self.setLayout(layout)
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="new_project.png",
                         help="New project",
                         callback=contents.newProject))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="open_project.png",
                         help="Open project...",
                         callback=contents.openProject))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="save.png",
                         help="Save project",
                         callback=contents.saveProject))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="save_as.png",
                         help="Save project as...",
                         callback=contents.saveProjectAs))
        layout.addWidget(CLSeparator())
        manipulator_group = QButtonGroup(parent=self)
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="drag_camera.png",
                         help="Set viewer to camera mode",
                         checkable=True,
                         checked=True,
                         group=manipulator_group,
                         callback=contents.setCameraMode))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="drag_teleop.png",
                         help="Set viewer to teleoperation mode...",
                         checkable=True,
                         group=manipulator_group,
                         callback=contents.setTeleoperationMode))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="reset_view.png",
                         help="Reset viewer",
                         callback=contents.resetViewer))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="screenshot.png",
                         help="Save viewer screenshot...",
                         callback=contents.screenshotViewer))
        layout.addWidget(CLSeparator())
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="robot.png",
                         help="Add robot...",
                         menu=self.MakeAddRobotMenu(actions=actions)))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="effector.png",
                         help="Add effector...",
                         menu=self.MakeAddEffectorMenu(actions=actions)))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="item.png",
                         help="Add item...",
                         menu=self.MakeAddItemMenu(actions=actions)))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="camera.png",
                         help="Add camera...",
                         menu=self.MakeAddCameraMenu(actions=actions)))
        layout.addWidget(CLSeparator())
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="sequence.png",
                         help="New flow behavior",
                         menu=self.MakeAddBehaviorMenu(actions=actions,
                                                       key="Flow")))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="vision.png",
                         help="New perception behavior",
                         menu=self.MakeAddBehaviorMenu(actions=actions,
                                                       key="Perception")))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="motion.png",
                         help="New motion behavior",
                         menu=self.MakeAddBehaviorMenu(actions=actions,
                                                       key="Motion")))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="move_item.png",
                         help="New manipulation behavior",
                         menu=self.MakeAddBehaviorMenu(actions=actions,
                                                       key="Manipulation")))
        layout.addWidget(CLSeparator())
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="target.png",
                         help="New variable",
                         menu=self.MakeAddVariableMenu(actions=actions)))
        layout.addStretch(1)

    @staticmethod
    def MakeAddRobotMenu(actions: CLActions) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet(QMENU_STYLE_SHEET)
        menu.addAction(actions.add_franka_panda_robot)
        menu.addAction(actions.add_ur3e_robot)
        menu.addAction(actions.add_ur5e_robot)
        menu.addAction(actions.add_ur10e_robot)
        return menu

    @staticmethod
    def MakeAddEffectorMenu(actions: CLActions) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet(QMENU_STYLE_SHEET)
        menu.addAction(actions.add_tool_frame)
        menu.addAction(actions.add_robotiq_2f85)
        menu.addAction(actions.add_franka_hand)
        return menu

    @staticmethod
    def MakeAddItemMenu(actions: CLActions) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet(QMENU_STYLE_SHEET)
        menu.addAction(actions.add_task_region)
        menu.addAction(actions.add_custom_item)
        menu.addAction(actions.add_desk)
        return menu

    @staticmethod
    def MakeAddCameraMenu(actions: CLActions) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet(QMENU_STYLE_SHEET)
        menu.addAction(actions.add_visual_marker)
        menu.addAction(actions.add_realsense_d435i)
        menu.addAction(actions.add_realsense_d405)
        return menu

    @staticmethod
    def MakeAddBehaviorMenu(actions: CLActions, key: str) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet(QMENU_STYLE_SHEET)
        for action in actions.add_behaviors[key]:
            menu.addAction(action)
        return menu

    @staticmethod
    def MakeAddVariableMenu(actions: CLActions) -> QMenu:
        menu = QMenu()
        menu.setStyleSheet(QMENU_STYLE_SHEET)
        for action in actions.add_variables:
            menu.addAction(action)
        return menu
