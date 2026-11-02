def calculate_order_total(items, discount_percent=0):
    """Return the order total after applying a percentage discount."""
    if not isinstance(items, (list, tuple)) or any(
        not isinstance(price, (int, float)) or isinstance(price, bool) or price < 0
        for price in items
    ):
        raise ValueError("items must contain only non-negative numbers")

    if (
        not isinstance(discount_percent, (int, float))
        or isinstance(discount_percent, bool)
        or not 0 <= discount_percent <= 100
    ):
        raise ValueError("discount_percent must be between 0 and 100")

    subtotal = sum(items)
    return round(subtotal * (1 - discount_percent / 100), 2)
