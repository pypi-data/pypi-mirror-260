# Copyright 2023-2024 Parker Owan.  All rights reserved.

from PyQt5.QtWidgets import QWidget, QHBoxLayout

from corolab_app.content import CLContentHandler
from corolab_app.tab.button import CLToolButton
from corolab_app.tab.separator import CLSeparator


class CLExecuteTab(QWidget):

    def __init__(self, contents: CLContentHandler):
        super(CLExecuteTab, self).__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 2, 10, 2)
        self.setLayout(layout)
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="set_respawn.png",
                         help="Set the project respawn state",
                         callback=contents.recordRespawnState))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="reset_state.png",
                         help="Reset the project state",
                         callback=contents.resetState))
        layout.addWidget(
            CLToolButton(parent=self,
                         icon="play.png",
                         help="Run simulator (local)...",
                         callback=contents.runLocalSimulator))
        layout.addWidget(CLSeparator())
        layout.addStretch(1)
