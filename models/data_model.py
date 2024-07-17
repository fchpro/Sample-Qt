from PySide6.QtCore import QObject, Signal
from settings import settings
from global_signals import global_signals
from logger_config import log_args_kwargs as print

class ModelSignals(QObject):
    updated = Signal()
    data_changed = Signal(str, object)


class DataModel():
    signals = ModelSignals()

    def __init__(self):
        super().__init__()

        self._data = None
        global_signals.print_current_data_model.connect(self.print_current_data_model)


        self.reset()

    def reset(self):
        print("d1G1b", "reset")

    def print_current_data_model(self):
        print("H1slS", self._data)

model = DataModel()

