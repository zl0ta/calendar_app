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
            
            QPushButton:hover {
                background-color: #0d47a1;
            }
            
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            
            QPushButton:disabled {
                background-color: #e8eaed;
                color: #a5a7aa;
            }

            QCheckBox {
                color: #202124;
            }

            QTimeEdit {
                background-color: #fff;
                border: 1px solid #ccc;
                color: #202124;
                padding: 2px;
            }

            QTextEdit {
                background-color: #fff;
                border: 1px solid #ccc;
                color: #202124;
                padding: 2px;
            }

            QComboBox {
                background-color: #fff;
                border: 1px solid #ccc;
                color: #202124;
                padding: 2px;
                padding-right: 20px;
                selection-background-color: #e8f0fe;
                selection-color: #4285f4;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border: none;
                background-color: transparent;
            }

            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }

            QCalendarWidget {
                background-color: #fff;
                selection-background-color: #fbbc05;
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
