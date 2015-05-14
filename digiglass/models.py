"""Python representations of Digi-Key stuff."""


class Category:
    """A Digi-Key product category."""
    def __init__(self, id, name, parent, qty):
        self.id = id
        self.name = name
        self.parent = parent
        self.qty = int(qty)

    def __repr__(self):
        return ('<Category {}: {} - {} ({} items)>'
                .format(self.id, self.parent, self.name, self.qty))
