import tkinter as tk
from tkinter import ttk, messagebox

from UI.styles import (
    BG,
    WHITE,
    GREEN,
    DARK_GREEN,
    LIGHT_GREEN,
    TEXT,
    RED,
    FONT
)

from tasks.inventory_service import (
    add_ingredient,
    get_ingredient,
    update_ingredient
)

from tasks.validation_service import validate_ingredient


class IngredientPage(tk.Frame):

    def __init__(self, parent, app, ingredient_id=None):
        super().__init__(parent, bg=BG)

        self.app = app
        self.ingredient_id = ingredient_id
        self.is_editing = ingredient_id is not None

        # ======================================
        # Variables
        # ======================================

        self.name_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="pcs")

        # Original values
        self.original_name = None
        self.original_quantity = None
        self.original_unit = None

        # ======================================
        # Entry Style
        # ======================================

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "SmartMeal.TEntry",
            foreground=DARK_GREEN,
            fieldbackground=WHITE,
            background=WHITE,
            bordercolor=GREEN,
            lightcolor=GREEN,
            darkcolor=GREEN,
            insertcolor=DARK_GREEN,
            padding=10,
            relief="flat",
            borderwidth=1
        )

        self.style.map(
            "SmartMeal.TEntry",
            foreground=[("focus", DARK_GREEN)],
            fieldbackground=[("focus", WHITE)],
            bordercolor=[("focus", DARK_GREEN)],
            lightcolor=[("focus", GREEN)],
            darkcolor=[("focus", GREEN)]
        )

        # ======================================
        # Load Existing Data
        # ======================================

        if self.is_editing:

            try:
                ingredient = get_ingredient(
                    self.ingredient_id
                )

            except Exception as e:
                messagebox.showerror(
                    "Database Error",
                    str(e)
                )
                self.after_idle(self.app.show_inventory)
                return

            if ingredient is None:
                messagebox.showerror(
                    "Error",
                    "Ingredient not found."
                )
                self.after_idle(self.app.show_inventory)
                return

            _, name, quantity, unit = ingredient

            self.original_name = name
            self.original_quantity = quantity
            self.original_unit = unit

            self.name_var.set(name)
            self.quantity_var.set(
                self.format_quantity(quantity)
            )
            self.unit_var.set(unit)

        # ======================================
        # Title
        # ======================================

        title = (
            "Update Ingredient"
            if self.is_editing
            else "Add Ingredient"
        )

        tk.Label(
            self,
            text=title,
            font=(FONT, 25, "bold"),
            bg=BG,
            fg=DARK_GREEN
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        # ======================================
        # IH#6: Step-by-Step Instructions
        # ======================================

        if self.is_editing:

            instruction_text = (
                "Step 1: Review the current ingredient.\n"
                "Step 2: Enter the new quantity.\n"
                "Step 3: Confirm and save your changes."
            )

        else:

            instruction_text = (
                "Step 1: Enter the ingredient name.\n"
                "Step 2: Enter the quantity and unit.\n"
                "Step 3: Save the ingredient."
            )

        tk.Label(
            self,
            text=instruction_text,
            font=(FONT, 11),
            bg=LIGHT_GREEN,
            fg=DARK_GREEN,
            padx=15,
            pady=15,
            justify="left",
            wraplength=340
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        # ======================================
        # Form
        # ======================================

        form = tk.Frame(
            self,
            bg=BG
        )

        form.pack(
            fill="x",
            padx=25
        )

        # Ingredient Name
        self.create_label(
            form,
            "Ingredient Name"
        )

        self.name_entry = self.create_entry(
            form,
            self.name_var
        )

        # ======================================
        # IH#8: Show Original Quantity
        # ======================================

        if self.is_editing:

            current_quantity = self.format_quantity(
                self.original_quantity
            )

            tk.Label(
                form,
                text=(
                    f"Current Quantity: "
                    f"{current_quantity} {self.original_unit}"
                ),
                font=(FONT, 11),
                bg=LIGHT_GREEN,
                fg=DARK_GREEN,
                padx=12,
                pady=10
            ).pack(
                fill="x",
                pady=(0, 15)
            )

        # Quantity
        self.create_label(
            form,
            "New Quantity" if self.is_editing else "Quantity"
        )

        self.quantity_entry = self.create_entry(
            form,
            self.quantity_var
        )

        # Unit
        self.create_label(
            form,
            "Unit"
        )

        unit_frame = tk.Frame(
            form,
            bg=WHITE,
            highlightbackground=GREEN,
            highlightthickness=1
        )

        unit_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        unit_menu = tk.OptionMenu(
            unit_frame,
            self.unit_var,
            "pcs",
            "g",
            "kg",
            "ml",
            "L",
            "bottles",
            "tbsp"
        )

        unit_menu.configure(
            font=(FONT, 12),
            bg=WHITE,
            fg=DARK_GREEN,
            activebackground=LIGHT_GREEN,
            activeforeground=DARK_GREEN,
            relief="flat",
            bd=0,
            highlightthickness=0
        )

        unit_menu.pack(fill="x")

        # ======================================
        # Validation Error
        # ======================================

        self.error_label = tk.Label(
            self,
            text="",
            font=(FONT, 11),
            bg=BG,
            fg=RED,
            wraplength=340
        )

        self.error_label.pack(
            padx=25,
            pady=(5, 10)
        )

        # ======================================
        # Save Button
        # ======================================

        save_text = (
            "Save Changes"
            if self.is_editing
            else "Add Ingredient"
        )

        self.create_button(
            text=save_text,
            command=self.save_ingredient,
            background=DARK_GREEN,
            foreground=WHITE
        )

        # ======================================
        # Cancel Button
        # ======================================

        self.create_button(
            text="Cancel",
            command=self.app.show_inventory,
            background=LIGHT_GREEN,
            foreground=DARK_GREEN
        )

    # ==========================================
    # Format Quantity
    # ==========================================

    def format_quantity(self, quantity):

        text = format(quantity, "f")

        if "." in text:
            text = text.rstrip("0").rstrip(".")

        return text

    # ==========================================
    # Create Label
    # ==========================================

    def create_label(self, parent, text):

        tk.Label(
            parent,
            text=text,
            font=(FONT, 12, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

    # ==========================================
    # Create Entry
    # ==========================================

    def create_entry(self, parent, variable):

        entry = ttk.Entry(
            parent,
            textvariable=variable,
            font=(FONT, 13),
            style="SmartMeal.TEntry"
        )

        entry.pack(
            fill="x",
            pady=(0, 20),
            ipady=5
        )

        return entry

    # ==========================================
    # Custom Button
    # ==========================================

    def create_button(
        self,
        text,
        command,
        background,
        foreground
    ):

        button_frame = tk.Frame(
            self,
            bg=background,
            cursor="hand2"
        )

        button_frame.pack(
            fill="x",
            padx=25,
            pady=7
        )

        button_label = tk.Label(
            button_frame,
            text=text,
            font=(FONT, 13, "bold"),
            bg=background,
            fg=foreground,
            pady=14,
            cursor="hand2"
        )

        button_label.pack(fill="x")

        button_frame.bind(
            "<Button-1>",
            lambda event: command()
        )

        button_label.bind(
            "<Button-1>",
            lambda event: command()
        )

    # ==========================================
    # Save Ingredient
    # ==========================================

    def save_ingredient(self):

        name = self.name_var.get().strip()
        quantity = self.quantity_var.get().strip()
        unit = self.unit_var.get().strip()

        self.error_label.config(text="")

        # ======================================
        # Validate Input
        # ======================================

        valid, error = validate_ingredient(
            name,
            quantity,
            unit
        )

        if not valid:

            self.error_label.config(
                text=error
            )

            return

        # ======================================
        # IH#5 and IH#8: Confirm Update
        # ======================================

        if self.is_editing:

            old_quantity = self.format_quantity(
                self.original_quantity
            )

            confirm_message = (
                f"Ingredient: {name}\n\n"
                f"Previous Quantity: "
                f"{old_quantity} {self.original_unit}\n"
                f"New Quantity: {quantity} {unit}\n\n"
                f"Are you sure you want to save these changes?"
            )

            confirmed = messagebox.askyesno(
                "Confirm Update",
                confirm_message
            )

            if not confirmed:
                return

        # ======================================
        # Save to MariaDB
        # ======================================

        try:

            if self.is_editing:

                success, message = update_ingredient(
                    self.ingredient_id,
                    name,
                    quantity,
                    unit
                )

            else:

                success, message = add_ingredient(
                    name,
                    quantity,
                    unit
                )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

            return

        if not success:

            self.error_label.config(
                text=message
            )

            return

        messagebox.showinfo(
            "Success",
            message
        )

        self.app.show_inventory()