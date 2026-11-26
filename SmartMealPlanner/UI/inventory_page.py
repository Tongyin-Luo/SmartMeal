import tkinter as tk
from tkinter import ttk, messagebox

from UI.styles import (
    BG,
    WHITE,
    GREEN,
    DARK_GREEN,
    LIGHT_GREEN,
    TEXT,
    GRAY,
    FONT
)

from tasks.inventory_service import (
    get_all_ingredients,
    search_ingredients
)


class InventoryPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)

        self.app = app

        # ======================================
        # Configure Entry Style
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
        # Page Title
        # ======================================

        tk.Label(
            self,
            text="My Inventory",
            font=(FONT, 26, "bold"),
            bg=BG,
            fg=DARK_GREEN
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        # ======================================
        # IH#1: Explain Benefits
        # ======================================

        tk.Label(
            self,
            text=(
                "Keep track of your ingredients "
                "to reduce food waste."
            ),
            font=(FONT, 11),
            bg=BG,
            fg=GRAY,
            wraplength=350,
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 12)
        )

        # ======================================
        # IH#2: Explain Costs
        # ======================================

        tk.Label(
            self,
            text=(
                "Reminder: Update ingredient quantities "
                "manually after using food."
            ),
            font=(FONT, 10),
            bg=LIGHT_GREEN,
            fg=DARK_GREEN,
            wraplength=350,
            justify="left",
            padx=12,
            pady=12
        ).pack(
            fill="x",
            padx=25,
            pady=(0, 18)
        )

        # ======================================
        # IH#7: Search Ingredients
        # ======================================

        tk.Label(
            self,
            text="Search Ingredients",
            font=(FONT, 11, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 8)
        )

        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(
            self,
            textvariable=self.search_var,
            font=(FONT, 12),
            style="SmartMeal.TEntry"
        )

        self.search_entry.pack(
            fill="x",
            padx=25,
            ipady=5,
            pady=(0, 15)
        )

        self.search_var.trace_add(
            "write",
            lambda *_: self.refresh_inventory()
        )

        # ======================================
        # Browse Inventory
        # ======================================

        self.count_label = tk.Label(
            self,
            text="Browse All Ingredients",
            font=(FONT, 12, "bold"),
            bg=BG,
            fg=DARK_GREEN
        )

        self.count_label.pack(
            anchor="w",
            padx=25,
            pady=(0, 10)
        )

        # ======================================
        # Scrollable Inventory
        # ======================================

        list_container = tk.Frame(
            self,
            bg=BG
        )

        list_container.pack(
            fill="both",
            expand=True,
            padx=25
        )

        self.canvas = tk.Canvas(
            list_container,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        scrollbar = ttk.Scrollbar(
            list_container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.inventory_frame = tk.Frame(
            self.canvas,
            bg=BG
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.inventory_frame,
            anchor="nw"
        )

        self.inventory_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_inventory_frame
        )

        # ======================================
        # Add Ingredient Button
        # ======================================

        self.create_button(
            text="+ Add Ingredient",
            command=self.app.show_add_ingredient,
            background=DARK_GREEN,
            foreground=WHITE
        )

        self.refresh_inventory()

    # ==========================================
    # Scroll Region
    # ==========================================

    def update_scroll_region(self, event):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_inventory_frame(self, event):

        self.canvas.itemconfigure(
            self.canvas_window,
            width=event.width
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
    # Refresh Inventory
    # ==========================================

    def refresh_inventory(self):

        for widget in self.inventory_frame.winfo_children():
            widget.destroy()

        keyword = self.search_var.get().strip()

        try:

            if keyword:
                ingredients = search_ingredients(keyword)
            else:
                ingredients = get_all_ingredients()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )
            return

        # Display number of records
        self.count_label.config(
            text=f"Browse Ingredients ({len(ingredients)})"
        )

        if not ingredients:

            tk.Label(
                self.inventory_frame,
                text="No ingredients found.",
                font=(FONT, 12),
                bg=BG,
                fg=GRAY
            ).pack(pady=25)

            return

        # ======================================
        # Ingredient Cards
        # ======================================

        for ingredient in ingredients:

            ingredient_id, name, quantity, unit = ingredient

            card = tk.Frame(
                self.inventory_frame,
                bg=WHITE
            )

            card.pack(
                fill="x",
                pady=6
            )

            tk.Label(
                card,
                text=name,
                font=(FONT, 13, "bold"),
                bg=WHITE,
                fg=TEXT
            ).pack(
                anchor="w",
                padx=15,
                pady=(12, 3)
            )

            tk.Label(
                card,
                text=f"{self.format_quantity(quantity)} {unit}",
                font=(FONT, 11),
                bg=WHITE,
                fg=GRAY
            ).pack(
                anchor="w",
                padx=15,
                pady=(0, 12)
            )

            # Edit button without black background
            edit_button = tk.Label(
                card,
                text="Edit →",
                font=(FONT, 11),
                bg=WHITE,
                fg=DARK_GREEN,
                cursor="hand2"
            )

            edit_button.pack(
                anchor="e",
                padx=15,
                pady=(0, 10)
            )

            edit_button.bind(
                "<Button-1>",
                lambda event, i=ingredient_id:
                    self.app.show_update_ingredient(i)
            )

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
            pady=18
        )

        button_label = tk.Label(
            button_frame,
            text=text,
            font=(FONT, 13, "bold"),
            bg=background,
            fg=foreground,
            pady=15,
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