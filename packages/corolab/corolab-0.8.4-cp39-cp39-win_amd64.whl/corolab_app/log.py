# Copyright 2023-2024 Parker Owan.  All rights reserved.

import logging

from PyQt5.QtWidgets import QPlainTextEdit

LOG_LEVEL = logging.INFO  # Use INFO for prod
TEXT_EDIT_LOGGER_DEFAULT_HEIGHT = 80
TRIVIAL_LOG_STR = "%(levelname)s - %(message)s"
SIMPLE_LOG_STR = "%(asctime)s - %(levelname)s - %(message)s"
DETAILED_LOG_STR = "[%(asctime)s] %(filename)s:%(lineno)d | %(levelname)s - %(message)s"


class CLTextLoggerWidget(QPlainTextEdit):

    def __init__(self):
        super(CLTextLoggerWidget, self).__init__()
        self._handler = _CLLogHandler(widget=self)
        self.setReadOnly(True)
        self.setFixedHeight(TEXT_EDIT_LOGGER_DEFAULT_HEIGHT)
        self.setStyleSheet("""
                QPlainTextEdit {
                    font: 11px;
                    background-color: rgb(228, 229, 241);
                    color: rgb(72, 75, 106);
                }

                QScrollBar {
                    width: 0px;
                    height: 0px;
                }
            """)


class _CLLogHandler(logging.Handler):

    def __init__(self, widget: QPlainTextEdit):
        super().__init__()
        self._widget = widget
        self.setFormatter(logging.Formatter(SIMPLE_LOG_STR))
        logging.getLogger().addHandler(self)
        logging.getLogger().setLevel(LOG_LEVEL)

    def emit(self, record):
        msg = self.format(record)
        self._widget.appendPlainText(msg)
