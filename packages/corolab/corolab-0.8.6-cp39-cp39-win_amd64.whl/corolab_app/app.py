# Copyright 2023-2024 Parker Owan.  All rights reserved.

import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QFrame,
)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
# import sip  # Need to import after PyQt5
import logging

from corolab_app.container import CLProjectContainer
from corolab_app.content import CLContentHandler
from corolab_app.constants import ICON_PATH, APP_TITLE
from corolab_app.actions import CLActions
from corolab_app.tab.widget import CLTabWidget
from corolab_app.menu import CLMenuBar
from corolab_app.log import CLTextLoggerWidget
from corolab_app.status import CLStatusBarWidget
from corolab_app.editor.tree import CLProjectTree
from corolab_app.editor.table import CLPropertyTable

MAIN_WINDOW_DEFAULT_WIDTH = 900
MAIN_WINDOW_DEFAULT_HEIGHT = 600
SPLITTER_HANDLE_WIDTH = 2


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(MAIN_WINDOW_DEFAULT_WIDTH, MAIN_WINDOW_DEFAULT_HEIGHT)
        self.setWindowTitle(APP_TITLE)
        self._createContainer()
        self._createPropertyTable()
        self._createProjectTree()
        self._createStatusBar()
        self._createContents()
        self._createVtkWindow()
        self._createLoggerBar()
        self._createActions()
        self._createTabBar()
        self._createMenuBar()

        # GUI
        self._createGui()

        # Timers
        # self.createConnectionTimer()
        # self.createFeedbackTimer()

        # TODO: This causes significant energy utilization
        # self.createRenderTimer()
        logging.info("Initialized application")

    def _createContainer(self):
        self._container = CLProjectContainer()

    def _createPropertyTable(self):
        self._property_table = CLPropertyTable(container=self._container)

    def _createProjectTree(self):
        self._project_tree = CLProjectTree(
            container=self._container,
            table=self._property_table,
        )

    def _createStatusBar(self):
        self._status_bar = CLStatusBarWidget()

    def _createContents(self):
        self._contents = CLContentHandler(
            window=self,
            container=self._container,
            project_tree=self._project_tree,
            status_bar=self._status_bar,
        )

    def _createVtkWindow(self):
        self._frame = QFrame()
        self._vtk_window = QVTKRenderWindowInteractor(self._frame)
        self._contents.viewer()._setWindow(
            window=self._vtk_window.GetRenderWindow())

    def _createLoggerBar(self):
        self._logger_bar = CLTextLoggerWidget()

    def _createActions(self):
        self._actions = CLActions(
            window=self,
            contents=self._contents,
            logger_bar=self._logger_bar,
            project_tree=self._project_tree,
            property_table=self._property_table,
        )

    def _createTabBar(self):
        self._tab_bar = CLTabWidget(
            contents=self._contents,
            actions=self._actions,
        )

    def _createMenuBar(self):
        self._menu_bar = CLMenuBar(
            window=self,
            actions=self._actions,
        )

    def _createGui(self):
        # ---------------------------------------------
        # TAB
        # ---------------------------------------------
        #                      |
        #                      |
        # ---------------------|
        #                      |
        #                      |
        # ---------------------------------------------
        #
        # ---------------------------------------------
        #
        # ---------------------------------------------

        CENTRAL_WIDGET_STYLE_SHEET = """
            QWidget {{
                background-color: rgb(228, 229, 241);
                border: 2px rgb(250, 250, 250);
            }}

            QSplitter::handle {{
                image: none;
                background: rgb(250, 250, 250);
            }}

            QSplitter::horizontal {{
                width: 3px;
                color: rgb(250, 250, 250);
            }}

            QSplitter::vertical {{
                width: 3px;
                color: rgb(250, 250, 250);
            }}

            QBoxLayout {{
                color: rgb(250, 250, 250);
            }}

            QScrollBar:vertical {{
                border: none;
                background: rgb(147, 148, 165);
                width: 6px;
                border-radius: 3px;
            }}

            QScrollBar::handle:vertical {{
                border: none;
                background: rgb(186, 219, 245);
                width: 6px;
                border-radius: 3px;
            }}

            QScrollBar:horizontal {{
                border: none;
                background: rgb(147, 148, 165);
                height: 6px;
                border-radius: 3px;
            }}

            QScrollBar::handle:horizontal {{
                border: none;
                background: rgb(186, 219, 245);
                height: 6px;
                border-radius: 3px;
            }}

            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                width: none;
                height: none;
                background: none;
            }}

            QComboBox {{
                border: 1px solid rgb(210, 211, 219);
                border-radius: 3px;
                padding: 3px 18px 3px 3px;
                min-width: 6em;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 rgb(250, 250, 250),
                                            stop: 1.0 rgb(228, 229, 241));
            }}

            QComboBox:on {{ /* shift the text when the popup opens */
                padding-top: 3px;
                padding-left: 4px;
            }}

            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;

                border-left-width: 1px;
                border-left-color: rgb(228, 229, 241);
                border-left-style: solid; /* just a single line */
                border-top-right-radius: 3px; /* same radius as the QComboBox */
                border-bottom-right-radius: 3px;
            }}

            QComboBox::down-arrow {{
                image: url({icon});
                width: 20px;
                height: 20px;
            }}

            QComboBox::down-arrow:on {{ /* shift the arrow when popup is open */
                top: 1px;
                left: 1px;
            }}
        """.format(icon=os.path.join(ICON_PATH, "drop_down.png"))

        central_widget = QWidget()
        central_widget.setStyleSheet(CENTRAL_WIDGET_STYLE_SHEET)
        self.setCentralWidget(central_widget)

        self._gui_layout = QVBoxLayout()
        self._gui_layout.setContentsMargins(0, 0, 0, 0)
        self._gui_layout.setSpacing(0)
        self._gui_layout.addWidget(self._tab_bar)

        content_layout = QSplitter(Qt.Horizontal)
        content_layout.setHandleWidth(SPLITTER_HANDLE_WIDTH)
        content_layout.setContentsMargins(0, 0, 0, 0)
        self._gui_layout.addWidget(content_layout)

        editor_layout = QSplitter(Qt.Vertical)
        editor_layout.setHandleWidth(SPLITTER_HANDLE_WIDTH)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(editor_layout)

        editor_layout.addWidget(self._project_tree)
        editor_layout.addWidget(self._property_table)

        workspace_layout = QSplitter(Qt.Vertical)
        workspace_layout.setHandleWidth(SPLITTER_HANDLE_WIDTH)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(workspace_layout)

        workspace_layout.addWidget(self._vtk_window)
        workspace_layout.addWidget(self._logger_bar)

        self._gui_layout.addWidget(self._status_bar)

        central_widget.setLayout(self._gui_layout)

    def initialize(self):
        self._contents.viewer().init()
        self._contents.viewer().resetCamera()

    def render(self):
        self._contents.viewer().render()


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.initialize()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
