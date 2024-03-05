# Copyright 2023-2024 Parker Owan.  All rights reserved.

import os
from dataclasses import dataclass

from PyQt5.QtWidgets import QAction, QMainWindow, QMessageBox
from PyQt5.QtGui import QKeySequence, QDesktopServices, QIcon
from PyQt5.QtCore import QUrl, Qt

from corolab import TEMPLATES_PATH, CL_PROJECT_FILE_EXT
import corolab

from corolab_app.constants import ICON_PATH, APP_TITLE
from corolab_app.content import CLContentHandler
from corolab_app.log import CLTextLoggerWidget
from corolab_app.editor.tree import CLProjectTree
from corolab_app.editor.table import CLPropertyTable

TUTORIALS_URL = "https://www.vesperrobotics.com/community"


class NewProjectAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(NewProjectAction, self).__init__("New Project", window)
        self.setShortcuts(QKeySequence.New)
        self.setStatusTip("Create a new project")
        self.triggered.connect(contents.newProject)


class OpenProjectAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(OpenProjectAction, self).__init__("Open...", window)
        self.setShortcuts(QKeySequence.Open)
        self.setStatusTip("Open an existing project")
        self.triggered.connect(contents.openProject)


class OpenTemplateAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler,
                 filepath: str):
        _, file = os.path.split(filepath)
        name = self._cleanFilename(file)
        super(OpenTemplateAction, self).__init__(name, window)
        self._filepath = filepath
        self.setStatusTip("Create a new project from template")
        self.triggered.connect(
            lambda: contents.openTemplate(filename=self._filepath))

    @staticmethod
    def _cleanFilename(name: str):
        return name.replace("_", " ").replace(CL_PROJECT_FILE_EXT,
                                              "").capitalize()


class SaveProjectAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(SaveProjectAction, self).__init__("Save", window)
        self.setShortcuts(QKeySequence.Save)
        self.setStatusTip("Save project to file")
        self.triggered.connect(contents.saveProject)


class SaveProjectAsAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(SaveProjectAsAction, self).__init__("Save as...", window)
        self.setShortcuts(QKeySequence.SaveAs)
        self.setStatusTip("Save project as a new file")
        self.triggered.connect(contents.saveProjectAs)


class QuitAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(QuitAction, self).__init__("Quit", window)
        self.setShortcuts(QKeySequence.Quit)
        self.setStatusTip("Quit CoroLab")
        self.triggered.connect(contents.quit)


class AddFrankaPandaRobot(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddFrankaPandaRobot, self).__init__("Franka-Emika Panda", window)
        self.setStatusTip("Add a Franka-Emika Panda robot")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "franka_panda_robot.png")))
        self.triggered.connect(
            lambda: contents.addRobot(robot_t="FrankaPandaRobot"))


class AddUR3eRobot(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddUR3eRobot, self).__init__("UR-3e Robot", window)
        self.setStatusTip("Add a UR-3e robot")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "ur3e_robot.png")))
        self.triggered.connect(lambda: contents.addRobot(robot_t="UR3eRobot"))


class AddUR5eRobot(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddUR5eRobot, self).__init__("UR-5e Robot", window)
        self.setStatusTip("Add a UR-5e robot")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "ur5e_robot.png")))
        self.triggered.connect(lambda: contents.addRobot(robot_t="UR5eRobot"))


class AddUR10eRobot(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddUR10eRobot, self).__init__("UR-10e Robot", window)
        self.setStatusTip("Add a UR-10e robot")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "ur10e_robot.png")))
        self.triggered.connect(lambda: contents.addRobot(robot_t="UR10eRobot"))


class AddRobotiqGripper2F85(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddRobotiqGripper2F85, self).__init__("Robotiq 2F-85", window)
        self.setStatusTip("Add a Robotiq 2F-85 gripper")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "robotiq_2f85.png")))
        self.triggered.connect(
            lambda: contents.addEffector(effector_t="RobotiqGripper2F85"))


class AddFrankaHand(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddFrankaHand, self).__init__("Franka Hand", window)
        self.setStatusTip("Add a Franka Hand gripper")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "franka_hand.png")))
        self.triggered.connect(
            lambda: contents.addEffector(effector_t="FrankaHand"))


