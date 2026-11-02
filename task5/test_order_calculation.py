import pytest

from order_calculation import calculate_order_total


@pytest.mark.parametrize(
    ("items", "discount_percent", "expected"),
    [
        ([100, 50], 10, 135.0),
        ([], 20, 0.0),
        ([80, 20], 100, 0.0),
    ],
)
def test_calculate_order_total_valid_inputs(items, discount_percent, expected):
    assert calculate_order_total(items, discount_percent) == expected


@pytest.mark.parametrize(
    ("items", "discount_percent"),
    [
        ([-10, 20], 10),
        ([100, 50], 101),
    ],
)
def test_calculate_order_total_invalid_inputs(items, discount_percent):
    with pytest.raises(ValueError):
        calculate_order_total(items, discount_percent)
