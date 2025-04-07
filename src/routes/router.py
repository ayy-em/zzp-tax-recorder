import flet as ft
from typing import Dict, Callable, List, Optional, Any
import re


class Router:
    """Base router class for handling navigation in the application"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.routes: Dict[str, Callable[[], ft.View]] = {}
        self.pattern_routes: List[tuple] = []  # List of (pattern, view_factory) tuples
        self.current_view: Optional[ft.View] = None
        
        # Set up route change handler
        self.page.on_route_change = self._handle_route_change
    
    def register_route(self, route: str, view_factory: Callable[[], ft.View]) -> None:
        """Register a route with its view factory"""
        self.routes[route] = view_factory
    
    def register_pattern_route(self, pattern: str, view_factory: Callable[[], ft.View]) -> None:
        """Register a route pattern with its view factory"""
        # Convert route pattern to regex pattern
        regex_pattern = re.compile(pattern.replace("{", "(?P<").replace("}",">[^/]+)"))
        self.pattern_routes.append((regex_pattern, view_factory))
    
    def _handle_route_change(self, e) -> None:
        """Handle route changes"""
        self.page.views.clear()
        
        # Get the current route
        route = self.page.route
        
        # First check exact matches
        if route in self.routes:
            view = self.routes[route]()
            self.page.views.append(view)
        else:
            # Then check pattern matches
            matched = False
            for pattern, view_factory in self.pattern_routes:
                match = pattern.match(route)
                if match:
                    # Store route parameters for use in the view factory
                    self.page.route_params = match.groupdict()
                    view = view_factory()
                    self.page.views.append(view)
                    matched = True
                    break
            
            # If no match found, show 404
            if not matched:
                self.page.views.append(self._create_404_view())
        
        self.page.update()
    
    def _create_404_view(self) -> ft.View:
        """Create a 404 view for unknown routes"""
        return ft.View(
            route="/404",
            controls=[
                ft.AppBar(title=ft.Text("Page Not Found")),
                ft.SafeArea(
                    ft.Container(
                        ft.Column([
                            ft.Text("404 - Page Not Found", size=30, weight=ft.FontWeight.BOLD),
                            ft.Text("The page you are looking for does not exist."),
                            ft.ElevatedButton("Go to Home", on_click=lambda _: self.navigate("/")),
                        ], spacing=20),
                        padding=20,
                    ),
                    expand=True,
                ),
            ],
        )
    
    def navigate(self, route: str) -> None:
        """Navigate to a specific route"""
        self.page.route = route
        self.page.update()
    
    def go(self, route: str = "/") -> None:
        """Initialize the router with a default route"""
        self.page.go(route) 