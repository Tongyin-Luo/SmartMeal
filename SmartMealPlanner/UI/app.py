import tkinter as tk

from UI.styles import BG


class SmartMealApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("SmartMeal")
        self.geometry("430x780")
        self.minsize(400, 650)

        self.configure(bg=BG)

        # Container for different pages
        self.container = tk.Frame(
            self,
            bg=BG
        )

        self.container.pack(
            fill="both",
            expand=True
        )

        # Start with Inventory page
        self.show_inventory()

    # Clear current page
    def clear_page(self):

        for widget in self.container.winfo_children():
            widget.destroy()

    # Show Inventory page
    def show_inventory(self):

        from UI.inventory_page import InventoryPage

        self.clear_page()

        page = InventoryPage(
            self.container,
            self
        )

        page.pack(
            fill="both",
            expand=True
        )

    # Show Add Ingredient page
    def show_add_ingredient(self):

        from UI.ingredient_page import IngredientPage

        self.clear_page()

        page = IngredientPage(
            self.container,
            self,
            ingredient_id=None
        )

        page.pack(
            fill="both",
            expand=True
        )

    # Show Update Ingredient page
    def show_update_ingredient(self, ingredient_id):

        from UI.ingredient_page import IngredientPage

        self.clear_page()

        page = IngredientPage(
            self.container,
            self,
            ingredient_id=ingredient_id
        )

        page.pack(
            fill="both",
            expand=True
        )