class AddToolFrame(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddToolFrame, self).__init__("Tool Frame", window)
        self.setStatusTip("Add a Tool Frame")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "tool_frame.png")))
        self.triggered.connect(contents.addToolFrame)


class AddCustomItem(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddCustomItem, self).__init__("Custom Item", window)
        self.setStatusTip("Add a Custom item")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "item.png")))
        self.triggered.connect(lambda: contents.addItem(item_t="CustomItem"))


class AddDesk(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddDesk, self).__init__("Desk", window)
        self.setStatusTip("Add a Desk item")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "item.png")))
        self.triggered.connect(lambda: contents.addItem(item_t="Desk"))


class AddTaskRegion(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddTaskRegion, self).__init__("Task Region", window)
        self.setStatusTip("Add a Task Region")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "task_region.png")))
        self.triggered.connect(contents.addTaskRegion)


class AddRealsenseD435i(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddRealsenseD435i, self).__init__("Realsense D435i", window)
        self.setStatusTip("Add a Realsense D435i camera")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "realsense_d435i.png")))
        self.triggered.connect(
            lambda: contents.addCamera(camera_t="RealsenseD435i"))


class AddRealsenseD405(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddRealsenseD405, self).__init__("Realsense D405", window)
        self.setStatusTip("Add a Realsense D405 camera")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "realsense_d405.png")))
        self.triggered.connect(
            lambda: contents.addCamera(camera_t="RealsenseD405"))


