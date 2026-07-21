from catalog.loader import load_metadata

CATEGORIES = load_metadata("categories")


def get_category(slug):
    return CATEGORIES.get(slug)


def get_all_categories():
    return list(CATEGORIES.values())