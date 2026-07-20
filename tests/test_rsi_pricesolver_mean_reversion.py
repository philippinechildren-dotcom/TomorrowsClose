"""
Tests for RSI PriceSolver Mean Reversion Strategy
"""

from strategies.rsi_pricesolver_mean_reversion import (
    evaluate_rsi_pricesolver_mean_reversion,
)


def test_price_below_trigger_is_long():
    """
    When current price is below the RSI trigger price,
    the oversold condition is active and the strategy is LONG.
    """

    result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=695.33,
        trigger_price=699.05,
    )

    assert result["status"] == "LONG"
    assert result["signal"] == "ENTRY_ACTIVE"
    assert result["current_price"] == 695.33
    assert result["trigger_price"] == 699.05


def test_price_above_trigger_is_flat():
    """
    When current price is above the RSI trigger price,
    the strategy is waiting for the oversold entry condition.
    """

    result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=710.00,
        trigger_price=699.05,
    )

    assert result["status"] == "FLAT"
    assert result["signal"] == "WAITING_FOR_ENTRY"
    assert result["current_price"] == 710.00
    assert result["trigger_price"] == 699.05


def test_price_equal_trigger_is_flat():
    """
    Equal price does not activate the oversold condition.

    The RSI threshold is active only when price closes below
    the calculated trigger price.
    """

    result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=699.05,
        trigger_price=699.05,
    )

    assert result["status"] == "FLAT"
    assert result["signal"] == "WAITING_FOR_ENTRY"


def test_qqq_real_world_example():
    """
    Validated QQQ example.

    QQQ close:
        695.33

    RSI(3):
        15.6981

    RSI threshold:
        30

    RSI PriceSolver:
        699.0468393412632

    Since the current price is below the RSI threshold price,
    the mean reversion condition is active.
    """

    result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=695.33,
        trigger_price=699.0468393412632,
    )

    assert result["status"] == "LONG"
    assert result["signal"] == "ENTRY_ACTIVE"
    assert result["current_price"] == 695.33
    assert result["trigger_price"] == 699.0468393412632