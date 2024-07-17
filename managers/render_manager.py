from logger_config import log_args_kwargs as print
# from utils.create_entry_string_from_data import create_the_sting_i_want_from_data
import os

from PySide6.QtCore import QAbstractListModel, Qt

#from debugger import log_error, print
from global_signals import global_signals
from managers.calc_n_variations import calculate_number_of_variations_from_data
from permutator_directory.old.data_fetcher import DataFetcher


def truncate(input_string):
    if len(input_string) <= 10:
        return input_string
    else:
        return input_string[:10] + "..."


def build_label(data):
    # try:
    data = DataFetcher(data)

    overlay_image_path_list_from_data = data.fetch("overlay_image_paths_list")
    overlay_folder_path_from_data = data.fetch("overlay_folder_path")

    if (
        overlay_folder_path_from_data is None
        and overlay_image_path_list_from_data is None
    ):
        final_overlay = "No Image Selected"
    elif len(overlay_image_path_list_from_data) == 0:
        final_overlay = "No Image Selected"

    elif (
        type(overlay_folder_path_from_data) == str
        and overlay_folder_path_from_data != ""
    ):
        final_overlay = overlay_folder_path_from_data

    elif (
        type(overlay_image_path_list_from_data) == list
        and len(overlay_image_path_list_from_data) > 0
    ):
        final_overlay = [
            os.path.basename(path) for path in overlay_image_path_list_from_data
        ]
    else:
        final_overlay = "No Image Selected"

    texts_list_of_tuples_from_data = data.fetch("input_texts")

    final_text = ""
    if texts_list_of_tuples_from_data is None:
        pass
    else:
        final_text = truncate("-" + str(len(texts_list_of_tuples_from_data)) + "TXT-")

    def sum_lengths_of_non_none(items):
        total_length = 0
        for item in items:
            if item is not None:
                if isinstance(item, dict) and "effects" in item:
                    total_length += len(item["effects"])
                else:
                    total_length += len(item)
        return total_length

    try:
        list_of_effects_variables = [
            data.fetch("canvas_effects_checked"),
            data.fetch("overlay_effects_selection_list"),
            data.fetch("text_1_data"),
            data.fetch("text_2_data"),
            data.fetch("text_3_data"),
            data.fetch("text_5_data"),
            data.fetch("text_4_data"),
        ]

        effects = sum_lengths_of_non_none(list_of_effects_variables)
        effects = f"-{effects}EFFECTS"
    except:
        log_error(" couldn't get the effects num")
        effects = ""

    def count_non_none_variables_by_key(variable_names):
        return sum(1 for name in variable_names if data.fetch(name) is not None)

    try:
        text_options = count_non_none_variables_by_key(
            [
                "all_outline_color",
                "outline_thickness",
                "image_for_ai_colors",
                "all_text_bottom_color",
                "all_text_top_color",
                "text_drop_shadow_enabled",
            ]
        )
        text_options = f"-{text_options}txt_params"
    except:
        text_options = ""

    try:
        general_options = count_non_none_variables_by_key(
            [
                "canvas_custom_background",
                "distress_file_path",
                "keep_original_distress",
                "overlay_knockout_path",
                "keep_original_overlay_knockout",
            ]
        )
        general_options = f"-{general_options}gen_params"
    except:
        general_options = ""

    return f"-{final_overlay}{final_text}{effects}{text_options}{general_options}"


class RenderManager(QAbstractListModel):
    def __init__(self):
        super().__init__()

        self._data = []
        try:
            global_signals.clear_render_data_list.connect(self.clear)
            print("did run the clear render data list from global signals")
        except Exception:
            print("couldn't clear the render queue after start rendering")

    # Qt Model interface (for display).

    def data(self, index, role):
        if role == Qt.DisplayRole:
            data = self._data[index.row()]
            metadata = data["metadata"]
            return metadata["identifier"]

    def rowCount(self, index):
        return len(self._data)

    def clear(self):
        self.layoutAboutToBeChanged.emit()
        self._data = []
        self.layoutChanged.emit()

    @property
    def n_items(self):
        return len(self._data)

    @property
    def n_variations(self):
        print(
            "sum n_variations : ",
            sum(d["metadata"]["number_of_variations"] for d in self._data),
        )
        return sum(d["metadata"]["number_of_variations"] for d in self._data)

    def remove_last_item(self):
        # Check if there are items in the list
        if self._data:
            self.layoutAboutToBeChanged.emit()
            self._data.pop()
            self.layoutChanged.emit()

    #  
    def add_entry(self, data):
        print("addind entry")
        self.layoutAboutToBeChanged.emit()
        data["metadata"] = dict()
        data["metadata"]["number_of_variations"] = (
            calculate_number_of_variations_from_data(data)
        )
        data["metadata"]["identifier"] = str(
            data["metadata"]["number_of_variations"]
        ) + build_label(data)
        self._data.append(data)
        self.layoutChanged.emit()

    def remove_item_by_row_index(self, row_index):
        self.layoutAboutToBeChanged.emit()
        try:
            del self._data[row_index]
        except Exception:
            pass
        self.layoutChanged.emit()

    def give_back_current_active_data_list_for_saving(self):
        return self._data


# render_manager = RenderManager()
