# Copyright 2023-2024 Parker Owan.  All rights reserved.

import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QHeaderView

import corolab

from corolab_app.container import CLProjectContainer
from corolab_app.editor.item import createWidgetsFromProperties

PROPERTY_TABLE_MIN_SECTION_WIDTH = 65


class CLPropertyTable(QTableWidget):

    def __init__(self, container: CLProjectContainer):
        super(CLPropertyTable, self).__init__()
        self._container = container
        self.setStyleSheet("""
            QWidget {
                font: 12px;
                color: rgb(42, 44, 46);
            }

            QHeaderView::section {
                padding: 5px;                               
                height: 12px;                                
                border: none;
                background-color: rgb(219, 220, 232);
                font: bold 11px;
                color: rgb(42, 44, 46);
                border-top: 1px solid rgb(250, 250, 250);
                border-bottom: 1px solid rgb(250, 250, 250);
                border-right: none;
                border-left: 2px solid rgb(250, 250, 250);
            }

            QTableWidget {
                selection-background-color: rgb(228, 229, 241);
                gridline-color: rgb(250, 250, 250);
                font-size: 12pt;
                color: rgb(42, 44, 46);
            }

            QLineEdit {
                border: 1px solid rgb(210, 211, 219);
                background: rgb(250, 250, 250);
                height: 24px;
            }

            QSpinBox {
                border: 1px solid rgb(210, 211, 219);
                background: rgb(250, 250, 250);
                height: 24px;
            }

            QSpinBox::up-arrow {
                border : 1px solid rgb(210, 211, 219);
                background : rgb(250, 250, 250);
            }

            QSpinBox::down-arrow {
                border : 1px solid rgb(210, 211, 219);
                background : rgb(250, 250, 250);
            }

            QDoubleSpinBox {
                border: 1px solid rgb(210, 211, 219);
                background: rgb(250, 250, 250);
                height: 24px;
            }

            QDoubleSpinBox::up-arrow {
                border : 1px solid rgb(210, 211, 219);
                background : rgb(250, 250, 250);
            }

            QDoubleSpinBox::down-arrow {
                border : 1px solid rgb(210, 211, 219);
                background : rgb(250, 250, 250);
            }

            QSlider::groove:horizontal {
                border: none;
                height: 8px; /* the groove expands to the size of the slider by default. by giving it a height, it has a fixed size */
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #8bb6d9, stop:1 #add6f7);
                margin: 2px 0;
            }

            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                border: 1px solid rgb(147, 148, 165);
                width: 12px;
                margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */
                border-radius: 3px;
            }
        """)
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels(["Properties"])
        self.verticalHeader().setVisible(False)
        self.setFocusPolicy(Qt.NoFocus)
        header = self.horizontalHeader()
        header.setMinimumSectionSize(PROPERTY_TABLE_MIN_SECTION_WIDTH)
        header.setSectionResizeMode(0, QHeaderView.Stretch)

    def reset(self):
        self.setRowCount(0)

    def populate(self, item: corolab.WithProperties):
        if not item:
            return
        logging.debug("Properties for '{}'".format(item.name()))
        widgets = createWidgetsFromProperties(table=self,
                                              container=self._container,
                                              item=item,
                                              name=item.name(),
                                              ptype=item.type())

        self.setVisible(False)
        self.reset()
        self.setRowCount(len(widgets))
        for i, widget in enumerate(widgets):
            self.setCellWidget(i, 0, widget)
        self.resizeRowsToContents()
        self.setVisible(True)
