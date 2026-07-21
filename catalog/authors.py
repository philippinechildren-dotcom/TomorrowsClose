from catalog.loader import load_metadata

AUTHORS = load_metadata("authors")


def get_author(slug):
    return AUTHORS.get(slug)


def get_all_authors():
    return list(AUTHORS.values())