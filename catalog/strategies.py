from catalog.loader import load_metadata

STRATEGIES = load_metadata("strategies")


def get_strategy(slug):
    return STRATEGIES.get(slug)


def get_all_strategies():
    return list(STRATEGIES.values())