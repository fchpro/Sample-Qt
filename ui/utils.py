from logger_config import log_args_kwargs as print
import json
import os
import re
from functools import cache
import svgwrite

from PIL import Image, ImageDraw
from PySide6 import QtCore, QtGui, QtSvg, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QDialog

from constants import FRAMEWORKS_BUTTONS_SIZE
#from debugger import log_error, print, log_function_call
from paths import Paths
from utils import os_funcs
from utils.cache import key_cache

import shutil

##from debugger import print, log_error, log_function_call, stop_script, save_current_pil_images
re_svglw = re.compile('stroke-width="(.*?)"')
re_svgcolor = re.compile('(color="(.*?)")')
re_svgstroke = re.compile('stroke="(.*?)"')

def create_sequential_folder(base_path):
    counter = 1
    while True:
        folder_name = f"{counter:03d}"
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            return folder_path
        counter += 1


def set_minimum_height_for_all_buttons(dialog: QDialog):
    for child in dialog.children():
        if isinstance(child, QPushButton):
            child.setMinimumHeight(40)


class DynamicPushButton(QtWidgets.QPushButton):
    def setProperty(self, name, value):
        super().setProperty(name, value)
        self.style().polish(self)


def build_svg(srcfile: str, lw=None, color=None, opacity=None, **kwargs):
    """Takes a source SVG and modifies it, replacing line
    width and color values. Stores the result in the icon cache
    using a reproducible name.

    Args:
        srcfile (str): The source SVG to load.
        lw (float, optional): The line width. Defaults to None.
        color (str, optional): Hex color code. Defaults to None.
    """
    if isinstance(color, QtGui.QColor):
        color = color.name()

    attribs = [lw, color, opacity]
    srcfile = srcfile

    if all(v is None for v in attribs):
        # Use original.
        return Paths.icon(srcfile)

    # Build the cache filename.
    name, ext = os.path.splitext(srcfile)
    namedef = "_".join([str(v) for v in attribs if v is not None])
    outfile = Paths.cached_icon(name + "_" + namedef + ext)

    # If it already exists, return it.
    if os.path.exists(outfile):
        return outfile

    with open(Paths.icon(srcfile), "r") as f:
        svg = f.read()

    # It doesn't, so build it.
    if lw is not None:
        svg = re_svglw.sub(f'stroke-width="{lw}"', svg)

    if color is not None:
        svg = re_svgcolor.sub(f'color="{color}"', svg)
        svg = re_svgstroke.sub(f'stroke="{color}"', svg)

    if opacity is not None:
        svg = re_svgcolor.sub(f'\g<1> opacity="{opacity}"', svg)

    with open(outfile, "w") as f:
        f.write(svg)
    return outfile


BUTTON_MODE_STATES = [
    (QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On),
    (QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off),
    (QtGui.QIcon.Mode.Disabled, QtGui.QIcon.State.On),
    (
        QtGui.QIcon.Mode.Disabled,
        QtGui.QIcon.State.Off,
    ),
]


@key_cache
def build_icon(
    icons,
    states=None,
    colors=None,
    **kwargs,
):
    colors = colors or {}

    # Default just define for Enabled/Disabled states.
    icon = QtGui.QIcon()

    # Build the buttons, adding states and colors for different states.
    # By default, single filename = same icon for all states.
    if isinstance(icons, str):
        states = {
            (QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off): icons,
            (QtGui.QIcon.Mode.Disabled, QtGui.QIcon.State.Off): icons,
            (QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On): icons,
            (QtGui.QIcon.Mode.Disabled, QtGui.QIcon.State.On): icons,
        }
    elif isinstance(icons, list):
        states = dict(**zip(*icons, *BUTTON_MODE_STATES))
    else:
        # Manually defined mode/states.
        states = icons

    for modestate, iconfile in states.items():
        color = colors.get(modestate, "white")
        mode, state = modestate
        kw = {
            "lw": 1,
            "color": color,
        }
        kw.update(**kwargs)
        icon.addFile(build_svg(iconfile, **kw), mode=mode, state=state)

    return icon


@cache
def build_pixmap(srcfile: str, lw=None, color=None, size=12):
    """Builds an icon pixmap. That is a widget which displays
    the specified icon.

    Args:
        srcfile (str): _description_
        lw (_type_, optional): _description_. Defaults to None.
        color (_type_, optional): _description_. Defaults to None.
        size
    """
    icon_file = build_svg(srcfile, lw, color)
    renderer = QtSvg.QSvgRenderer(icon_file)

    image = QtGui.QImage(size * 2, size * 2, QtGui.QImage.Format_ARGB32)
    image.fill(Qt.transparent)

    painter = QtGui.QPainter(image)
    painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()

    pixmap = QtGui.QPixmap.fromImage(image)
    pixmap.setDevicePixelRatio(2)
    return pixmap


def build_button(
    icons,
    states=None,
    size=None,
    isize=12,
    tooltip=None,
    hover=False,
    colors=None,
    btn_widget=None,
    label=None,
    min_width=None,
    no_max_width=False,
    **kwargs,
):
    if btn_widget:
        btn = btn_widget
    else:
        btn = DynamicPushButton()

    colors = colors or {}

    # Default just define for Enabled/Disabled states.
    btn.setObjectName("builtButton")
    icon = build_icon(icons, states=None, colors=None, **kwargs)
    btn.setIcon(icon)
    btn.setIconSize(QtCore.QSize(isize, isize))
    if size:
        btn.setFixedSize(QtCore.QSize(size, size))
    if tooltip:
        btn.setToolTip(tooltip)
    if label:
        btn.setText(label)
    if min_width:
        btn.setMinimumWidth(min_width)
    return btn


