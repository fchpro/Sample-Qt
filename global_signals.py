from PySide6.QtCore import QObject, Signal

class Signals(QObject):
    progress = Signal(int)
    image_completed = Signal()
    completed_images = Signal(int)
    debug_mode = Signal(bool)
    print_settings = Signal()
    notify = Signal(dict)
    print_current_data_model = Signal()


global_signals = Signals()
