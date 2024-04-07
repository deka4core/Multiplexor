from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (QMainWindow,
                             QPushButton,
                             QLabel,
                             QWidget,
                             QHBoxLayout,
                             QToolButton,
                             QVBoxLayout )
from constants import WINDOW_HEIGHT, WINDOW_WIDTH


class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('background-image: url("./images/top.png");'
                           'font-weight: bold;')
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)
        title_bar_layout.setSpacing(0)

        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_bar_layout.addWidget(self.title)

        # Min button
        self.min_button = QToolButton(self)
        self.min_button.clicked.connect(self.window().showMinimized)
        self.min_button.setStyleSheet(
            """background-image: url(./images/min_button.png);
                border: 0px;
            """)

        # Close button
        self.close_button = QToolButton(self)
        self.close_button.clicked.connect(self.window().close)
        self.close_button.setStyleSheet(
            """background-image: url(./images/close_button.png);
            border: 0px;
            """
        )

        buttons = [
            self.min_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(28, 32))
            title_bar_layout.addWidget(button)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()

    def mouseReleaseEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()


class Wire(QLabel):
    def __init__(self, parent, img_active, img_inactive, name=None):
        super().__init__(parent)
        self.images = [img_inactive, img_active]
        self.setStyleSheet(f'background-image: url("./images/wires/{img_inactive}");')
        self.is_active = False
        self.name = name

    def change_state(self):
        self.is_active = not self.is_active
        self.setStyleSheet(f'background-image: url("./images/wires/{self.images[self.is_active]}")')

    def reset(self):
        self.setStyleSheet(f'background-image: url("./images/wires/{self.images[0]}");')
        self.is_active = False


class Port(QPushButton):
    def __init__(self, parent, img_inactive, img_active):
        super().__init__(parent)
        self.images = [img_inactive, img_active]
        self.clicked.connect(parent.change_state)
        self.setStyleSheet(f'background-image: url("./images/{img_inactive}");'
                           f'border: 0px;')
        self.is_active = False

    def change_state(self):
        self.is_active = not self.is_active
        self.setStyleSheet(f'background-image: url("./images/{self.images[self.is_active]}");'
                           f'border: 0px;')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        central_widget = QWidget()
        self.title_bar = CustomTitleBar(self)

        centra_widget_layout = QVBoxLayout()
        centra_widget_layout.setContentsMargins(0, 0, 0, 0)
        centra_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        centra_widget_layout.addWidget(self.title_bar)
        central_widget.setLayout(centra_widget_layout)
        self.setCentralWidget(central_widget)

        central_widget.setStyleSheet("background-image: url(./images/background.png)")

        for i in range(8):
            label = QLabel(f"I{i}", self)
            label.setGeometry(300, 120 + (i * 52), 30, 30)
            label.setStyleSheet("font-weight: bold;"
                                "font-size: 20px;")

        wire_a = Wire(self, "A.png", "not_A.png")
        wire_a.setGeometry(355, 144, 170, 491)
        wire_b = Wire(self, "B.png", "not_B.png")
        wire_b.setGeometry(416, 154, 108, 481)
        wire_c = Wire(self, "C.png", "not_C.png")
        wire_c.setGeometry(478, 163, 46, 472)
        self.wires = [wire_a, wire_b, wire_c]

        wire_i1 = Wire(self, "I1_active.png", "I1_inactive.png", name="I0")
        wire_i1.setGeometry(579, 150, 95, 160)
        wire_i1.change_state()
        wire_i2 = Wire(self, "I2_active.png", "I2_inactive.png", name="I1")
        wire_i2.setGeometry(579, 202, 97, 115)
        wire_i3 = Wire(self, "I3_active.png", "I3_inactive.png", name="I2")
        wire_i3.setGeometry(579, 254, 99, 69)

        wire_i4 = Wire(self, "I4_active.png", "I4_inactive.png", name="I3")
        wire_i4.setGeometry(579, 306, 99, 24)
        wire_i5 = Wire(self, "I5_active.png", "I5_inactive.png", name="I4")
        wire_i5.setGeometry(579, 336, 100, 23)
        wire_i6 = Wire(self, "I6_active.png", "I6_inactive.png", name="I5")
        wire_i6.setGeometry(579, 343, 99, 70)
        wire_i7 = Wire(self, "I7_active.png", "I7_inactive.png", name="I6")
        wire_i7.setGeometry(579, 350, 98, 115)
        wire_i8 = Wire(self, "I8_active.png", "I8_inactive.png", name="I7")
        wire_i8.setGeometry(579, 358, 95, 160)
        self.output_wires = [[[wire_i1, wire_i2], [wire_i3, wire_i4]],
                             [[wire_i5, wire_i6], [wire_i7, wire_i8]]]

        self.ports = []
        for i in range(3):
            button = Port(self, 'button_0.png', 'button_1.png')
            button.setGeometry(347 + (i * 62), 630, 25, 25)
            self.ports.append(button)

        self.output_label = QLabel("I0", self)
        self.output_label.setStyleSheet("font-weight: bold;"
                                        "font-size: 16px;")
        self.output_label.setGeometry(760, 300, 30, 30)

    def change_state(self):
        # Reset last output wire
        a, b, c = map(int, [port.is_active for port in self.ports])
        self.output_wires[a][b][c].change_state()

        self.wires[self.ports.index(self.sender())].change_state()
        self.sender().change_state()

        a, b, c = map(int, [port.is_active for port in self.ports])
        self.output_wires[a][b][c].change_state()
        self.output_label.setText(self.output_wires[a][b][c].name)



