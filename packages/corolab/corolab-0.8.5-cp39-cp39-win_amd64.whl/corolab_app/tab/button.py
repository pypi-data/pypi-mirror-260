# Copyright 2023-2024 Parker Owan.  All rights reserved.

import os
from typing import Callable

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QToolButton, QMenu, QButtonGroup)

from corolab_app.constants import ICON_PATH

TAB_BUTTON_HEIGHT = 34
TAB_BUTTON_WIDTH = 34
TAB_BUTTON_DROPDOWN_WIDTH = 46
TAB_BUTTON_ICON_HEIGHT = 24
TAB_BUTTON_ICON_WIDTH = 24

QTOOLBUTTON_STYLE_SHEET = """
    QToolButton {{ /* all types of tool button */
        border: none;
        border-radius: 5px;
        background-color: transparent;
        margin: 0px;
    }}

    QToolButton::hover {{ /* all types of tool button */
        border: 0.5px solid rgb(228, 229, 241);
        border-radius: 5px;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 rgb(210, 210, 210), stop: 1 rgb(228, 229, 241));
    }}

    QToolButton::pressed {{ /* all types of tool button */
        border: 0.5px solid rgb(228, 229, 241);
        border-radius: 5px;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 rgb(228, 229, 241), stop: 1 rgb(250, 250, 250));
    }}

    QToolButton::checked {{ /* all types of tool button */
        border: 0.5px solid rgb(228, 229, 241);
        border-radius: 5px;
        background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 rgb(210, 210, 210), stop: 1 rgb(228, 229, 241));
    }}

    QToolButton[popupMode="1"] {{ /* only for MenuButtonPopup */
        padding-right: 10px; /* make way for the popup button */
    }}

    /* the subcontrols below are used only in the MenuButtonPopup mode */
    QToolButton::menu-button {{
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
        /* 16px width + 4px for border = 20px allocated above */
        width: 16px;
    }}

    QToolButton::menu-arrow {{
        image: url({icon});
        width: 20px;
        height: 20px;
    }}

    QToolButton::menu-arrow:open {{
        top: 1px; left: 1px; /* shift it a bit */
    }}
""".format(icon=os.path.join(ICON_PATH, "drop_down.png"))


class CLToolButton(QToolButton):

    def __init__(self,
                 parent: QWidget,
                 icon: str,
                 help: str,
                 checkable: bool = False,
                 checked: bool = False,
                 callback: Callable = None,
                 menu: QMenu = None,
                 group: QButtonGroup = None):
        super(CLToolButton, self).__init__(parent)
        self.setStyleSheet(QTOOLBUTTON_STYLE_SHEET)
        self.setIcon(QIcon(os.path.join(ICON_PATH, icon)))
        self.setIconSize(QSize(TAB_BUTTON_ICON_WIDTH, TAB_BUTTON_ICON_HEIGHT))
        self.setToolTip(help)
        self.setCheckable(checkable)
        if checkable:
            self.setChecked(checked)
        if callback:
            self.clicked.connect(callback)
        if menu:
            self.setFixedSize(TAB_BUTTON_DROPDOWN_WIDTH, TAB_BUTTON_HEIGHT)
            self.setPopupMode(QToolButton.MenuButtonPopup)
            self.setMenu(menu)
        else:
            self.setFixedSize(TAB_BUTTON_WIDTH, TAB_BUTTON_HEIGHT)
        if group:
            group.addButton(self)
