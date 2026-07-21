from catalog.loader import load_metadata

TAGS = load_metadata("tags")


def get_tag(slug):
    return TAGS.get(slug)


def get_all_tags():
    return list(TAGS.values())