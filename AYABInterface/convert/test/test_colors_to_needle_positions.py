import pytest
from AYABInterface.convert import colors_to_needle_positions


class TestColorsToBinary(object):

    """Test :func:`AYABInterface.convert.colors_to_needle_positions`."""

    @pytest.mark.parametrize("rows,expected_needles", [
        [[[0, 0, 0, 0]], [[([0, 0, 0, 0], (0,), False)]]],  # single color
        [[[1, 2, 1, 2]], [[([0, 1, 0, 1], (1, 2), True)]]],  # two colors
        [[[1, 2, 0, 2]], [[([0, 1, 1, 1], (1,), False),  # three colors
                           ([1, 0, 1, 0], (2,), False),
                           ([1, 1, 0, 1], (0,), False)]]]])
    def test_conversion(self, rows, expected_needles):
        needles = colors_to_needle_positions(rows)
        assert needles == expected_needles

    def test_attributes(self):
        needles = colors_to_needle_positions([[0, 0]])
        row = needles[0][0]
        assert row[0] == row.needle_coloring
        assert row[1] == row.colors
        assert row[2] == row.two_colors
