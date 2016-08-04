"""Test utility methods."""
import pytest
from AYABInterface.utils import sum_all, number_of_colors, next_line, \
    camel_case_to_under_score


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


class TestNextLine(object):

    """Test the next_line function.

    The behaviour of :func:`AYABInterface.utils.next_line`
    is specified in :ref:`reqline`.
    """

    @pytest.mark.parametrize("last_line,expected_next_lines", [
        (0, list(range(0, 128)) + list(range(-128, 0))),
        (30, list(range(0, 158)) + list(range(-98, 0))),
        (127, list(range(0, 255)) + [-1]),
        (128, list(range(0, 256))),
        (200, list(range(256, 328)) + list(range(72, 256))),
        (256, list(range(256, 384)) + list(range(128, 256)))])
    def test_valid_arguments(self, last_line, expected_next_lines):
        next_lines = [next_line(last_line, i) for i in range(256)]
        assert next_lines == expected_next_lines


class TestCamelCase(object):

    """Test the camel_case_to_under_score function."""

    @pytest.mark.parametrize("input,output", [
        ("A", "a"), ("AA", "a_a"), ("ACalCal", "a_cal_cal"), ("NaN", "na_n")])
    def test_conversion(self, input, output):
        assert camel_case_to_under_score(input) == output
