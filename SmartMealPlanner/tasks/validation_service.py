from decimal import Decimal, InvalidOperation


# Validate ingredient information
def validate_ingredient(name, quantity, unit):

    # Validate ingredient name
    if not isinstance(name, str):
        return False, "Ingredient name must be text."

    name = name.strip()

    if not name:
        return False, "Ingredient name cannot be empty."

    if len(name) > 255:
        return False, "Ingredient name is too long."

    # Validate unit
    if not isinstance(unit, str):
        return False, "Invalid unit."

    unit = unit.strip()

    if not unit:
        return False, "Please select a unit."

    if len(unit) > 30:
        return False, "Unit is too long."

    # Validate quantity
    try:
        quantity = Decimal(str(quantity))

    except (InvalidOperation, ValueError, TypeError):
        return False, "Quantity must be a number."

    if not quantity.is_finite():
        return False, "Quantity must be a finite number."

    if quantity < 0:
        return False, "Quantity cannot be negative."

    if quantity > Decimal("999999999.999"):
        return False, "Quantity is too large."

    if quantity.as_tuple().exponent < -3:
        return False, "Quantity supports up to 3 decimal places."

    return True, ""