import flet as ft
from typing import Callable, Dict, Any
from ui.transaction_views import IncomeForm, ExpenseForm
from models.objects import TransactionType
from ui.theme import TEXT_STYLE, PAGE_CONTAINER_STYLE
from ui.custom_elements import CustomAppBar


def create_transaction_form_view(router) -> Callable[[], ft.View]:
    """Create a factory function for the transaction form view"""
    
    def transaction_form_view_factory() -> ft.View:
        # Get parameters from route
        year = int(router.page.route_params.get("year", 0))
        transaction_type = router.page.route_params.get("transaction_type", "")
        
        def go_back(e):
            router.navigate(f"/year/{year}")
        
        def save_transaction(data: Dict[str, Any]):
            # TODO: Save transaction to database
            print(f"Saving {transaction_type} transaction: {data}")
            # Navigate back to year view after saving
            router.navigate(f"/year/{year}")
        
        # Create the appropriate form based on transaction type
        if transaction_type == "income":
            form = IncomeForm(on_save=save_transaction)
            title = "Add Income"
        elif transaction_type == "expense":
            form = ExpenseForm(on_save=save_transaction)
            title = "Add Expense"
        else:
            return router._create_404_view()
        
        return ft.View(
            route=f"/year/{year}/add/{transaction_type}",
            controls=[
                CustomAppBar(
                    title=title,
                    leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=go_back),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=30, weight=ft.FontWeight.BOLD, style=TEXT_STYLE),
                        ft.Divider(color=ft.Colors.WHITE),
                        form,
                    ], spacing=20),
                    **PAGE_CONTAINER_STYLE,
                    expand=True,
                    width=router.page.window_width,
                    height=router.page.window_height,
                ),
            ],
            padding=0,
            spacing=0,
        )
    
    return transaction_form_view_factory 