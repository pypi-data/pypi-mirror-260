# Copyright 2023-2024 Parker Owan.  All rights reserved.

from PyQt5.QtWidgets import QTabWidget, QWidget

from corolab_app.content import CLContentHandler
from corolab_app.actions import CLActions
from corolab_app.tab.project import CLProjectTab
from corolab_app.tab.execute import CLExecuteTab

TAB_BAR_HEIGHT = 74

TAB_STYLE_SHEET = """
    QWidget {
        font: bold 13px;
        background: rgb(210, 211, 219);
        color: rgb(72, 75, 78);
    }

    QTabBar {
        background: rgb(228, 229, 241);
        qproperty-drawBase: 0;
    }

    QTabWidget::pane {
        border: 0px solid rgb(210, 211, 219);
        background: rgb(210, 211, 219);
        margin-bottom: 0px;
    }

    QTabWidget::tab-bar:top {
        top: 0px;
    }

    QTabWidget::tab-bar:bottom {
        bottom: 0px;
    }

    QTabWidget::tab-bar:left {
        right: 0px;
    }

    QTabWidget::tab-bar:right {
        left: 0px;
    }

    QTabBar::tab {
        border: 0px solid rgb(228, 229, 241);
        background: rgb(228, 229, 241);
    }

    QTabBar::tab:selected {
        background: rgb(210, 211, 219);
        color: rgb(42, 44, 46);
    }

    QTabBar::tab:!selected:hover {
        background: rgb(147, 148, 165);
        color: rgb(250, 250, 250)
    }

    QTabBar::tab:top:!selected {
        margin-top: 3px;
    }

    QTabBar::tab:bottom:!selected {
        margin-bottom: 3px;
    }

    QTabBar::tab:top, QTabBar::tab:bottom {
        min-width: 8ex;
        margin-right: -1px;
        padding: 7px 12px 7px 12px;
    }

    QTabBar::tab:top:selected {
        border-bottom-color: none;
    }

    QTabBar::tab:bottom:selected {
        border-top-color: none;
    }

    QTabBar::tab:top:last, QTabBar::tab:bottom:last,
    QTabBar::tab:top:only-one, QTabBar::tab:bottom:only-one {
        margin-right: 0;
    }

    QTabBar::tab:left:!selected {
        margin-right: 3px;
    }

    QTabBar::tab:right:!selected {
        margin-left: 3px;
    }

    QTabBar::tab:left, QTabBar::tab:right {
        min-height: 6ex;
        margin-bottom: -1px;
        padding: 10px 5px 10px 5px;
    }

    QTabBar::tab:left:selected {
        border-left-color: none;
    }

    QTabBar::tab:right:selected {
        border-right-color: none;
    }

    QTabBar::tab:left:last, QTabBar::tab:right:last,
    QTabBar::tab:left:only-one, QTabBar::tab:right:only-one {
        margin-bottom: 0;
    }
"""


class CLTabWidget(QTabWidget):

    def __init__(self, contents: CLContentHandler, actions: CLActions):
        super(CLTabWidget, self).__init__()
        self._contents = contents
        self._actions = actions
        self.setStyleSheet(TAB_STYLE_SHEET)
        self.setFixedHeight(TAB_BAR_HEIGHT)
        self._createProjectTab()
        self._createExecuteTab()
        # self._createAnalyzeTab()
        # self._createDatasetTab()
        # self._createTrainTab()

    def _createProjectTab(self):
        widget = CLProjectTab(contents=self._contents, actions=self._actions)
        self.addTab(widget, "Project")

    def _createExecuteTab(self):
        widget = CLExecuteTab(self._contents)
        self.addTab(widget, "Execute")

    def _createAnalyzeTab(self):
        widget = QWidget()
        self.addTab(widget, "Analyze")

    def _createDatasetTab(self):
        widget = QWidget()
        self.addTab(widget, "Dataset")

    def _createTrainTab(self):
        widget = QWidget()
        self.addTab(widget, "Train")
