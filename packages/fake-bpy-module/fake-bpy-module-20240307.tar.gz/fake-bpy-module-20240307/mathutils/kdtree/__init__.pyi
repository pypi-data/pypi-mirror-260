import typing
import mathutils

GenericType = typing.TypeVar("GenericType")

class KDTree:
    """KdTree(size) -> new kd-tree initialized to hold size items."""

    def balance(self):
        """Balance the tree."""
        ...

    def find(
        self,
        co: typing.Union["mathutils.Vector", typing.Sequence[float]],
        filter: typing.Callable = None,
    ) -> typing.Tuple:
        """Find nearest point to co.

        :param co: 3d coordinates.
        :type co: typing.Union['mathutils.Vector', typing.Sequence[float]]
        :param filter: function which takes an index and returns True for indices to include in the search.
        :type filter: typing.Callable
        :rtype: typing.Tuple
        :return: Returns (`Vector`, index, distance).
        """
        ...

    def find_n(
        self, co: typing.Union["mathutils.Vector", typing.Sequence[float]], n: int
    ) -> typing.List:
        """Find nearest n points to co.

        :param co: 3d coordinates.
        :type co: typing.Union['mathutils.Vector', typing.Sequence[float]]
        :param n: Number of points to find.
        :type n: int
        :rtype: typing.List
        :return: Returns a list of tuples (`Vector`, index, distance).
        """
        ...

    def find_range(
        self,
        co: typing.Union["mathutils.Vector", typing.Sequence[float]],
        radius: float,
    ) -> typing.List:
        """Find all points within radius of co.

        :param co: 3d coordinates.
        :type co: typing.Union['mathutils.Vector', typing.Sequence[float]]
        :param radius: Distance to search for points.
        :type radius: float
        :rtype: typing.List
        :return: Returns a list of tuples (`Vector`, index, distance).
        """
        ...

    def insert(
        self, co: typing.Union["mathutils.Vector", typing.Sequence[float]], index: int
    ):
        """Insert a point into the KDTree.

        :param co: Point 3d position.
        :type co: typing.Union['mathutils.Vector', typing.Sequence[float]]
        :param index: The index of the point.
        :type index: int
        """
        ...

    def __init__(self, size) -> typing.Any:
        """

        :rtype: typing.Any
        """
        ...
