__author__ = 'roberto'

from ..shape import Shape


class Pad(Shape):
    """
    Result of pad operation.
    """
    def __init__(self, parent, cat_constructor, sketch, limit):
        super(Pad, self).__init__(parent, cat_constructor)
        self.sketch = sketch
        self.limit = limit

