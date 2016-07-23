"""Test utility methods."""
import pytest
from AYABInterface.utils import sum_all, number_of_colors


class TestSumAll(object):

    """Test :func:`AYABInterface.utils.sum_all`."""

    def test_integers(self):
        """Sum up :class:`integers <int>`."""
        assert sum_all([1, 2, 3, 4], 2) == 12

    def test_lists(self):
        """Sum up :class:`lists <list>`."""
        assert sum_all([[1], [2, 3], [4]], [9]) == [9, 1, 2, 3, 4]

    def test_sets(self):
        """Sum up :class:`sets <set>`."""
        assert sum_all(map(set, [[1, 2], [3, 5], [3, 1]]), set([0, 5])) == \
            set([0, 1, 2, 3, 5])


class TestNumberOfColors(object):

    """Test :func:`AYABInterface.utils.number_of_colors`."""

    @pytest.mark.parametrize("colors,number", [
        [[[1, 2, 3], [2, 3, 3, 3], [2, 2, 2], [0]], 4],
        [[[], [], []], 0], [[[1, 1, 1], ["", "q"], ["asd"]], 4]])
    def test_number_of_colors(self, colors, number):
        """Test different inputs."""
        assert number_of_colors(colors) == number

