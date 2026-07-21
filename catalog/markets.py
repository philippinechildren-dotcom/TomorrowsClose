from catalog.loader import load_metadata

MARKETS = load_metadata("markets")


def get_market(slug):
    return MARKETS.get(slug)


def get_all_markets():
    return list(MARKETS.values())