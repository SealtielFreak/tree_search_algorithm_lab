import typing

T = typing.TypeVar("T", int, float)


class Point(typing.Generic[T]):
    def __init__(self, data: tuple[T, T]):
        self.x, self.y = data

    def __iter__(self) -> typing.Iterator[T]:
        return iter((self.x, self.y))

    def __getitem__(self, item):
        data = [self.x, self.y]
        return data[item]

    def __setitem__(self, key, value):
        data = [self.x, self.y]
        data[key] = value

    def __str__(self):
        return str((self.x, self.y))
