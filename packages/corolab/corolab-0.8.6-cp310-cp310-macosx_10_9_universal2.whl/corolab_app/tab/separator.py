# Copyright 2023-2024 Parker Owan.  All rights reserved.

from PyQt5.QtWidgets import QFrame


class CLSeparator(QFrame):

    def __init__(self):
        super().__init__()
        self.setFrameShape(self.VLine)
        self.setStyleSheet("""
            QFrame[frameShape="4"],
            QFrame[frameShape="5"]
            {
                border: none;
                background: rgb(228, 229, 241);
            }
        """)
