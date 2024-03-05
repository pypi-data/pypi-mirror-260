# Copyright 2023-2024 Parker Owan.  All rights reserved.

import os
import sys
import logging
from typing import Tuple, Any
import numpy as np

from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import (QFileDialog, QMainWindow, QDialog, QLabel,
                             QComboBox, QGridLayout, QDialogButtonBox, QWidget,
                             QLineEdit, QCheckBox, QSpinBox, QMessageBox)

import corolab

from corolab_app.container import CLProjectContainer
from corolab_app.editor.tree import CLProjectTree
from corolab_app.status import CLStatusBarWidget
from corolab_app.exception import logerror

DEFAULT_PATH = os.path.expanduser("~")
PROJECT_FILE_FILTER = f"CoroLab project file (*{corolab.CL_PROJECT_FILE_EXT})"
DEFAULT_PROJECT_SAVE = os.path.join(
    DEFAULT_PATH,
    "Documents",
    f"my_project{corolab.CL_PROJECT_FILE_EXT}",
)
IMAGE_FILE_FILTER = f"Png image file (*{corolab.CL_IMAGE_FILE_EXT})"
DEFAULT_IMAGE_SAVE = os.path.join(
    DEFAULT_PATH,
    "Desktop",
    f"screenshot{corolab.CL_IMAGE_FILE_EXT}",
)


