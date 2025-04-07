import flet as ft
from typing import Callable
from ui.theme import TEXT_STYLE, BUTTON_STYLE, PAGE_CONTAINER_STYLE, CARD_STYLE
from ui.custom_elements import CustomUIButton, CustomAppBar


def create_year_view(router) -> Callable[[], ft.View]:
    """Create a factory function for the year view"""
    
    def year_view_factory() -> ft.View:
        # Get year from route parameters
        year = int(router.page.route_params.get("year", 0))
        
        def go_back(e):
            router.navigate("/")
        
        def add_income(e):
            router.navigate(f"/year/{year}/add/income")
        
        def add_expense(e):
            router.navigate(f"/year/{year}/add/expense")
        
        return ft.View(
            route=f"/year/{year}",
            controls=[
                CustomAppBar(
                    title=f"Year {year}",
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(f"Year {year}", size=30, weight=ft.FontWeight.BOLD, style=TEXT_STYLE),
                        ft.Row([
                            CustomUIButton(
                                text="Add Income", 
                                icon=ft.Icons.ADD, 
                                on_click=add_income,
                            ),
                            CustomUIButton(
                                text="Add Expense", 
                                icon=ft.Icons.REMOVE, 
                                on_click=add_expense,
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                        ft.Divider(color=ft.Colors.WHITE),
                        ft.Text("Transactions will be displayed here", size=16, style=TEXT_STYLE),
                        # Placeholder for transaction list
                        ft.Container(
                            ft.Column([
                                ft.Text("No transactions yet", italic=True, style=TEXT_STYLE),
                            ]),
                            padding=20,
                            border=ft.border.all(1, ft.Colors.WHITE),
                            border_radius=10,
                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        ),
                    ], spacing=20),
                    **PAGE_CONTAINER_STYLE,
                ),
            ],
            padding=0,
            spacing=0,
        )
    
    return year_view_factory 