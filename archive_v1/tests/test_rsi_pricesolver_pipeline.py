"""
Integration test for RSI PriceSolver Mean Reversion pipeline.

Flow tested:

Market data values
        ↓
RSI PriceSolver output
        ↓
Mean Reversion Strategy
        ↓
Signal Formatter
"""

from strategies.rsi_pricesolver_mean_reversion import (
    evaluate_rsi_pricesolver_mean_reversion,
)

from presentation.signal_formatter import (
    format_rsi_pricesolver_signal,
)


def test_rsi_pricesolver_mean_reversion_pipeline():
    """
    Validated QQQ example:

    Close:
        695.33

    RSI(3):
        15.6981

    RSI Threshold:
        30

    PriceSolver:
        699.0468393412632

    Since price is below the trigger,
    the strategy should be LONG.
    """

    # Values produced by previous layers
    current_price = 695.33
    trigger_price = 699.0468393412632

    # Strategy layer
    strategy_result = evaluate_rsi_pricesolver_mean_reversion(
        current_price=current_price,
        trigger_price=trigger_price,
    )

    assert strategy_result["status"] == "LONG"
    assert strategy_result["signal"] == "ENTRY_ACTIVE"

    # Presentation layer
    formatted_result = format_rsi_pricesolver_signal(
        strategy_result
    )

    assert formatted_result["headline"] == "Current Status: Long"
    assert formatted_result["message"] == "Oversold condition is active."
    assert formatted_result["trigger_price"] == trigger_price