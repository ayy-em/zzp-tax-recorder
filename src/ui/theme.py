import flet as ft


# Color constants
PRIMARY_COLOR = "#2b5876"
SECONDARY_COLOR = "#4e4376"
TEXT_COLOR = "#FAFAFA"

# Font constants
FONT_FAMILY = "Ubuntu"
FONT_FAMILY_URL = "https://fonts.googleapis.com/css2?family=Ubuntu:wght@300;400;500;700&display=swap"
FONT_SIZE = "1.5rem"

# Background gradient
BACKGROUND_GRADIENT = ft.LinearGradient(
    begin=ft.alignment.top_left,
    end=ft.alignment.bottom_right,
    colors=[PRIMARY_COLOR, SECONDARY_COLOR],
    rotation=-20,
)

# Text style
TEXT_STYLE = ft.TextStyle(
    color=TEXT_COLOR,
    font_family=FONT_FAMILY,
    size=FONT_SIZE,
)

APPBAR_TEXT_STYLE = ft.TextStyle(
    color=TEXT_COLOR,
    font_family=FONT_FAMILY,
    size=FONT_SIZE,
)

# Card style
CARD_STYLE = {
    "bgcolor": ft.Colors.WHITE,
    "elevation": 5,
    "border_radius": 10,
    "padding": 15,
}

# Button style
BUTTON_STYLE = {
    # ToDo: this does not work
    "bgcolor": PRIMARY_COLOR,
    "color": TEXT_COLOR,
    "font_family": FONT_FAMILY,
    "border_radius": 5,
    "padding": 10,
}

# Input field style
INPUT_FIELD_STYLE = {
    "border_color": PRIMARY_COLOR,
    "border_radius": 5,
    "focused_border_color": SECONDARY_COLOR,
    "focused_bgcolor": ft.Colors.WHITE,
    "bgcolor": ft.Colors.WHITE,
    "color": ft.Colors.BLACK,
    "font_family": FONT_FAMILY,
}

# Container style for pages
PAGE_CONTAINER_STYLE = {
    "gradient": BACKGROUND_GRADIENT,
    "padding": 0,
    "expand": True,
}

# Function to apply theme to a page
def apply_theme(page: ft.Page):
    """Apply the theme to a Flet page"""
    page.bgcolor = BACKGROUND_GRADIENT
    page.fonts = {
        FONT_FAMILY: FONT_FAMILY_URL
    }
    page.padding = 0
    page.spacing = 0
    page.window_maximizable = True
    page.window_resizable = True
    page.window_full_screen = False
    page.window_always_on_top = False
    page.window_center = True
    page.window_min_width = 800
    page.window_min_height = 600
    page.update() 