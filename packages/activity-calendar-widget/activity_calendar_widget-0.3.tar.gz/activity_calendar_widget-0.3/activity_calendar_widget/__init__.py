from .commons import *


class ActivityCalendarWidget(QFrame):
    def __init__(
        self,
        title: str = "Activity",
        title_font: Font = None,
        toggle_font: Font = None,
        default_activities: dict = None,
        default_month: datetime = None,
        month_font: Font = None,
        day_button_font: Font = None,
        border_radius: int = 15,
        divider_color: str = "#d9dada",
        day_letter_color: str = "#a4a6ae",
        day_button_event_color: str = "#c8dbff",
        #
        parent: QWidget = None,
    ):
        super().__init__(parent)

        self.activities = default_activities or {}
        self.current_month = default_month or datetime.now()

        assert isinstance(self.current_month, datetime)

        # setting up widgets

        lay = QVBoxLayout(self)
        m = 20
        lay.setContentsMargins(m, m, m, m)

        # lay.addWidget(self.base)

        top_lay = QHBoxLayout()
        lay.addLayout(top_lay)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("title_label")
        top_lay.addWidget(self.title_label)

        top_lay.addStretch()

        self.prev_button = QPushButton("<")
        self.prev_button.clicked.connect(self.toggle_prev_month)
        top_lay.addWidget(self.prev_button)

        self.month_label = QLabel()
        self.month_label.setObjectName("month_label")
        top_lay.addWidget(self.month_label)

        self.next_button = QPushButton(">")
        self.next_button.clicked.connect(self.toggle_next_month)
        top_lay.addWidget(self.next_button)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.Shape.HLine)
        # divider.setMaximumHeight(1)
        lay.addWidget(divider)

        # for loop to set the day buttons

        days_letters_lay = QHBoxLayout()
        days_letters_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        days_letters_lay.setSpacing(10)
        lay.addLayout(days_letters_lay)

        for day_letter in DAYS_LETTERS:
            label = DayLetter(day_letter)
            days_letters_lay.addWidget(label)

        self.days_numbers: list[DayButton] = []

        for row in range(6):
            days_numbers_lay = QHBoxLayout()
            days_numbers_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            days_numbers_lay.setSpacing(10)
            lay.addLayout(days_numbers_lay)

            for col in range(len(DAYS_LETTERS)):
                button = DayButton(row, col)
                days_numbers_lay.addWidget(button)
                self.days_numbers.append(button)

        # setting the QSS
        border_radius = f"border-radius: {border_radius}px;" if border_radius else ""
        divider_color = f"color: {divider_color};" if divider_color else ""

        if not title_font:
            title_font = Font(
                color="#565656",
                font_size=20,
                font_weight="bold",
            )
        assert isinstance(title_font, Font)

        if not toggle_font:
            toggle_font = Font(
                color="#565656",
                font_size=15,
                font_weight="bold",
            )
        assert isinstance(toggle_font, Font)

        if not month_font:
            month_font = Font(
                color="black",
                font_size=22,
                font_weight="bold",
            )
        assert isinstance(month_font, Font)

        if not day_button_font:
            day_button_font = Font(
                color="#2c65f9",
                font_size=22,
                font_weight="bold",
            )
        assert isinstance(day_button_font, Font)

        toggle_button_size = toggle_font.font_size * 2

        for button in (self.prev_button, self.next_button):
            button.setObjectName("toggle_button")
            s = toggle_button_size
            button.setFixedSize(s, s)

        self.setStyleSheet(
            f"""
            ActivityCalendarWidget {{
                background: white;
                {border_radius}
            }}

            QFrame#divider {{
                {divider_color}
                max-height: 8px;
            }}
            QLabel#title_label {{
                {title_font}
            }}
            QLabel#month_label {{
                {month_font}
            }}

            QPushButton#toggle_button {{
                border-radius: {toggle_button_size/2}px;
                {toggle_font}
                background: transparent;
            }}
            QPushButton#toggle_button:hover {{
                background: #d9dce3;
                color: white;
            }}
            QPushButton#toggle_button:pressed {{
                background: #565656;
                color: white;
            }}

            DayLetter {{
                color: {day_letter_color};
                font-size: 15px;
                font-weight: bold;
            }}

            DayButton {{
                border-radius: {toggle_button_size/2}px;
                {day_button_font}
            }}
            DayButton#day_number_event, DayButton#day_number {{
                background: transparent;
            }}
            DayButton#day_number_event:hover, DayButton#day_number:hover {{
                background: #d9dce3;
                color: white;
            }}
            DayButton#day_number_event:pressed, DayButton#day_number:pressed {{
                background: #565656;
                color: white;
            }}

            DayButton#day_number_event {{
                border-radius: {toggle_button_size/2}px;
                {toggle_font}
                background: {day_button_event_color};
            }}

            DayButton#no_day {{
                background: transparent
            }}
            DayButton#no_day:hover {{
                background: transparent
            }}
            DayButton#no_day:pressed {{
                background: transparent
            }}

            """
        )

        self.set_month(self.current_month)

    def set_month(self, month: datetime):
        self.current_month = month
        self.month_label.setText(self.current_month.strftime("%b %Y").upper())

        days: list[datetime] = []

        for _day in range(1, 29):
            day_ = datetime(month.year, month.month, _day)
            days.append(day_)

        day_28: datetime = days[-1]

        for _day in range(1, 4):
            day_ = day_28 + timedelta(days=_day)
            if day_.month == month.month:
                days.append(day_)
            else:
                break

        day_1 = (days[0].weekday() + 1) % 7

        for _ in range(day_1):
            days.insert(0, 0)
        for _ in range(len(days), len(self.days_numbers)):
            days.append(0)

        m = self.current_month.strftime("%m-%Y")
        month_activities: dict = self.activities.get(m)

        for day, day_button in zip(days, self.days_numbers):
            if day:
                event = ""
                if month_activities:
                    event = month_activities.get(day.day)
                day_button.set_day(day, event)
            else:
                day_button.set_empty()

        self.setStyleSheet(self.styleSheet())

    def toggle_prev_month(self):
        month = datetime(self.current_month.year, self.current_month.month, 1)
        self.set_month(month - timedelta(days=1))

    def toggle_next_month(self):
        month = datetime(self.current_month.year, self.current_month.month, 1)
        self.set_month(month + timedelta(days=31))
