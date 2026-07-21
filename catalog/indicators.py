from catalog.loader import load_metadata

INDICATORS = load_metadata("indicators")


def get_indicator(slug):
    return INDICATORS.get(slug)


def get_all_indicators():
    return list(INDICATORS.values())