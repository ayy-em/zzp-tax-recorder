import flet as ft


def main(page: ft.Page):
    def navigate_to_year(year):
        def on_click(e):
            page.route = f"/{str(year)}"
            page.update()
        return on_click

    def create_year_page(year):
        def go_back(e):
            page.route = "/"
            page.update()
        
        return ft.View(
            route=f"/{year}",
            controls=[
                ft.AppBar(title=ft.Text(f"Year {year}")),
                ft.SafeArea(
                    ft.Container(
                        ft.Column([
                            ft.Text(f"Year {year}", size=30, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
                                size=16,
                            ),
                            ft.ElevatedButton("Back to Home", on_click=go_back),
                        ], spacing=20),
                        padding=20,
                    ),
                    expand=True,
                ),
            ],
        )

    def route_change(e):
        page.views.clear()
        if page.route == "/":
            buttons = [
                ft.ElevatedButton(text="2023", on_click=navigate_to_year(2023)),
                ft.ElevatedButton(text="2024", on_click=navigate_to_year(2024)),
                ft.ElevatedButton(text="2025", on_click=navigate_to_year(2025)),
                ft.ElevatedButton(text="2026", on_click=navigate_to_year(2026)),
            ]
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.SafeArea(
                            ft.Container(
                                ft.Column(buttons, alignment=ft.alignment.center),
                                alignment=ft.alignment.center,
                            ),
                            expand=True,
                        )
                    ],
                )
            )
        else:
            year = int(page.route[1:])  # Remove the leading slash
            page.views.append(create_year_page(year))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(main)
