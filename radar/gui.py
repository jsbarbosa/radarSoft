import logging
import sys

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QStatusBar, QHBoxLayout, QFrame, \
    QSpinBox, QGroupBox, QGridLayout, QLabel

import radar.constants as constants
from radar.connection.core import find_devices, RadarSerial
from radar.plots import RadarCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(f"Radar {constants.__version__}")

        central_widget = QWidget()
        self._main_layout = QHBoxLayout()
        central_widget.setLayout(self._main_layout)
        self.setCentralWidget(central_widget)

        self._radar_canvas = RadarCanvas()
        self._main_layout.addWidget(self._radar_canvas)

        self._radar_serial: RadarSerial = None

        self._find_serial_timer = QTimer()
        self._find_serial_timer.timeout.connect(self.find_connect)
        self.start_find_serial_timer()

        self._update_data_timer = QTimer()
        self._update_data_timer.timeout.connect(self.update_data)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self._options_frame = QFrame()
        self._options_frame.setLayout(QVBoxLayout())

        self._options_frame_groupbox = QGroupBox('Options')
        self._options_frame_groupbox.setLayout(QGridLayout())

        self._main_layout.addWidget(self._options_frame)
        self._options_frame.layout().addWidget(self._options_frame_groupbox)

        self.populate_options_frame_widgets()

    def populate_options_frame_widgets(self):
        layout = self._options_frame_groupbox.layout()
        for i, info in enumerate(constants.OPTIONS_WIDGETS):
            layout.addWidget(
                QLabel(info['label']),
                i, 0
            )
            widget = eval(info['widget'])
            setattr(self, info['name'], widget)

            eval(f"widget.{info['connect']}(self.{info['function']})")

            for prop, value in info['properties'].items():
                exec(f"self.{info['name']}.{prop}({value})")

            layout.addWidget(
                widget,
                i, 1
            )

    def start_find_serial_timer(self):
        self._find_serial_timer.start(constants.FIND_SERIAL_TIMEOUT)

    def start_update_timer(self):
        self._update_data_timer.start(constants.UPDATE_DATA_TIMEOUT)

    @staticmethod
    def find_devices():
        logging.info('find_devices has been called')
        devices = find_devices()
        if len(devices):
            return devices[0]

    def set_serial(self, device: str):
        logging.info('set_serial has been called')
        self._radar_serial = RadarSerial(device)
        self._find_serial_timer.stop()
        self.start_update_timer()

    def find_connect(self):
        device = self.find_devices()
        if device is not None:
            self.set_serial(device)

    def update_data(self):
        logging.info('update_data has been called')
        angle, distance = self._radar_serial.read_angle_distance()
        self._radar_canvas.append_data(angle, distance)
        self.status_bar.showMessage(f"{angle}°, {distance} cm", 1e3)

    def rotate_plot(self):
        logging.info('rotate_plot has been called')
        self._radar_canvas.rotate_plot(
            self.origin_spin_box.value()
        )

    def resizeEvent(self, event):
        logging.info('resizeEvent has been called')
        self._radar_canvas.rotate_plot(
            self.origin_spin_box.value()
        )
        super(MainWindow, self).resizeEvent(event)


def dark_paletter():
    palette = QPalette()
    palette.setColor(QPalette.Window, Qt.black)
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, Qt.black)
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    return palette


def run():
    app = QApplication(sys.argv)
    app.setPalette(dark_paletter())
    mainwindow = MainWindow()
    mainwindow.show()
    return app.exec_()
