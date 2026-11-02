def calculate_subtotal(items):
    """Return the sum of item prices."""
    return sum(items)


def calculate_total(subtotal, tax_rate=0):
    """Return the subtotal with tax applied."""
    return subtotal + (subtotal * tax_rate)


if __name__ == "__main__":
    items = [120, 80, 50]
    tax_rate = 0.05
    subtotal = calculate_subtotal(items)
    total = calculate_total(subtotal, tax_rate)

    print("Food ordering application")
    print(f"Subtotal: Rs. {subtotal:.2f}")
    print(f"Tax: Rs. {subtotal * tax_rate:.2f}")
    print(f"Total: Rs. {total:.2f}")