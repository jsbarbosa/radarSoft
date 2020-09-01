__version__: str = 'v0.1'

FIND_SERIAL_TIMEOUT: int = 1000
UPDATE_DATA_TIMEOUT: int = 25

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
    }
]