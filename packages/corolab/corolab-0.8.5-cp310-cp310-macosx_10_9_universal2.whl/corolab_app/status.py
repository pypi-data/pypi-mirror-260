# Copyright 2023-2024 Parker Owan.  All rights reserved.

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QTextEdit, QFrame

STATUS_BAR_HEIGHT = 25


class CLStatusBarWidget(QFrame):

    def __init__(self):
        super(CLStatusBarWidget, self).__init__()
        status_bar_layout = QHBoxLayout()
        status_bar_layout.setContentsMargins(0, 0, 0, 0)
        status_bar_layout.setSpacing(0)

        self.setLayout(status_bar_layout)
        self.setFixedHeight(STATUS_BAR_HEIGHT)

        self._code = QTextEdit()
        self._code.setReadOnly(True)

        status_bar_layout.addWidget(self._code)
        self.indicateReady()

    def indicateReady(self):
        self._code.setPlainText("Ready")
        self._code.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                QTextEdit {
                    font: bold 11px;
                    background-color: rgb(4, 4, 4);
                    color: white;
                }
            """)

    def indicateConnected(self):
        self._code.setPlainText("Connected to Client")
        self._code.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                QTextEdit { 
                    font: bold 11px;
                    background-color: rgb(4, 4, 40); 
                    color: white;
                }
            """)

    def indicateFaulted(self):
        self._code.setPlainText("Faulted")
        self._code.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                QTextEdit { 
                    font: bold 11px;
                    background-color: rgb(40, 4, 4); 
                    color: white;
                }
            """)

    def indicateCompleted(self):
        self._code.setPlainText("Completed")
        self._code.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                QTextEdit { 
                    font: bold 11px;
                    background-color: rgb(4, 40, 4); 
                    color: white;
                }
            """)

    def indicateRunningLocalSim(self):
        self._code.setPlainText("Running (Local Sim)")
        self._code.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                QTextEdit { 
                    font: bold 11px;
                    background-color: rgb(40, 4, 40); 
                    color: white;
                }
            """)

    def indicateRunningRemoteSim(self):
        self._code.setPlainText("Running (Remote Sim)")
        self._code.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                QTextEdit { 
                    font: bold 11px;
                    background-color: rgb(40, 4, 40); 
                    color: white;
                }
            """)

    def indicateRunningHardware(self):
        self._code.setPlainText("Running (Hardware)")
        self._code.setAlignment(Qt.AlignRight)
        self.setStyleSheet("""
                QTextEdit { 
                    font: bold 11px;
                    background-color: rgb(140, 60, 4); 
                    color: white;
                }
            """)
