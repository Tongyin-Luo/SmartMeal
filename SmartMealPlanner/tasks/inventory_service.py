from decimal import Decimal

from tasks.database import get_connection

from tasks.validation_service import validate_ingredient

from tasks.logging_service import (
    log_add,
    log_update,
    log_delete
)


# ==========================================
# Add Ingredient
# ==========================================

def add_ingredient(name, quantity, unit):

    # Validate user input
    valid, message = validate_ingredient(
        name,
        quantity,
        unit
    )

    if not valid:
        return False, message

    name = name.strip()
    quantity = Decimal(str(quantity))
    unit = unit.strip()

    # Insert ingredient into MariaDB
    with get_connection() as conn:

        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO ingredients
                (name, quantity, unit)
                VALUES (?, ?, ?)
            """, (
                name,
                quantity,
                unit
            ))

            conn.commit()

        finally:
            cursor.close()

    # Record operation
    log_add(name, quantity, unit)

    return True, "Ingredient added successfully!"


# ==========================================
# View Inventory
# ==========================================

def get_all_ingredients():

    with get_connection() as conn:

        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id, name, quantity, unit
                FROM ingredients
                ORDER BY name, id
            """)

            ingredients = cursor.fetchall()

            return ingredients

        finally:
            cursor.close()


# ==========================================
# Search Ingredients
# ==========================================

def search_ingredients(keyword):

    keyword = keyword.strip()

    with get_connection() as conn:

        cursor = conn.cursor()

        try:
            # Fetch all records and filter in Python.
            # This treats % and _ as literal search characters.
            cursor.execute("""
                SELECT id, name, quantity, unit
                FROM ingredients
                ORDER BY name, id
            """)

            ingredients = cursor.fetchall()

            return [
                ingredient
                for ingredient in ingredients
                if keyword.casefold()
                in ingredient[1].casefold()
            ]

        finally:
            cursor.close()


# ==========================================
# Get One Ingredient
# ==========================================

def get_ingredient(ingredient_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id, name, quantity, unit
                FROM ingredients
                WHERE id = ?
            """, (
                ingredient_id,
            ))

            ingredient = cursor.fetchone()

            return ingredient

        finally:
            cursor.close()


# ==========================================
# Update Ingredient
# ==========================================

def update_ingredient(
    ingredient_id,
    name,
    quantity,
    unit
):

    # Validate input
    valid, message = validate_ingredient(
        name,
        quantity,
        unit
    )

    if not valid:
        return False, message

    name = name.strip()
    quantity = Decimal(str(quantity))
    unit = unit.strip()

    with get_connection() as conn:

        cursor = conn.cursor()

        try:
            # Retrieve current quantity and lock the row
            cursor.execute("""
                SELECT quantity
                FROM ingredients
                WHERE id = ?
                FOR UPDATE
            """, (
                ingredient_id,
            ))

            old_ingredient = cursor.fetchone()

            if old_ingredient is None:
                return False, "Ingredient not found."

            old_quantity = old_ingredient[0]

            # Update ingredient
            cursor.execute("""
                UPDATE ingredients
                SET name = ?,
                    quantity = ?,
                    unit = ?
                WHERE id = ?
            """, (
                name,
                quantity,
                unit,
                ingredient_id
            ))

            conn.commit()

        finally:
            cursor.close()

    # Log changes
    log_update(
        name,
        old_quantity,
        quantity
    )

    return True, "Ingredient updated successfully!"


# ==========================================
# Delete Ingredient
# ==========================================

def delete_ingredient(ingredient_id):

    with get_connection() as conn:

        cursor = conn.cursor()

        try:
            # Retrieve ingredient before deletion
            cursor.execute("""
                SELECT name
                FROM ingredients
                WHERE id = ?
                FOR UPDATE
            """, (
                ingredient_id,
            ))

            ingredient = cursor.fetchone()

            if ingredient is None:
                return False, "Ingredient not found."

            name = ingredient[0]

            # Delete ingredient
            cursor.execute("""
                DELETE FROM ingredients
                WHERE id = ?
            """, (
                ingredient_id,
            ))

            conn.commit()

        finally:
            cursor.close()

    log_delete(name)

    return True, "Ingredient deleted successfully!"