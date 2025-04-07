import flet as ft
from datetime import date
from decimal import Decimal
from typing import Optional, Callable

from models.objects import Transaction, Income, Expense, TransactionType, TransactionCategory
from ui.theme import TEXT_STYLE, CARD_STYLE, BUTTON_STYLE, INPUT_FIELD_STYLE
from ui.custom_elements import CustomUIButton

class TransactionView(ft.Control):
    """Base class for displaying a transaction"""
    def __init__(self, transaction: Transaction, on_edit: Optional[Callable] = None):
        super().__init__()
        self.transaction = transaction
        self.on_edit = on_edit

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            self.transaction.description,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            style=TEXT_STYLE
                        ),
                        ft.Text(
                            f"€{self.transaction.gross_amount:,.2f}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN if self.transaction.type == TransactionType.INCOME else ft.Colors.RED,
                            style=TEXT_STYLE
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(f"Counterparty: {self.transaction.counterparty}", style=TEXT_STYLE),
                    ft.Row([
                        ft.Text(f"Date: {self.transaction.date.strftime('%Y-%m-%d')}", style=TEXT_STYLE),
                        ft.Text(f"Category: {self.transaction.category.value.replace('_', ' ').title()}", style=TEXT_STYLE),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text(f"Net: €{self.transaction.net_amount:,.2f}", style=TEXT_STYLE),
                        ft.Text(f"VAT: €{self.transaction.vat_amount:,.2f}", style=TEXT_STYLE),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ]),
                padding=10
            ),
            **CARD_STYLE
        )

class IncomeView(TransactionView):
    """View for displaying an income transaction"""
    def __init__(self, income: Income, on_edit: Optional[Callable] = None):
        super().__init__(income, on_edit)

class ExpenseView(TransactionView):
    """View for displaying an expense transaction"""
    def __init__(self, expense: Expense, on_edit: Optional[Callable] = None):
        super().__init__(expense, on_edit)

class TransactionForm(ft.Control):
    """Base class for transaction forms"""
    def __init__(self, on_save: Callable, transaction: Optional[Transaction] = None):
        super().__init__()
        self.on_save = on_save
        self.transaction = transaction
        
        # Form fields
        self.date_field = ft.DatePicker(
            first_date=date(2020, 1, 1),
            last_date=date(2030, 12, 31),
            on_change=self._date_changed
        )
        self.description_field = ft.TextField(
            label="Description",
            value=transaction.description if transaction else "",
            required=True,
            **INPUT_FIELD_STYLE
        )
        self.counterparty_field = ft.TextField(
            label="Counterparty",
            value=transaction.counterparty if transaction else "",
            required=True,
            **INPUT_FIELD_STYLE
        )
        self.net_amount_field = ft.TextField(
            label="Net Amount (€)",
            value=str(transaction.net_amount) if transaction else "",
            required=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            **INPUT_FIELD_STYLE
        )
        self.vat_amount_field = ft.TextField(
            label="VAT Amount (€)",
            value=str(transaction.vat_amount) if transaction else "",
            required=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            **INPUT_FIELD_STYLE
        )
        self.gross_amount_field = ft.TextField(
            label="Gross Amount (€)",
            value=str(transaction.gross_amount) if transaction else "",
            required=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            disabled=True,
            **INPUT_FIELD_STYLE
        )
        self.category_dropdown = ft.Dropdown(
            label="Category",
            required=True,
            **INPUT_FIELD_STYLE
        )
        
        # Calculate button
        self.calculate_button = CustomUIButton(
            text="Calculate Gross",
            icon=ft.icons.CALCULATE,
            on_click=self._calculate_gross,
        )
        
        # Save button
        self.save_button = CustomUIButton(
            text="Save",
            icon=ft.icons.SAVE,
            on_click=self._save,
        )

    def _date_changed(self, e):
        self.date_field.value = e.date
        self.update()

    def _calculate_gross(self, e):
        try:
            net = Decimal(self.net_amount_field.value or "0")
            vat = Decimal(self.vat_amount_field.value or "0")
            gross = net + vat
            self.gross_amount_field.value = str(gross)
            self.update()
        except (ValueError, TypeError):
            self.gross_amount_field.value = "Invalid input"
            self.update()

    def _save(self, e):
        try:
            data = {
                "date": self.date_field.value,
                "description": self.description_field.value,
                "counterparty": self.counterparty_field.value,
                "net_amount": Decimal(self.net_amount_field.value),
                "vat_amount": Decimal(self.vat_amount_field.value),
                "gross_amount": Decimal(self.gross_amount_field.value),
                "category": self.category_dropdown.value
            }
            self.on_save(data)
        except (ValueError, TypeError) as ex:
            # Show error message
            pass

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Date", size=16, style=TEXT_STYLE),
                self.date_field,
                self.description_field,
                self.counterparty_field,
                self.net_amount_field,
                self.vat_amount_field,
                self.gross_amount_field,
                self.category_dropdown,
                ft.Row([
                    self.calculate_button,
                    self.save_button
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ]),
            padding=20
        )

class IncomeForm(TransactionForm):
    """Form for adding/editing income transactions"""
    def __init__(self, on_save: Callable, income: Optional[Income] = None):
        super().__init__(on_save, income)
        self.category_dropdown.options = [
            ft.dropdown.Option(category.value) 
            for category in TransactionCategory 
            if category.value in ["salary", "consulting", "project", "other_income"]
        ]
        if income:
            self.category_dropdown.value = income.category.value

class ExpenseForm(TransactionForm):
    """Form for adding/editing expense transactions"""
    def __init__(self, on_save: Callable, expense: Optional[Expense] = None):
        super().__init__(on_save, expense)
        self.category_dropdown.options = [
            ft.dropdown.Option(category.value) 
            for category in TransactionCategory 
            if category.value not in ["salary", "consulting", "project", "other_income"]
        ]
        if expense:
            self.category_dropdown.value = expense.category.value 
            