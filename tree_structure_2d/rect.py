import typing

T = typing.TypeVar("T", int, float)


class Rect(typing.Generic[T]):
    def __init__(self, position: typing.Tuple[T, T], size: typing.Tuple[T, T]):
        self.position = position
        self.size = size

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def right(self):
        return self.position[0] + self.width

    @property
    def left(self):
        return self.position[0]

    @property
    def top(self):
        return self.position[1]

    @property
    def bottom(self):
        return self.position[1] + self.height

    def __str__(self):
        x, y = self.position

        return f"[{x}, {y}, {self.right}, {self.bottom}]"

    def __iter__(self):
        x, y = self.position

        return iter((x, y, self.right, self.bottom))
