import flet as ft
from typing import Callable
from ui.theme import TEXT_STYLE, BUTTON_STYLE, PAGE_CONTAINER_STYLE, BACKGROUND_GRADIENT
from ui.custom_elements import CustomUIButton, CustomAppBar


def create_home_view(router) -> Callable[[], ft.View]:
    """Create a factory function for the home view"""
    
    def home_view_factory() -> ft.View:
        def navigate_to_year(year: int):
            def on_click(e):
                router.navigate(f"/year/{year}")
            return on_click
        
        buttons = [
            CustomUIButton(
                text="2023", 
                on_click=navigate_to_year(2023),
            ),
            CustomUIButton(
                text="2024", 
                on_click=navigate_to_year(2024),
            ),
            CustomUIButton(
                text="2025", 
                on_click=navigate_to_year(2025),
            ),
            CustomUIButton(
                text="2026", 
                on_click=navigate_to_year(2026),
            ),
        ]
        
        return ft.View(
            route="/",
            controls=[
                CustomAppBar(
                    title="ZZP Tracker",
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Welcome to ZZP Tracker", 
                            size=30, 
                            weight=ft.FontWeight.BOLD,
                            style=TEXT_STYLE
                        ),
                        ft.Text(
                            "Select a year to view your financial data or add new transactions.",
                            size=16,
                            style=TEXT_STYLE
                        ),
                        ft.Divider(color=ft.Colors.WHITE),
                        ft.Text(
                            "Select Year:", 
                            size=20, 
                            weight=ft.FontWeight.BOLD,
                            style=TEXT_STYLE
                        ),
                        ft.Row(buttons, alignment=ft.MainAxisAlignment.CENTER),
                    ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
                    **PAGE_CONTAINER_STYLE,
                ),
            ],
            padding=0,
            spacing=0,
            bgcolor=BACKGROUND_GRADIENT,
        )
    
    return home_view_factory 