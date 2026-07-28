from catalog.strategies import get_strategy


def get_defaults(ticker):

    strategy = get_strategy("rsi-pricesolver")

    return strategy["default_parameters"][ticker]