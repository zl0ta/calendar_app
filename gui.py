import sys
from functools import partial

from css import style_sheet
from clndr import gc_get_service, gc_upload_event, gc_create_event, gc_get_events, gc_delete_event
from db_functions import db_connect, db_load_groups, db_get_events_for_date, db_load_event, db_delete_event

from PySide6.QtCore import QLocale, QTime, QDate
from PySide6.QtGui import QFontDatabase, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QCalendarWidget, \
    QApplication, QHBoxLayout, QVBoxLayout, QSizePolicy, QCheckBox, QGroupBox, QTimeEdit, \
    QComboBox, QTextEdit, QMessageBox


class Event(QWidget):
    def __init__(self, date, app):
        super().__init__()

        layout = QHBoxLayout(self)

        self.check_box = QCheckBox()
        layout.addWidget(self.check_box)

        self.start = QTimeEdit()
        layout.addWidget(self.start)

        self.end = QTimeEdit()
        layout.addWidget(self.end)

        self.title = QTextEdit()
        self.title.setFixedHeight(30)
        self.title.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.title)

        # choose group from list
        self.group = QComboBox()
        self.group.addItems(app.group_titles)
        layout.addWidget(self.group)

        self.idGCAL = None
        self.date = date
        self.start_time = self.start.time().currentTime()
        self.end_time = self.end.time().currentTime()
        self.title_data = self.title.toPlainText()
        self.group_data = self.group.currentText()

        self.add_event_button = QPushButton("+")
        self.add_event_button.setContentsMargins(0, 0, 0, 0)
        self.add_event_button.clicked.connect(partial(self.add_event_to_gc_db, app))
        layout.addWidget(self.add_event_button)

        self.setFixedHeight(28)
        self.check_box.setFixedWidth(30)
        self.start.setFixedWidth(80)
        self.end.setFixedWidth(80)
        self.group.setFixedWidth(80)
        self.add_event_button.setFixedWidth(40)
        layout.setContentsMargins(0, 0, 0, 0)

    def add_data(self, event):
        self.add_event_button.setDisabled(True)

        if event.idGCAL is not None:
            self.idGCAL = event.idGCAL
        self.date = event.date
        start_time = QTime.fromString(event.start_time.strftime("%H:%M:%S"))
        end_time = QTime.fromString(event.end_time.strftime("%H:%M:%S"))
        self.start.setTime(start_time)
        self.end.setTime(end_time)
        self.title.setText(event.title)
        self.group.setCurrentText(event.group)

        return self

    def add_event_to_gc_db(self, app):
        self.add_event_button.setDisabled(True)
        app.add_event_template(self.date)

        date = self.date
        start_time = self.start.time()
        end_time = self.end.time()
        title = self.title.toPlainText()
        group = self.group.currentText()

        # check input data
        if title == "":
            alert = QMessageBox(QMessageBox.Icon.Critical, "Error",
                                "Title cannot be empty", QMessageBox.StandardButton.Ok)
            alert.exec()
            return
        if start_time > end_time:
            alert = QMessageBox(QMessageBox.Icon.Critical, "Error",
                                "End time must not be earlier than start time", QMessageBox.StandardButton.Ok)
            alert.exec()
            return

        # upload to google calendar and save to database
        event_idGCAL = gc_upload_event(app.gc_service, gc_create_event(date, start_time, end_time, title), group)
        self.idGCAL = event_idGCAL
        db_load_event(event_idGCAL, app.db_session, date, start_time, end_time, title, group)


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
        self.db_session = db_connect()
        self.gc_service = gc_get_service()
        self.event_list_groupbox_layout = None
        self._create_ui()
        self.apply_style()
        self.resize(1000, 600)
        self.setWindowTitle("Events calendar app")
        self.group_titles = None
        db_load_groups(self)

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
        # monday as first day of week
        self.calendar_widget.setFirstDayOfWeek(Qt.DayOfWeek.Monday)
        # set locale to english
        self.calendar_widget.setLocale(QLocale(QLocale.English))
        # set current date
        self.calendar_widget.setSelectedDate(QDate.currentDate())
        self.calendar_widget.clicked.connect(partial(self.show_events_for_date))
        calendar_layout.addWidget(self.calendar_widget)

        operations_container = QWidget()
        operations_layout = QVBoxLayout(operations_container)

        import_events_button = QPushButton("Import all events from Google Calendar")

        delete_events_button = QPushButton("Delete chosen events")
        delete_events_button.clicked.connect(partial(self.delete_chosen_events))

        edit_event_button = QPushButton("Edit chosen event")
        edit_event_button.clicked.connect(partial(self.edit_chosen_event))

        operations_layout.addWidget(import_events_button)
        operations_layout.addWidget(delete_events_button)
        operations_layout.addWidget(edit_event_button)

        management_layout.addWidget(calendar_container)
        management_layout.addWidget(operations_container)

        main_layout.addWidget(management_container)
        management_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
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

    def add_event_template(self, date):
        template = Event(date, self)
        self.event_list_groupbox_layout.addWidget(template)

    def show_events_for_date(self, date):
        # Clear event list
        for i in reversed(range(self.event_list_groupbox_layout.count())):
            self.event_list_groupbox_layout.itemAt(i).widget().setParent(None)

        events = db_get_events_for_date(self, date)
        for event in events:
            event = Event(date, self).add_data(event)
            self.event_list_groupbox_layout.addWidget(event)
        self.add_event_template(date)

    def delete_chosen_events(self):
        for i in reversed(range(self.event_list_groupbox_layout.count())):
            event = self.event_list_groupbox_layout.itemAt(i).widget()
            if event.check_box.isChecked():
                db_delete_event(self, event.idGCAL)
                gc_delete_event(self, event)
                event.setParent(None)

    def edit_chosen_event(self):
        chosen_events = []
        chosen_event = None
        for i in reversed(range(self.event_list_groupbox_layout.count())):
            event = self.event_list_groupbox_layout.itemAt(i).widget()
            if event.check_box.isChecked():
                chosen_events.append(event)

        if len(chosen_events) > 1:
            alert = QMessageBox()
            alert.setText("You can edit only one event at a time")
            alert.exec()
        elif len(chosen_events) == 0:
            alert = QMessageBox()
            alert.setText("You have to choose an event to edit")
            alert.exec()
        else:
            chosen_event = chosen_events[0]

        db_delete_event(self, chosen_event.idGCAL)

    # def get_events_from_gc(self, service):
    #    imported_events = gc_get_events(service)
    #    db_load_events(self, imported_events)

    # close event
    def closeEvent(self, event):
        self.db_session.close()
        self.gc_service.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EventsApp()
    window.show()
    sys.exit(app.exec())
