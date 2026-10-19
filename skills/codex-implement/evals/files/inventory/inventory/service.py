from .models import Item


class Inventory:
    def __init__(self, items=None):
        self._items = list(items or [])

    def all(self):
        return list(self._items)

    def add(self, item):
        self._items.append(item)

    def find(self, sku):
        for item in self._items:
            if item.sku == sku:
                return item
        return None
