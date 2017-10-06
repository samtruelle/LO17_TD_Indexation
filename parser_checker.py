from bulletins_to_xml import parse_bulletins


def get_available_rubriques():
    yield from {bulletin.rubrique for bulletin in parse_bulletins('./BULLETINS.zip')}


def get_available_titles():
    yield from {bulletin.titre for bulletin in parse_bulletins('./BULLETINS.zip')}


if __name__ == "__main__":
    print("Rubriques:")
    print(sorted(list(get_available_rubriques())))
    print("Titres de bulletins:")
    print(sorted(list(get_available_titles())))
