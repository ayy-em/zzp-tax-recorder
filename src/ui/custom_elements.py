import flet as ft
from ui.theme import TEXT_COLOR, FONT_FAMILY, FONT_SIZE, PRIMARY_COLOR, TEXT_STYLE, BUTTON_STYLE, APPBAR_TEXT_STYLE


class CustomUIButton(ft.ElevatedButton):
    """Custom button with consistent styling"""
    def __init__(self, text: str, icon: str = None, on_click=None, **kwargs):
        super().__init__(
            text=text,
            icon=icon,
            on_click=on_click,
            **kwargs
        )


class CustomAppBar(ft.AppBar):
    """Custom AppBar with consistent styling across the application"""
    def __init__(self, title: str, leading: ft.Control = None, actions: list = None, **kwargs):
        super().__init__(
            title=ft.Text(title, style=APPBAR_TEXT_STYLE),
            leading=leading,
            actions=actions,
            **kwargs
        ) 
