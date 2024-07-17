import os


class Paths:
    base = os.path.dirname(__file__)
    effects = os.path.join(base, "../unused/effects")
    old_effects = os.path.join(effects, "../unused")
    resources = os.path.join(base, "resources")
    temp = os.path.join(base, "temp")
    temp_templates = os.path.join(temp, "temp_templates")
    temp_images = os.path.join(temp, "temp_images")
    checkers_cache = os.path.join(temp, "checkers_cache")
    log_folder = os.path.join(base, "log_folder")
    log_file = os.path.join(log_folder, "log.txt")
    sample_image = os.path.join(temp_images, "sample_image.png")
    ui_files = os.path.join(base, "ui")
    assets = os.path.join(ui_files, "assets")
    ui_images = os.path.join(assets, "images")
    loading_gif = os.path.join(ui_images, "loading.gif")
    templates = os.path.join(resources, "templates")
    

    fonts_from_resources = os.path.join(resources, "fonts")
    others_from_resources = os.path.join(resources, "others")
    previewer_bg = os.path.join(others_from_resources, "previewer_background.png")
    frameworks_templates = os.path.join(templates, "frameworks")

    blueprints_templates = os.path.join(templates, "blueprints")
    outputs = os.path.join(base, "outputs")
    output_folder = os.path.join(base, "outputs")
    debug_folder = os.path.join(base, "debug_folder")

    image_inputs = os.path.join(base, "image_inputs")
    elephant = os.path.join(image_inputs, "elephant.png")
    square = os.path.join(image_inputs, "72.jpg")
    small_square = os.path.join(image_inputs, "small_72.jpg")
    valid_font = os.path.join(fonts_from_resources, "LuckiestGuy-Regular.ttf")
    belive = os.path.join(image_inputs, "text i beliebe.png")

    # UI assets.
    ui_fonts = os.path.join(assets, "fonts")
    icons = os.path.join(assets, "icons")
    icon_cache = os.path.join(icons, "cache")
    styles = os.path.join(assets, "styles")
    frameworks_templates_icons = os.path.join(frameworks_templates, "frameworks_icons")
    ui_images = os.path.join(assets, "images")

    # File loaders.
    @classmethod
    def effect(cls, filename):
        return os.path.join(cls.effects, filename)

    @classmethod
    def old_effect(cls, filename):
        return os.path.join(cls.old_effects, filename)

    @classmethod
    def resource(cls, filename):
        return os.path.join(cls.resources, filename)

    @classmethod
    def font(cls, filename):
        return os.path.join(cls.ui_fonts, filename)

    @classmethod
    def icon(cls, filename):
        return os.path.join(cls.icons, filename)

    @classmethod
    def cached_icon(cls, filename):
        return os.path.join(cls.icon_cache, filename).replace("\\", "/")

    @classmethod
    def style(cls, filename):
        return os.path.join(cls.styles, filename)

    @classmethod
    def template(cls, filename):
        return os.path.join(cls.templates, filename)
