import sys
import re

from css import style_sheet
from clndr import *
from app_functions import *

from PySide6.QtCore import QLocale
from PySide6.QtGui import QFontDatabase, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QCalendarWidget, \
    QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QScrollBar, QTableWidgetItem, QCheckBox, QGroupBox, QTimeEdit, \
    QComboBox, QTextEdit

from data_storage import get_groups


class EventRow(QWidget):
    def __init__(self, date):
        super().__init__()

        layout = QHBoxLayout(self)

        self.date = date

        self.check = QCheckBox()
        layout.addWidget(self.check)

        self.start = QTimeEdit()
        layout.addWidget(self.start)

        self.end = QTimeEdit()
        layout.addWidget(self.end)

        self.title = QTextEdit()
        layout.addWidget(self.title)

        #choose group from list
        self.group = QComboBox()
        # self.group.addItems([group.summary for group in get_groups()]
        self.group.addItems(["Group 1", "Group 2", "Group 3"])
        layout.addWidget(self.group)

        self.setFixedHeight(26)
        self.check.setFixedWidth(30)
        self.start.setFixedWidth(80)
        self.end.setFixedWidth(80)
        self.title.setFixedWidth(300)
        self.group.setFixedWidth(80)
        layout.setContentsMargins(0, 0, 0, 0)


class Header(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        self.check_label = QLabel("✔")
        layout.addWidget(self.check_label)

        self.start_label = QLabel("Start Time")
        layout.addWidget(self.start_label)

        self.end_label = QLabel("End Time")
        layout.addWidget(self.end_label)

        self.title_label = QLabel("Title")
        layout.addWidget(self.title_label)

        self.group_label = QLabel("Group")
        layout.addWidget(self.group_label)

        self.setFixedHeight(30)
        self.check_label.setFixedWidth(30)
        self.start_label.setFixedWidth(80)
        self.end_label.setFixedWidth(80)
        self.title_label.setFixedWidth(300)
        self.group_label.setFixedWidth(80)


class EventsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self._create_ui()
        self.apply_style()
        self.resize(1000, 600)
        self.setWindowTitle("Events calendar app")

    def _create_ui(self):
        main_container = QWidget(self)
        main_container.setMinimumWidth(800)
        self.setCentralWidget(main_container)
        main_container.setContentsMargins(0, 0, 0, 0)

        main_layout = QHBoxLayout(main_container)

        event_list_container = QWidget()
        event_list_layout = QVBoxLayout(event_list_container)
        event_list_container.setContentsMargins(0, 0, 0, 0)

        event_list_label = QLabel("Events")
        event_list_label.setFixedHeight(15)
        event_list_layout.addWidget(event_list_label,
                                    alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        event_list_header = Header()
        event_list_header.setFixedHeight(30)
        event_list_layout.addWidget(event_list_header,
                                    alignment=Qt.AlignmentFlag.AlignTop)

        event_list_groupbox = QGroupBox()
        event_list_groupbox.setFixedHeight(int(event_list_container.width() * 0.85))
        self.event_list_groupbox_layout = QVBoxLayout(event_list_groupbox)
        self.event_list_groupbox_layout.setContentsMargins(0, 0, 0, 0)
        self.event_list_groupbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # for i in range(10):
        #     self.event_list_groupbox_layout.addWidget(EventRow())

        event_list_layout.addWidget(event_list_groupbox)

        event_list_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        main_layout.addWidget(event_list_container)

        management_container = QWidget()
        management_layout = QVBoxLayout(management_container)
        management_container.setContentsMargins(0, 0, 0, 0)

        calendar_container = QWidget()
        calendar_layout = QVBoxLayout(calendar_container)
        self.calendar_widget = QCalendarWidget()
        self.calendar_widget.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar_widget.setFirstDayOfWeek(Qt.Monday)
        self.calendar_widget.setLocale(QLocale(QLocale.English))
        self.calendar_widget.clicked.connect(self.add_event1)

        calendar_layout.addWidget(self.calendar_widget)

        operations_container = QWidget()
        operations_layout = QVBoxLayout(operations_container)
        export_unsync_button = QPushButton("Export all events to Google Calendar")
        import_events_button = QPushButton("Import all events from Google Calendar")
        delete_events_button = QPushButton("Delete chosen events")
        operations_layout.addWidget(export_unsync_button)
        operations_layout.addWidget(import_events_button)
        operations_layout.addWidget(delete_events_button)

        management_layout.addWidget(calendar_container)
        management_layout.addWidget(operations_container)

        main_layout.addWidget(management_container)
        management_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        management_container.setFixedWidth(int(main_container.width() * 0.45))

        main_container.setLayout(main_layout)

    def apply_style(self):
        # Load Google font
        font_id = QFontDatabase.addApplicationFont("google-sans-cufonfonts/ProductSans-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font_size = 11
        font = QFontDatabase.systemFont(QFontDatabase.GeneralFont)
        font.setFamily(font_family)
        font.setPointSize(font_size)
        self.setFont(font)

        # Apply styles using CSS
        self.setStyleSheet(style_sheet)

    # choose date from calendar and add event to table
    def add_event(self):
        pass

    # delete chosen event from table
    def delete_event(self):
        pass

    # export added event to google calendar
    def export_event(self):
        pass

    # import events from google calendar
    def import_event(self):
        pass

    def add_event1(self, date):
        event_row1 = EventRow(date)
        event_row2 = EventRow(date)

        self.event_list_groupbox_layout.addWidget(event_row1)
        self.event_list_groupbox_layout.addWidget(event_row2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EventsApp()
    window.show()
    sys.exit(app.exec())
