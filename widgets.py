from PyQt6.QtCore import Qt, QSize
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from PyQt6.QtWidgets import (QMainWindow,
                             QPushButton,
                             QLabel,
                             QWidget,
                             QHBoxLayout,
                             QToolButton,
                             QVBoxLayout)


class CustomTitleBar(QWidget):
    """ Custom Title Bar """

    def __init__(self, parent):
        """ Title Bar Initialization
        :param parent: Parent"""
        super().__init__(parent)
        self.initial_pos = None  # Position to drag window

        self.setStyleSheet('background-image: url("./images/top.png");'
                           'font-weight: bold;')

        # Layout
        self.title_bar_layout = QHBoxLayout(self)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar_layout.setSpacing(0)

        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_bar_layout.addWidget(self.title)

        self.init_buttons()

    def init_buttons(self) -> None:
        """ Buttons Initialization """
        # Min button
        min_button = QToolButton(self)
        min_button.clicked.connect(self.window().showMinimized)
        min_button.setStyleSheet(
            """background-image: url(./images/min_button.png);
                border: 0px;
            """)

        # Close button
        close_button = QToolButton(self)
        close_button.clicked.connect(self.window().close)
        close_button.setStyleSheet(
            """background-image: url(./images/close_button.png);
            border: 0px;
            """
        )

        buttons = [
            min_button,
            close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(28, 32))
            self.title_bar_layout.addWidget(button)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()

    def mouseReleaseEvent(self, event) -> None:
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.window().move(
                self.window().x() + delta.x(),
                self.window().y() + delta.y(),
            )
        self.initial_pos = None


class Wire(QLabel):
    """ Wire class
    Contains information about wire, output name and two states"""

    def __init__(self, parent, img_active, img_inactive, name=None):
        """ Initialization
         :param parent: Parent
         :param img_active: Filename of image of active wire
         :param img_inactive: Filename of image of inactive wire
         :param name: Optional name of output signal """
        super().__init__(parent)
        # Graphics
        self.images = [img_inactive, img_active]
        self.setStyleSheet(f'background-image: url("./images/wires/{img_inactive}");')

        # States
        self.is_active = False
        self.name = name

    def change_state(self) -> None:
        """ Turns on/off the wire """
        self.is_active = not self.is_active
        self.setStyleSheet(f'background-image: url("./images/wires/{self.images[self.is_active]}")')


class Port(QPushButton):
    """ Address port """

    def __init__(self, parent, img_inactive, img_active):
        """ Initialization of address port
        :param parent: Parent
        :param img_active: Filename of image of active port
        :param img_inactive: Filename of image of inactive port """
        super().__init__(parent)
        # Graphics
        self.images = [img_inactive, img_active]
        self.setStyleSheet(f'background-image: url("./images/{img_inactive}");'
                           f'border: 0px;')
        # States
        self.is_active = False
        self.clicked.connect(parent.change_state)

    def change_state(self) -> None:
        """ Turns on/off the button """
        self.is_active = not self.is_active
        self.setStyleSheet(f'background-image: url("./images/{self.images[self.is_active]}");'
                           f'border: 0px;')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Custom Title init
        self.title_bar = CustomTitleBar(self)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-image: url(./images/background.png)")

        # Layout
        central_widget_layout = QVBoxLayout()
        central_widget_layout.setContentsMargins(0, 0, 0, 0)
        central_widget_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        central_widget_layout.addWidget(self.title_bar)
        central_widget.setLayout(central_widget_layout)

        # Fields
        self.output_wires = []
        self.address_wires = []
        self.ports = []
        self.output_label = None

        self.init_wires()
        self.init_labels()
        self.init_ports()

    def init_wires(self) -> None:
        """ Initialization of wire classes """
        wire_a = Wire(self, "A.png", "not_A.png")
        wire_a.setGeometry(355, 144, 170, 491)
        wire_b = Wire(self, "B.png", "not_B.png")
        wire_b.setGeometry(416, 154, 108, 481)
        wire_c = Wire(self, "C.png", "not_C.png")
        wire_c.setGeometry(478, 163, 46, 472)
        self.address_wires = [wire_a, wire_b, wire_c]

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

    def init_labels(self) -> None:
        """ Initialization of labels """
        for i in range(8):
            label = QLabel(f"I{i}", self)
            label.setGeometry(300, 120 + (i * 52), 30, 30)
            label.setStyleSheet("font-weight: bold;"
                                "font-size: 20px;")
        self.output_label = QLabel("I0", self)
        self.output_label.setStyleSheet("font-weight: bold;"
                                        "font-size: 16px;")
        self.output_label.setGeometry(760, 300, 30, 30)

    def init_ports(self) -> None:
        """ Initialization of ports """
        for i in range(3):
            button = Port(self, 'button_0.png', 'button_1.png')
            button.setGeometry(347 + (i * 62), 630, 25, 25)
            self.ports.append(button)

    def change_state(self) -> None:
        """ Change all states and refresh the image of schem """
        # Reset last output wire
        a, b, c = map(int, [port.is_active for port in self.ports])
        self.output_wires[a][b][c].change_state()  # MDNF: !a!b!ci0 V !a!bci1 V !ab!ci2 V !abci3 V a!b!ci4 V
        # a!bci5 V ab!ci6 V abci7

        # Change address buttons and wires
        self.address_wires[self.ports.index(self.sender())].change_state()
        self.sender().change_state()

        # Change output wires and output label
        a, b, c = map(int, [port.is_active for port in self.ports])
        self.output_wires[a][b][c].change_state()
        self.output_label.setText(self.output_wires[a][b][c].name)
