from logger_config import log_args_kwargs as print
from PySide6.QtCore import QSettings
import json
import os
from typing import Any
from paths import Paths
from constants import *
from global_signals import global_signals


class Settings:
    def __init__(self):
        self.settings = QSettings("fivers_apps", "magnets")
        global_signals.print_settings.connect(self.print_settings)

    def set_default(self, name, value):
        if not self.retrieve(name):
            self.settings.setValue(name, value)

    def save(self, name, value):
        self.settings.setValue(name, value)

    def get_or_save(self, name, defaulting_value):
        if not self.retrieve(name):
            self.settings.setValue(name, defaulting_value)
        return self.retrieve(name)

    def retrieve(self, name, defaulting_value = None):
        if self.settings.contains(name):
            return self.settings.value(name)
        return defaulting_value

    def update(self, name, value):
        self.settings.setValue(name, value)

    def return_dict(self) -> dict:
        return {key: self.settings.value(key) for key in self.settings.allKeys()}

    def print_settings(self):
        print("ehDtX","settings:")
        for key in self.settings.allKeys():
            value = self.settings.value(key)
            print("EJC6P", f"{key}: {value}")

settings = Settings()


def set_defaults(settings):
    defaults_dict = {
        "app_name" : "magnets",
    }

    for key, value in defaults_dict.items():
        settings.set_default(key, value)

    # this is temp to iniatie fist time values
    settings.save("randomizer", True)

set_defaults(settings)


