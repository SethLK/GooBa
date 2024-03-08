class Style:
    def __init__(self):
        self.color = None
        self.background_color = None
        self.font_size = None
        self.font_family = None
        self.font_weight = None
        self.font_style = None
        self.text_decoration = None
        self.text_align = None
        self.padding = None
        self.margin = None
        self.border = None
        self.border_radius = None
        self.width = None
        self.height = None
        self.position = None
        self.display = None
        self.float = None
        self.clear = None
        self.opacity = None
        self.box_shadow = None
        self.text_shadow = None
        self.line_height = None
        self.text_transform = None
        self.cursor = None
        self.transition = None


# Example usage:
class CustomStyle(Style):
    def __init__(self):
        super().__init__()
        # Additional styles specific to CustomStyle
        self.custom_property = None