def build_enabled_icon_pair(icon_filename, **kwargs):
    icon = QtGui.QIcon()
    icon.addFile(build_svg(icon_filename, **kwargs),
                 mode=QtGui.QIcon.Mode.Normal)
    icon.addFile(build_svg(icon_filename, opacity=0.25, **kwargs),
                 mode=QtGui.QIcon.Mode.Disabled)
    return icon

# Helper function to create a row with a label and a line edit
# def create_input_row(widget, label_text, attribute_name):
#     label = QLabel(label_text)
#     line_edit = QLineEdit()
#
#     widget.layout().addWidget(label)
#     widget.layout().addWidget(line_edit)
#     widget.layout().addSpacing(10)
#
#     setattr(line_edit, attribute_name, line_edit)


 
def create_input_row(widget, label_text, attribute_name):
    label = QLabel(label_text)
    line_edit = QLineEdit()

    # Add the label and line edit to the widget's layout
    widget.layout().addWidget(label)
    widget.layout().addWidget(line_edit)
    widget.layout().addSpacing(10)

    # Set the line_edit as an attribute of the widget
    setattr(widget, attribute_name, line_edit)


 
def update_template_data_with_new_icon(template_data, new_icon_path, template_folder):
    """find the json file then add the icon path to the json file under the key "icon_path" """
    for file_name in os.listdir(template_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(template_folder, file_name)
            with open(file_path, "r+") as file:
                data = json.load(file)
                if data == template_data:
                    data["icon_path"] = new_icon_path
                    file.seek(0)
                    json.dump(data, file)
                    file.truncate()


 
def create_frameworks_template_icon(
    template_data,
    output_folder=Paths.frameworks_templates_icons,
    width=FRAMEWORKS_BUTTONS_SIZE[0],
    height=FRAMEWORKS_BUTTONS_SIZE[1],
    image_color="white",
    text_color="cyan",
):
    """create a frameworks icon as png or svg for the frameworks template button"""

    template_name = template_data.get("name")

    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Scaling factors
    scale_x = width / template_data["framework"]["width"]
    scale_y = height / template_data["framework"]["height"]

    # Draw image rectangle if exists
    if "image" in template_data:
        x, y = [int(i * scale_x) for i in template_data["image"]["position"]]
        w, h = [int(i * scale_y) for i in template_data["image"]["size"]]
        # Ensure the rectangle does not go beyond the image height
        y = min(y, height - h)
        draw.rectangle([x, y, x + w, y + h], outline=image_color, width=2)

    # Draw text rectangles if exist
    if "texts" in template_data:
        for text in template_data["texts"]:
            x, y = [int(i * scale_x) for i in text["position"]]
            w, h = [int(i * scale_x) for i in text["size"]]
            # Ensure the rectangle does not go beyond the image height
            y = min(y, height - h)
            draw.rectangle([x, y, x + w, y + h], outline=text_color, width=2)

    icon_output_path = f"{output_folder}/{template_name}_icon.png"

    img.save(icon_output_path, "PNG")
    try:
        update_template_data_with_new_icon(
            template_data, icon_output_path, output_folder
        )
    except Exception as e:
        log_error("couldn't update tempalte data with new icon ,", e)
    return icon_output_path


 
def create_basic_template_icon_svg(template_data, output_folder=Paths.frameworks_templates_icons,
                                   width=FRAMEWORKS_BUTTONS_SIZE[0], height=FRAMEWORKS_BUTTONS_SIZE[1],
                                   image_color="#F0F0F0", text_color="#007ACC"):
    """create a basic icon as svg for the basic template button """
    template_name = template_data.get("name")
    dwg = svgwrite.Drawing(
        f"{output_folder}/{template_name}_icon.svg", size=(width, height))

    # Scaling factors
    scale_x = width / template_data["framework"]["width"]
    scale_y = height / template_data["framework"]["height"]

    # Draw image rectangle if exists
    if "image" in template_data:
        x, y = [i * scale_x for i in template_data["image"]["position"]]
        w, h = [i * scale_y for i in template_data["image"]["size"]]
        # Ensure the rectangle does not go beyond the image height
        y = min(y, height - h)
        dwg.add(dwg.rect(insert=(x, y), size=(w, h),
                stroke=image_color, fill='none'))

    # Draw text rectangles if exist
    if "texts" in template_data:
        for text in template_data["texts"]:
            x, y = [i * scale_x for i in text["position"]]
            w, h = [i * scale_x for i in text["size"]]
            # Ensure the rectangle does not go beyond the image height
            y = min(y, height - h)
            dwg.add(dwg.rect(insert=(x, y), size=(w, h),
                    stroke=text_color, fill='none'))

    dwg.save()
    try:
        update_template_data_with_new_icon(
            template_data, f"{output_folder}/{template_name}_icon.svg", output_folder)
    except Exception as e:
        log_error("couldn't update template data with new icon,", e)
    return f"{output_folder}/{template_name}_icon.svg"


 
def check_if_template_data_has_valid_icon(
    template_data
):
    """check if there's already an icon for this template in the icons folder
    RETURNS :
        None if there's no valid icon already made
        ICON_PATH if it does exist
    """
    # icon_name = template_data.get("icon_path", None)
    template_name = template_data.get("name", None)

    if template_name is None:
        return None

    try:
        icon_name = template_name + "_icon.svg"
        icon_path = os.path.join(Paths.frameworks_templates_icons, icon_name)

        if os_funcs.is_image_file(icon_path) or os_funcs.is_svg_file(icon_path):
            print(
                "got a already premade icon for the template button :", icon_path)
            return icon_path

    except Exception:
        log_error("couldn't get a premade icon , error happned")
        return None
