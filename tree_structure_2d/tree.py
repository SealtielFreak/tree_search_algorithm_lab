import typing
from collections import deque

from tree_structure_2d.point import Point
from tree_structure_2d.rect import Rect

T = typing.TypeVar("T", int, float)


def is_collision(that: Rect[T], other: Rect[T] | Point) -> bool:
    collision_aabb: typing.Callable[[Rect[T], Rect[T]], bool] = lambda a, b: (
            (a.bottom > b.top or b.top < a.bottom) and
            (a.right > b.left or a.left < b.right)
    )

    def collision_point(a: Rect[T], x: T, y: T):
        x_axis_left = x > a.left
        x_axis_right = x < a.right
        x_axis = x_axis_left and x_axis_right

        y_axis_top = y > a.top
        y_axis_bottom = y < a.bottom
        y_axis = y_axis_top and y_axis_bottom

        return x_axis and y_axis

    if isinstance(other, Rect):
        return collision_aabb(that, other)

    _x, _y, = other

    return collision_point(that, _x, _y)


def create_child(parent: Rect[T], size_limit: typing.Tuple[T, T]):
    w, h = parent.width / 2, parent.height / 2
    x, y = parent.position

    child = []

    if w >= size_limit[0] and h >= size_limit[1]:
        size = w, h

        rects = [
            Rect((x, y), size),
            Rect((x + w, y), size),
            Rect((x, y + h), size),
            Rect((x + w, y + h), size),
        ]

        for rect in rects:
            child.append(
                TreeNode(rect, size_limit)
            )

    return child


class TreeNode(typing.Generic[T]):
    def __init__(self, rect: Rect[T], size_limit=None):
        self.__rect = rect
        self.__points = deque()

        size_limit_child = size_limit if size_limit else (
            rect.size[0] / 2, rect.size[1] / 2
        )

        self.__child = create_child(
            self.__rect,
            size_limit_child
        )

    @property
    def rect(self):
        return self.__rect

    @property
    def child(self):
        return self.__child

    @property
    def points(self):
        return self.__points

    def insert_point(self, point: Point):
        if not len(self.child) > 0:
            self.points.append(point)
        else:
            for c in self.child:
                if is_collision(c.rect, point):
                    return c.insert_point(point)

    def __str__(self):
        return str(self.rect)

    def __iter__(self):
        def iter_child(child: list[TreeNode], points=None):
            if points is None:
                points = []

            for c in child:
                if len(c.child) != 0:
                    iter_child(c.child, points)
                else:
                    if len(c.points) > 0:
                        points.append(list(c.points))

            return points

        return iter(iter_child(self.child))

    def get_points_with_root(self):
        def iter_child(child: list[TreeNode], points=None):
            if points is None:
                points = []

            for c in child:
                if len(c.child) != 0:
                    iter_child(c.child, points)
                else:
                    if len(c.points) > 0:
                        points.append((c, list(c.points)))

            return points

        return list(iter_child(self.child))

    def sort(self, root=False):
        if root:
            return self.get_points_with_root()

        return list(self)


class QuadTree:
    def __init__(self, f_obj):
        self.__f_obj = f_obj
        self.__childs = deque()

    def __iter__(self):
        return iter([])
