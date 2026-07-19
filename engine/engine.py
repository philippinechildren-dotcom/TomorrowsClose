"""
engine/engine.py

Tomorrow's Close Engine

The engine coordinates the flow of information between the
market data layer, indicator solvers, strategy solvers,
and presentation layer.

It performs no indicator calculations itself.
"""

from market_data.provider import get_market_data


def process_request(ticker):
    """
    Process a request for market data.

    Parameters
    ----------
    ticker : str

    Returns
    -------
    dict
    """

    market_data = get_market_data(ticker)

    return market_data


if __name__ == "__main__":

    result = process_request("QQQ")

    print(result)
