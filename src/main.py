import flet as ft
from routes.router import Router
from routes.home_route import create_home_view
from routes.year_route import create_year_view
from routes.transaction_form_route import create_transaction_form_view
from db.database import init_db
from ui.theme import apply_theme


def main(page: ft.Page):
    # Initialize the database
    init_db()
    
    # Configure the page
    page.title = "ZZP Tracker"
    
    # Apply the theme
    apply_theme(page)
    
    # Create the router
    router = Router(page)
    
    # Register exact routes
    router.register_route("/", create_home_view(router))
    
    # Register pattern routes
    router.register_pattern_route("/year/{year}", create_year_view(router))
    router.register_pattern_route("/year/{year}/add/{transaction_type}", create_transaction_form_view(router))
    
    # Initialize the router
    router.go()


ft.app(main)
