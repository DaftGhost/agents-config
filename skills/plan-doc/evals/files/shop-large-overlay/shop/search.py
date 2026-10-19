def search(catalog, term):
    return [s for s in catalog if term.lower() in s.lower()]