class AddVisualMarker(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(AddVisualMarker, self).__init__("Visual Marker", window)
        self.setStatusTip("Add a Visual Marker fiducial")
        self.setIcon(QIcon(os.path.join(ICON_PATH, "fiducial.png")))
        self.triggered.connect(
            lambda: contents.addFiducial(fiducial_t="VisualMarker"))


class AddItemAction(QAction):

    def __init__(
        self,
        window: QMainWindow,
        name: str,
        status: str,
        icon: str,
        callback: callable,
        type_t: type,
    ):
        super(AddItemAction, self).__init__(name, window)
        self.setStatusTip(status)
        self.setIcon(QIcon(os.path.join(ICON_PATH, icon)))
        self.triggered.connect(lambda: callback(type_t=type_t))


class ResetViewerAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(ResetViewerAction, self).__init__("Reset Viewer", window)
        self.setStatusTip("View zoom and position of viewer")
        self.triggered.connect(contents.resetViewer)


class SaveScreenshotAction(QAction):

    def __init__(self, window: QMainWindow, contents: CLContentHandler):
        super(SaveScreenshotAction, self).__init__("Save Screenshot...",
                                                   window)
        self.setStatusTip("Save viewer screenshot")
        self.triggered.connect(contents.screenshotViewer)


class ViewLoggingBarAction(QAction):

    def __init__(self, window: QMainWindow, widget: CLTextLoggerWidget):
        super(ViewLoggingBarAction, self).__init__("Logging Bar", window)
        self.setShortcuts(QKeySequence(Qt.CTRL + Qt.Key_L))
        self.setStatusTip("View logging bar")
        self.setCheckable(True)
        self.triggered.connect(widget.setVisible)
        self.setChecked(True)


class ViewProjectTreeAction(QAction):

    def __init__(self, window: QMainWindow, widget: CLProjectTree):
        super(ViewProjectTreeAction, self).__init__("Project Tree", window)
        self.setShortcuts(QKeySequence(Qt.CTRL + Qt.Key_T))
        self.setStatusTip("View project tree")
        self.setCheckable(True)
        self.triggered.connect(widget.setVisible)
        self.setChecked(True)


class ViewPropertyTableAction(QAction):

    def __init__(self, window: QMainWindow, widget: CLPropertyTable):
        super(ViewPropertyTableAction, self).__init__("Property Table", window)
        self.setShortcuts(QKeySequence(Qt.CTRL + Qt.Key_P))
        self.setStatusTip("View property table")
        self.setCheckable(True)
        self.triggered.connect(widget.setVisible)
        self.setChecked(True)


class HelpTutorialsAction(QAction):

    def __init__(self, window: QMainWindow):
        super(HelpTutorialsAction, self).__init__("Tutorials", window)
        self.setStatusTip("Visit CoroLab tutorials")
        self.triggered.connect(self.openTutorials)

    def openTutorials(self):
        QDesktopServices.openUrl(QUrl(TUTORIALS_URL))


class AboutAction(QAction):

    def __init__(self, window: QMainWindow):
        super(AboutAction, self).__init__("About CoroLab", window)
        self._window = window
        self.setStatusTip("View CoroLab information")
        self.triggered.connect(self.openAbout)

    def openAbout(self):
        QMessageBox.information(
            self._window,
            "About CoroLab",
            f"""
            {APP_TITLE}
            Version: {corolab.__version__}
            """,
            QMessageBox.Ok,
        )


@dataclass
class Entry:
    name: str
    status: str
    icon: str
    type_t: str


FLOW_BEHAVIOR_LIST = [
    Entry(name="Repeat Routine",
          status="Add a Repeat Routine behavior",
          icon="repeat.png",
          type_t=corolab.RepeatRoutine),
    Entry(name="Sequence Routine",
          status="Add a Sequence Routine behavior",
          icon="sequence.png",
          type_t=corolab.SequenceRoutine),
    Entry(name="Sleep Routine",
          status="Add a Sleep Routine behavior",
          icon="sleep.png",
          type_t=corolab.SleepRoutine),
    Entry(name="Start Recording Data",
          status="Add a Start Recording Data behavior",
          icon="start_record_data.png",
          type_t=corolab.StartRecordingData),
    Entry(name="Stop Recording Data",
          status="Add a Stop Recording Data behavior",
          icon="stop_record_data.png",
          type_t=corolab.StopRecordingData),
]

PERCEPTION_BEHAVIOR_LIST = [
    Entry(name="Initialize Perception",
          status="Add an Initialize Perception behavior",
          icon="vision.png",
          type_t=corolab.InitializePerception),
    Entry(name="Shutdown Perception",
          status="Add a Shutdown Perception behavior",
          icon="vision.png",
          type_t=corolab.ShutdownPerception),
    Entry(name="Calibrate Camera from Markers",
          status="Add a Calibrate Camera from Markers behavior",
          icon="vision.png",
          type_t=corolab.CalibrateCameraFromMarkers),
    Entry(name="Record Images",
          status="Add a Record Images behavior",
          icon="vision.png",
          type_t=corolab.RecordImages),
    Entry(name="Perspective Crop Image",
          status="Add a Perspective Crop Image behavior",
          icon="vision.png",
          type_t=corolab.PerspectiveCropImage),
]

MOTION_BEHAVIOR_LIST = [
    Entry(name="Initialize Controller",
          status="Add an Initialize Controller behavior",
          icon="control.png",
          type_t=corolab.InitializeController),
    Entry(name="Shutdown Controller",
          status="Add a Shutdown Controller behavior",
          icon="control.png",
          type_t=corolab.ShutdownController),
    Entry(name="Goto Target Positions",
          status="Add a Goto Target Positions behavior",
          icon="motion.png",
          type_t=corolab.GotoTargetPositions),
    Entry(name="Screw Along Last Axis",
          status="Add a Screw Along Last Axis behavior",
          icon="motion.png",
          type_t=corolab.ScrewAlongLastAxis),
    Entry(name="Generate Target Poses",
          status="Add a Generate Target Poses behavior",
          icon="motion.png",
          type_t=corolab.GenerateTargetPoses),
    Entry(name="Open Gripper",
          status="Add an Open Gripper behavior",
          icon="control.png",
          type_t=corolab.OpenGripper),
    Entry(name="Close Gripper",
          status="Add a Close Gripper behavior",
          icon="control.png",
          type_t=corolab.CloseGripper),
    Entry(name="Set Gripper Positions",
          status="Add a Set Gripper Positions behavior",
          icon="control.png",
          type_t=corolab.SetEffectorPositions),
]

MANIPULATION_BEHAVIOR_LIST = [
    Entry(name="Align Item to Tool",
          status="Add an Align Item to Tool behavior",
          icon="align.png",
          type_t=corolab.AlignItemToTool),
    Entry(name="Attach Item to Tool",
          status="Add an Attach Item to Tool behavior",
          icon="attach.png",
          type_t=corolab.AttachItemToTool),
    Entry(name="Detach Item from Tool",
          status="Add a Detach Item from Tool behavior",
          icon="detach.png",
          type_t=corolab.DetachItemFromTool),
]

BEHAVIOR_DICT = {
    "Flow": FLOW_BEHAVIOR_LIST,
    "Perception": PERCEPTION_BEHAVIOR_LIST,
    "Motion": MOTION_BEHAVIOR_LIST,
    "Manipulation": MANIPULATION_BEHAVIOR_LIST,
}

VARIABLES_LIST = [
    Entry(name="Motion Limits",
          status="Add a Motion Limits variable",
          icon="bounds.png",
          type_t=corolab.MotionLimits),
    Entry(name="Joint Position Target",
          status="Add a Joint Position Target variable",
          icon="target.png",
          type_t=corolab.JointPositionTarget),
    Entry(name="Task Region Target",
          status="Add a Task Region Target variable",
          icon="target.png",
          type_t=corolab.TaskRegionTarget),
    Entry(name="Mixture Target",
          status="Add a Mixture Target variable",
          icon="target.png",
          type_t=corolab.MixtureTarget),
]


class CLActions:

    def __init__(
        self,
        window: QMainWindow,
        contents: CLContentHandler,
        logger_bar: CLTextLoggerWidget,
        project_tree: CLProjectTree,
        property_table: CLPropertyTable,
    ):
        self.new_action = NewProjectAction(window, contents)
        self.open_action = OpenProjectAction(window, contents)
        self.open_templates = []
        for filename in os.listdir(TEMPLATES_PATH):
            filepath = os.path.join(TEMPLATES_PATH, filename)
            if filepath.endswith(CL_PROJECT_FILE_EXT):
                self.open_templates.append(
                    OpenTemplateAction(window, contents, filepath))
        self.save_action = SaveProjectAction(window, contents)
        self.save_as_action = SaveProjectAsAction(window, contents)
        self.quit_action = QuitAction(window, contents)

        self.add_franka_panda_robot = AddFrankaPandaRobot(window, contents)
        self.add_ur3e_robot = AddUR3eRobot(window, contents)
        self.add_ur5e_robot = AddUR5eRobot(window, contents)
        self.add_ur10e_robot = AddUR10eRobot(window, contents)

        self.add_tool_frame = AddToolFrame(window, contents)
        self.add_robotiq_2f85 = AddRobotiqGripper2F85(window, contents)
        self.add_franka_hand = AddFrankaHand(window, contents)

        self.add_task_region = AddTaskRegion(window, contents)
        self.add_custom_item = AddCustomItem(window, contents)
        self.add_desk = AddDesk(window, contents)

        self.add_visual_marker = AddVisualMarker(window, contents)
        self.add_realsense_d435i = AddRealsenseD435i(window, contents)
        self.add_realsense_d405 = AddRealsenseD405(window, contents)

        self.add_behaviors = {}
        for key, value in BEHAVIOR_DICT.items():
            self.add_behaviors[key] = []
            for entry in value:
                self.add_behaviors[key].append(
                    AddItemAction(window,
                                  name=entry.name,
                                  status=entry.status,
                                  icon=entry.icon,
                                  callback=contents.addBehavior,
                                  type_t=entry.type_t))

        self.add_variables = []
        for entry in VARIABLES_LIST:
            self.add_variables.append(
                AddItemAction(window,
                              name=entry.name,
                              status=entry.status,
                              icon=entry.icon,
                              callback=contents.addVariable,
                              type_t=entry.type_t))

        self.reset_viewer_action = ResetViewerAction(window, contents)
        self.save_screenshot_action = SaveScreenshotAction(window, contents)
        self.view_logging_bar_action = ViewLoggingBarAction(window, logger_bar)
        self.view_project_tree_action = ViewProjectTreeAction(
            window, project_tree)
        self.view_property_table_action = ViewPropertyTableAction(
            window, property_table)
        self.help_tutorials_action = HelpTutorialsAction(window)
        self.about_action = AboutAction(window)
