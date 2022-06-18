import pytest
from unittest.mock import patch

from main import compare


@pytest.mark.parametrize('trade, price, comparison, result',
                         [('btcusdt', 30000, ('more', 60000), False), ('ethbtc', 0.09, ('less', 0.07), False),
                          ('dotusdt', 10, ('more_eq', 40), False), ('ethusdt', 5000, ('less_eq', 4000), False)])
def test_compare_false(trade, price, comparison, result):
    assert compare(trade, price, comparison) == result


@patch('main.send_message')
def test_compare_true_more(send_message):
    assert compare('btcusdt', 70000, ('more', 60000)) is True


@patch('main.send_message')
def test_compare_true_less(send_message):
    assert compare('ethbtc', 0.06, ('less', 0.07)) is True


@patch('main.send_message')
def test_compare_true_more_eq(send_message):
    assert compare('dotusdt', 40, ('more_eq', 40)) is True


@patch('main.send_message')
def test_compare_true_less_eq(send_message):
    assert compare('ethusdt', 4000, ('less_eq', 4000)) is True
