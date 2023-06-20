style_sheet = """
            QLabel {
                color: #202124;
                font-size: 14px;
                font-weight: bold;
            }

            QPushButton {
                background-color: #1a73e8;
                color: #fff;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }

            QCalendarWidget QAbstractItemView:enabled {
                color: #202124;
                selection-background-color: #1a73e8;
                selection-color: #fff;
            }

            QTableWidget {
                background-color: #fff;
                border: 1px solid #ccc;
                selection-background-color: #1a73e8;
                selection-color: #fff;
            }

            QHeaderView::section {
                background-color: #f2f2f2;
                color: #202124;
                font-size: 14px;
                font-weight: bold;
                padding: 6px;
                border: none;
                border-right: 1px solid #ccc;
            }

            QScrollBar {
                background-color: #f2f2f2;
                width: 12px;
            }

            QScrollBar::handle {
                background-color: #ccc;
                border-radius: 6px;
            }

            QScrollBar::handle:hover {
                background-color: #bbb;
            }

            QScrollBar::sub-page,
            QScrollBar::add-page {
                background-color: #f2f2f2;
            }

            QScrollBar::sub-line,
            QScrollBar::add-line {
                background-color: transparent;
            }
        """