class CLContentHandler:
    """
    Manages creation and access to CoroLab contents in the main application
    """

    def __init__(
        self,
        window: QMainWindow,
        container: CLProjectContainer,
        project_tree: CLProjectTree,
        status_bar: CLStatusBarWidget,
    ):
        self._respawn_state = None
        self._locked = False
        self._window = window
        self._container = container
        self._project_tree = project_tree
        self._status_bar = status_bar
        self._setupProject()
        self._simulator = None
        self._active_filename = None
        self._active_behavior = None
        self._active_robot = None
        self._active_tool = None

    def viewer(self) -> corolab.WorkspaceViewer:
        return self._container.viewer()

    def project(self) -> corolab.Project:
        return self._container.project()

    @logerror
    def quit(self):
        if CLMessageBox.userWantsToSaveProject(self._window):
            self.saveProject()
        sys.exit()

    @logerror
    def newProject(self):
        if self._locked:
            return
        if CLMessageBox.userWantsToSaveProject(self._window):
            self.saveProject()
        self._container.newProject()
        self._setupProject()
        self._active_filename = None
        logging.info("Created new project")

    @logerror
    def openProject(self):
        if self._locked:
            return
        if CLMessageBox.userWantsToSaveProject(self._window):
            self.saveProject()
        filename = CLFileDialog.getOpenFileName(
            parent=self._window,
            caption="Open file",
            filter=PROJECT_FILE_FILTER,
        )
        if filename:
            self._container.newProject()
            self._container.project().load(file=filename)
            self._setupProject()
            self._active_filename = filename
            logging.info(f"Opened project '{filename}'")

    @logerror
    def openTemplate(self, filename: str):
        if self._locked:
            return
        if CLMessageBox.userWantsToSaveProject(self._window):
            self.saveProject()
        if not os.path.exists(filename):
            logging.error("Unable to open template")
            return
        self._container.newProject()
        self._container.project().load(file=filename)
        self._setupProject()
        self._active_filename = None
        logging.info("Created new project from template")

    @logerror
    def saveProject(self):
        if self._locked:
            return
        if not self._active_filename:
            self.saveProjectAs()
            return
        self._container.project().save(file=self._active_filename)
        logging.info(f"Saved project '{self._active_filename}'")
        self.recordRespawnState()

    @logerror
    def saveProjectAs(self):
        if self._locked:
            return
        filename = CLFileDialog.getSaveFileName(
            parent=self._window,
            caption="Save file",
            directory=DEFAULT_PROJECT_SAVE,
            filter=PROJECT_FILE_FILTER,
        )
        if filename:
            self._active_filename = filename
            self._container.project().save(file=self._active_filename)
            logging.info("Saved file '{}'".format(self._active_filename))
            self.recordRespawnState()

    @logerror
    def setCameraMode(self):
        self._container.viewer().setCameraMode()

    @logerror
    def setTeleoperationMode(self):
        if self._locked:
            return
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.EXISTING_ROBOT_KEY: self._active_robot,
                CLSelectorDialog.EXISTING_TOOL_KEY: self._active_tool,
            },
        )
        if not params:
            return
        self._container.viewer().setTeleoperationMode(
            robot=params[CLSelectorDialog.EXISTING_ROBOT_KEY],
            tool=params[CLSelectorDialog.EXISTING_TOOL_KEY],
        )

    @logerror
    def resetViewer(self):
        self._container.viewer().resetCamera()
        self._container.viewer().render()

    @logerror
    def screenshotViewer(self):
        filename = CLFileDialog.getSaveFileName(
            parent=self._window,
            caption="Save image",
            directory=DEFAULT_IMAGE_SAVE,
            filter=IMAGE_FILE_FILTER,
        )
        if filename:
            self._container.viewer().screenshot(filename=filename)
            logging.info("Saved image '{}'".format(filename))

    @logerror
    def addRobot(self, robot_t: str):
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Robot",
            },
        )
        if not params:
            return
        if robot_t == "FrankaPandaRobot":
            corolab.FrankaPandaRobot(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        elif robot_t == "UR3eRobot":
            corolab.UR3eRobot(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        elif robot_t == "UR5eRobot":
            corolab.UR5eRobot(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        elif robot_t == "UR10eRobot":
            corolab.UR10eRobot(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        self._rebuildViewerAndTree()

    @logerror
    def addEffector(self, effector_t: str):
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Effector",
            },
        )
        if not params:
            return
        if effector_t == "RobotiqGripper2F85":
            corolab.RobotiqGripper2F85(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        elif effector_t == "FrankaHand":
            corolab.FrankaHand(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        self._rebuildViewerAndTree()

    @logerror
    def addToolFrame(self):
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Tool Frame",
                CLSelectorDialog.EXISTING_ROBOT_KEY: "",
            },
        )
        if not params:
            return
        tool_frame = corolab.ToolFrame(
            workspace=self._container.project().workspace(),
            name=params[CLSelectorDialog.NEW_NAME_KEY],
        )
        robot = self._container.project().workspace().getRobot(
            params[CLSelectorDialog.EXISTING_ROBOT_KEY])
        robot.addToolFrame(tool_frame=tool_frame)
        self._rebuildViewerAndTree()

    @logerror
    def addItem(self, item_t: str):
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Item",
            },
        )
        if not params:
            return
        if item_t == "CustomItem":
            corolab.CustomItem(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        elif item_t == "Desk":
            corolab.Desk(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        self._rebuildViewerAndTree()

    @logerror
    def addTaskRegion(self):
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Task Region",
            },
        )
        if not params:
            return
        corolab.TaskRegion(
            workspace=self._container.project().workspace(),
            name=params[CLSelectorDialog.NEW_NAME_KEY],
        )
        self._rebuildViewerAndTree()

    @logerror
    def addCamera(self, camera_t: str):
        # TODO: Add option to load intrinsics from file
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Camera",
            },
        )
        if not params:
            return
        if camera_t == "RealsenseD435i":
            corolab.RealsenseD435i(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        elif camera_t == "RealsenseD405":
            corolab.RealsenseD405(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        self._rebuildViewerAndTree()

    @logerror
    def addFiducial(self, fiducial_t: str):
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Fiducial",
            },
        )
        if not params:
            return
        if fiducial_t == "VisualMarker":
            corolab.VisualMarker(
                workspace=self._container.project().workspace(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
            )
        self._rebuildViewerAndTree()

    @logerror
    def addBehavior(self, type_t: type):
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={
                CLSelectorDialog.NEW_NAME_KEY: "My Behavior",
                CLSelectorDialog.PARENT_BEHAVIOR_KEY: None,
            },
        )
        if not params:
            return
        behavior = type_t(
            project=self._container.project(),
            name=params[CLSelectorDialog.NEW_NAME_KEY],
        )

        if params[CLSelectorDialog.PARENT_BEHAVIOR_KEY]:
            # TODO: This is too general, use the set<>(), add<>() calls of specific routines
            self._container.project().behaviors()[params[
                CLSelectorDialog.PARENT_BEHAVIOR_KEY]]._addChild(behavior)
        else:
            self._container.project().addProgram(behavior=behavior)

        self._rebuildViewerAndTree()

    @logerror
    def addVariable(self, type_t: type):
        params = {CLSelectorDialog.NEW_NAME_KEY: "My Variable"}
        if type_t == corolab.MotionLimits:
            params[CLSelectorDialog.EXISTING_ROBOT_KEY] = ""
        elif type_t == corolab.JointPositionTarget:
            params[CLSelectorDialog.EXISTING_ROBOT_KEY] = ""
            params[CLSelectorDialog.JOINT_POS_DISTRIBUTION_TYPE_KEY] = ""
        elif type_t == corolab.TaskRegionTarget:
            params[CLSelectorDialog.EXISTING_ROBOT_KEY] = ""
            params[CLSelectorDialog.USE_SEED_POSITIONS_KEY] = True
            params[CLSelectorDialog.JOINT_POS_DISTRIBUTION_TYPE_KEY] = ""
        elif type_t == corolab.MixtureTarget:
            params[CLSelectorDialog.NUMBER_OF_MIXTURES] = 1
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params=params,
        )
        if not params:
            return
        if type_t == corolab.MotionLimits:
            robot = self._container.project().workspace().getRobot(
                params[CLSelectorDialog.EXISTING_ROBOT_KEY])
            corolab.MotionLimits(
                project=self._container.project(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
                joint_velocity=np.ones(robot.getNumDofs()),
                joint_acceleration=np.ones(robot.getNumDofs()),
            )
        elif type_t == corolab.JointPositionTarget:
            robot = self._container.project().workspace().getRobot(
                params[CLSelectorDialog.EXISTING_ROBOT_KEY])
            corolab.JointPositionTarget(
                project=self._container.project(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
                joint_positions=corolab.Distribution.CreateFromTypename(
                    typename=params[
                        CLSelectorDialog.JOINT_POS_DISTRIBUTION_TYPE_KEY],
                    dim=robot.getNumDofs(),
                ),
            )
        elif type_t == corolab.TaskRegionTarget:
            robot = self._container.project().workspace().getRobot(
                params[CLSelectorDialog.EXISTING_ROBOT_KEY])
            seed_joint_positions = []
            if params[CLSelectorDialog.USE_SEED_POSITIONS_KEY]:
                seed_joint_positions = corolab.Distribution.CreateFromTypename(
                    typename=params[
                        CLSelectorDialog.JOINT_POS_DISTRIBUTION_TYPE_KEY],
                    dim=robot.getNumDofs(),
                )
            corolab.TaskRegionTarget(
                project=self._container.project(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
                pose_generator=corolab.PoseGenerator(
                    project=self._container.project()),
                seed_joint_positions=seed_joint_positions,
            )
        elif type_t == corolab.MixtureTarget:
            n = params[CLSelectorDialog.NUMBER_OF_MIXTURES]
            corolab.MixtureTarget(
                project=self._container.project(),
                name=params[CLSelectorDialog.NEW_NAME_KEY],
                target_generators=["" for _ in range(n)],
                weights=[1.0 for _ in range(n)],
            )
        self._rebuildViewerAndTree()

    @logerror
    def recordRespawnState(self):
        if self._locked:
            return
        logging.info(f"Recorded the project respawn state")
        self._respawn_state = self._container.project().workspace()._getState()

    @logerror
    def resetState(self):
        if self._locked:
            return
        if self._respawn_state is not None:
            logging.info(f"Reset the project state")
            self._container.project().workspace()._setState(
                self._respawn_state)
            self._container.viewer().render()

    @logerror
    def runLocalSimulator(self):
        if self._locked:
            return
        params = CLSelectorDialog.getParams(
            parent=self._window,
            project=self._container.project(),
            params={CLSelectorDialog.EXECUTE_BEHAVIOR_KEY: ""},
        )
        if not params:
            return
        simulator = corolab.Simulator(project=self._container.project(),
                                      viewer=self._container.viewer())
        # self._thread = _RunLocalSimulatorThread(
        #     simulator=simulator,
        #     behavior=params[CLSelectorDialog.EXECUTE_BEHAVIOR_KEY],
        # )

        # TODO: Only do this when the system is running.  It causes
        # significant energy utilization when running all the time.
        # self._render_timer = QTimer(self._window)
        # self._render_timer.timeout.connect(
        # lambda: self._container.viewer().render())
        # RENDER_TIMER_MS = 1000
        # self._render_timer.start(RENDER_TIMER_MS)

        # self._thread.started.connect(lambda: self._lock())
        # self._thread.started.connect(self._status_bar.indicateRunningLocalSim)
        # self._thread.succeeded.connect(self._status_bar.indicateCompleted)
        # self._thread.failed.connect(self._status_bar.indicateFaulted)
        # self._thread.finished.connect(self._render_timer.stop)
        # self._thread.finished.connect(lambda: self._unlock())
        # self._thread.start()

        # Run the simulator in the main thread
        self._status_bar.indicateRunningLocalSim()
        if simulator.runProgram(
                name=params[CLSelectorDialog.EXECUTE_BEHAVIOR_KEY]):
            self._status_bar.indicateCompleted()
        else:
            self._status_bar.indicateFaulted()

    def _rebuildViewerAndTree(self):
        self._container.rebuildViewer()
        self._project_tree.updateProjectTreeContent()

    def _setupProject(self):
        self._rebuildViewerAndTree()
        self._container.viewer()._getRenderer().ResetCamera()
        self._container.viewer().render()
        self._status_bar.indicateReady()
        self.recordRespawnState()

    def _lock(self):
        self._locked = True

    def _unlock(self):
        self._locked = False


# class _RunLocalSimulatorThread(QThread):
#     finished = pyqtSignal()
#     succeeded = pyqtSignal()
#     failed = pyqtSignal()

#     def __init__(self, simulator: corolab.Simulator, behavior: str):
#         super(_RunLocalSimulatorThread, self).__init__()
#         self._simulator = simulator
#         self._behavior = behavior

#     @logerror
#     def run(self):
#         if self._simulator.runProgram(name=self._behavior):
#             self.succeeded.emit()
#         else:
#             self.failed.emit()
#         self.finished.emit()


class CLSelectorDialog(QDialog):
    """A custom class for handling specialty inputs"""

    NEW_NAME_KEY = "Enter a Name"
    EXISTING_ROBOT_KEY = "Select a Robot"
    EXISTING_TOOL_KEY = "Select a Tool"
    EXECUTE_BEHAVIOR_KEY = "Select a Behavior to Execute"
    PARENT_BEHAVIOR_KEY = "Select a Parent Behavior"
    JOINT_POS_DISTRIBUTION_TYPE_KEY = "Select a Joint Position Distribution"
    USE_SEED_POSITIONS_KEY = "Use Explicit Seed Positions for IK"
    NUMBER_OF_MIXTURES = "Select the Number of Mixtures"

    def __init__(self, parent: QWidget, project: corolab.Project,
                 params: dict):
        super(CLSelectorDialog, self).__init__(parent)
        self._params = params

        layout = QGridLayout(self)

        i = 0
        for key, value in params.items():
            label = QLabel(key)
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            # Choose widget based on key
            editor = None
            if key == self.NEW_NAME_KEY:
                editor = QLineEdit(value)
                editor.textEdited.connect(self.makeSetParamCallback(key))
            elif key == self.EXISTING_ROBOT_KEY:
                editor = QComboBox()
                editor.addItems(project.workspace().getRobots())
                self._params[key] = editor.currentText()
                editor.currentTextChanged.connect(
                    self.makeSetParamCallback(key))
            elif key == self.EXISTING_TOOL_KEY:
                editor = QComboBox()
                editor.addItems(project.workspace().getToolFrames())
                self._params[key] = editor.currentText()
                editor.currentTextChanged.connect(
                    self.makeSetParamCallback(key))
            elif key == self.EXECUTE_BEHAVIOR_KEY:
                editor = QComboBox()
                editor.addItems([k for k in project.programs().keys()])
                self._params[key] = editor.currentText()
                editor.currentTextChanged.connect(
                    self.makeSetParamCallback(key))
            elif key == self.PARENT_BEHAVIOR_KEY:
                editor = QComboBox()
                editor.addItem(None)
                # Only grab behaviors that can have children, i.e. not an _Action
                for k, v in project.behaviors().items():
                    if not isinstance(v, corolab.Action):
                        editor.addItem(k)
                self._params[key] = editor.currentText()
                editor.currentTextChanged.connect(
                    self.makeSetParamCallback(key))
            elif key == self.JOINT_POS_DISTRIBUTION_TYPE_KEY:
                editor = QComboBox()
                editor.addItems(["Deterministic", "Uniform", "Gaussian"])
                self._params[key] = editor.currentText()
                editor.currentTextChanged.connect(
                    self.makeSetParamCallback(key))
            elif key == self.USE_SEED_POSITIONS_KEY:
                editor = QCheckBox()
                self._params[key] = editor.isChecked()
                editor.stateChanged.connect(self.makeSetParamCallback(key))
            elif key == self.NUMBER_OF_MIXTURES:
                editor = QSpinBox()
                editor.setRange(1, 100)
                self._params[key] = editor.value()
                editor.valueChanged.connect(self.makeSetParamCallback(key))
            else:
                raise NotImplementedError(
                    f"Internal error: '{key}' not implemented")

            layout.addWidget(label, i, 0)
            layout.addWidget(editor, i, 1)
            i += 1

        box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            centerButtons=True,
        )
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box, i, 0, 1, 2)

        self.resize(420, 60 * (i + 1))

    def setParam(self, key: str, value: Any):
        self._params[key] = value

    def makeSetParamCallback(self, key: str):

        def callback(value):
            self.setParam(key, value)

        return callback

    @staticmethod
    def getParams(
        parent: QWidget,
        project: corolab.Project,
        params: dict,
    ) -> Tuple[str, str]:
        dialog = CLSelectorDialog(parent=parent,
                                  project=project,
                                  params=params)
        if not dialog.exec_():
            return None
        return dialog._params


class CLFileDialog:

    @staticmethod
    def getSaveFileName(
        parent: QWidget,
        caption: str,
        directory: str,
        filter: str,
    ) -> str:
        dialog = QFileDialog(parent, caption, directory, filter)
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setViewMode(QFileDialog.Detail)
        if not dialog.exec_():
            return None
        filenames = dialog.selectedFiles()
        if len(filenames) != 1:
            return None
        return filenames[0]

    @staticmethod
    def getOpenFileName(
        parent: QWidget,
        caption: str,
        filter: str,
    ) -> str:
        dialog = QFileDialog(parent, caption, "", filter)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setViewMode(QFileDialog.Detail)
        if not dialog.exec_():
            return None
        filenames = dialog.selectedFiles()
        if len(filenames) != 1:
            return None
        return filenames[0]


class CLMessageBox:

    @staticmethod
    def warning(
        parent: QWidget,
        title: str,
        text: str,
        buttons: QMessageBox.StandardButtons,
        default: QMessageBox.StandardButton,
    ) -> QMessageBox.StandardButton:
        pass

    @staticmethod
    def userWantsToSaveProject(parent: QWidget) -> bool:
        dialog = QMessageBox(
            QMessageBox.Warning,
            "Save Project",
            "Would you like to save the project first?",
            QMessageBox.Yes | QMessageBox.No,
            parent,
        )
        dialog.setDefaultButton(QMessageBox.Yes)
        ret = dialog.exec_()
        if ret == QMessageBox.Yes:
            return True
        return False
