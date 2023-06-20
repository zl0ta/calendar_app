import sys
import re

from css import style_sheet
from clndr import auth #, get_events, create_event, delete_event, update_event

from PySide6.QtCore import QLocale
from PySide6.QtGui import QFontDatabase, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QCalendarWidget, \
    QApplication, QTableWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QScrollBar


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
        event_list_layout.addWidget(event_list_label, alignment=Qt.AlignCenter)

        event_list_table = QTableWidget()
        event_list_table.setColumnCount(5)
        headers = ["✓", "Start Time", "End Time", "Title", "Group"]
        event_list_table.setHorizontalHeaderLabels(headers)
        event_list_table.setHorizontalScrollBar(QScrollBar())
        event_list_table.setVerticalScrollBar(QScrollBar())
        event_list_table.setColumnWidth(0, 10)
        event_list_table.setColumnWidth(1, 90)
        event_list_table.setColumnWidth(2, 90)
        event_list_table.setColumnWidth(3, 280)
        event_list_table.setColumnWidth(4, 100)

        event_list_layout.addWidget(event_list_table)

        main_layout.addWidget(event_list_container)
        event_list_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        management_container = QWidget()
        management_layout = QVBoxLayout(management_container)
        management_container.setContentsMargins(0, 0, 0, 0)

        calendar_container = QWidget()
        calendar_layout = QVBoxLayout(calendar_container)
        calendar_widget = QCalendarWidget()
        calendar_widget.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        calendar_widget.setFirstDayOfWeek(Qt.Monday)
        calendar_widget.setLocale(QLocale(QLocale.English))
        calendar_layout.addWidget(calendar_widget)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EventsApp()
    window.show()
    sys.exit(app.exec())