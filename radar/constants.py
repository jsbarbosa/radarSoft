import radar.connection.constants as constants

__version__: str = 'v0.1'

FIND_SERIAL_TIMEOUT: int = 1000
UPDATE_DATA_TIMEOUT: int = 1

SHOW_LAST_NDOTS: int = 45

OPTIONS_WIDGETS: list = [
    {
        'label': 'Radar origin (°)',
        'name': 'origin_spin_box',
        'widget': 'QSpinBox()',
        'connect': 'valueChanged.connect',
        'function': "rotate_plot",
        'properties': {
            'setMinimum': 0,
            'setMaximum': 360,
        }
    },
    {
        'label': 'Point trace',
        'name': 'point_trace_spin_box',
        'widget': 'QSpinBox()',
        'connect': 'valueChanged.connect',
        'function': "update_point_trace",
        'properties': {
            'setMinimum': 1,
            'setMaximum': 1e3,
            'setValue': SHOW_LAST_NDOTS
        }
    },
    {
        'label': 'Min shooting range',
        'name': 'min_shooting_range_spin_box',
        'widget': 'QSpinBox()',
        'connect': 'valueChanged.connect',
        'function': "update_shooting_range",
        'properties': {
            'setMinimum': 0,
            'setMaximum': constants.MAX_DISTANCE,
            'setValue': 50
        }
    },
    {
        'label': 'Max shooting range',
        'name': 'max_shooting_range_spin_box',
        'widget': 'QSpinBox()',
        'connect': 'valueChanged.connect',
        'function': "update_shooting_range",
        'properties': {
            'setMinimum': 0,
            'setMaximum': constants.MAX_DISTANCE,
            'setValue': 150
        }
    },
    {
        'label': '',
        'name': 'stop_start_pushbutton',
        'widget': 'QPushButton("Start/Stop")',
        'connect': 'clicked.connect',
        'function': "stop_start",
        'properties': {}
    },
    {
        'label': '',
        'name': 'shoot_pushbutton',
        'widget': 'QPushButton("Shoot")',
        'connect': 'clicked.connect',
        'function': "shoot",
        'properties': {}
    },
    {
        'label': '',
        'name': 'stop_shooting_pushbutton',
        'widget': 'QPushButton("Stop Shooting")',
        'connect': 'clicked.connect',
        'function': "stop_shooting",
        'properties': {}
    }
]
