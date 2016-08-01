"""test the NeedlePositionCache."""
from AYABInterface.communication.cache import NeedlePositionCache
import AYABInterface.communication.cache as needle_position_cache
from unittest.mock import Mock, call
import pytest
from pytest import fixture
import crc8


@fixture
def get_line():
    return Mock()


@fixture
def machine():
    return Mock()


@fixture
def cache(get_line, machine):
    return NeedlePositionCache(get_line, machine)


class TestGet(object):

    @pytest.mark.parametrize("line_number", [3, 5, 7])
    def test_get(self, line_number, get_line, cache):
        assert cache.get(line_number) == get_line.return_value
        get_line.assert_called_once_with(line_number)

    def test_cache(self, get_line, cache):
        get_line.return_value = "a"
        a = cache.get(1)
        get_line.return_value = "b"
        b = cache.get(2)
        get_line.assert_has_calls([call(1), call(2)])
        get_line.return_value = "c"
        c = cache.get(1)
        get_line.return_value = "d"
        d = cache.get(2)
        assert a == c
        assert b == d
        get_line.assert_has_calls([call(1), call(2)])


class TestLastLine(object):

    """Test the is_last test."""

    @pytest.mark.parametrize("number", [1, 4, 8])
    @pytest.mark.parametrize("line,truth", [([], False), (None, True)])
    def test_last(self, get_line, cache, number, line, truth):
        get_line.return_value = line
        assert cache.is_last(number) == truth
        get_line.assert_called_once_with(number + 1)

    @pytest.mark.parametrize("last", [True, False])
    def test_cached(self, get_line, cache, last):
        get_line.return_value = (None if last else [])
        assert cache.get(1) is get_line.return_value
        get_line.return_value = []
        assert cache.is_last(0) == last


class TestGetLineBytes(object):

    """Test the get_bytes method.

    .. seealso::
        :meth:`AYABInterface.cache.Commmunication.get_line_bytes`
    """

    @pytest.mark.parametrize("line", [1, -123, 10000])
    def test_get_line(self, cache, get_line, line, machine):
        line_bytes = cache.get_bytes(line)
        get_line.assert_called_with(line)
        machine.needle_positions_to_bytes.assert_called_with(
            get_line.return_value)
        assert line_bytes == machine.needle_positions_to_bytes.return_value

    @pytest.mark.parametrize("line", [4, -89])
    def test_line_is_cached(self, cache, get_line, line, machine):
        cache.get_bytes(line)
        cached_value = machine.needle_positions_to_bytes.return_value
        machine.needle_positions_to_bytes.return_value = None
        line_bytes = cache.get_bytes(line)
        assert line_bytes == cached_value

    @pytest.mark.parametrize("line", [55, 4])
    @pytest.mark.parametrize("added", [-1, 1, 12, -2])
    def test_cache_works_only_for_specific_line(
            self, cache, get_line, line, machine, added):
        cache.get_bytes(line)
        machine.needle_positions_to_bytes.return_value = None
        line_bytes = cache.get_bytes(line + added)
        assert line_bytes is None

    @pytest.mark.parametrize("line", [55, 4])
    def test_line_is_not_known(self, cache, get_line, machine, line):
        get_line.return_value = None
        assert cache.get_bytes(line) is None
        machine.needle_positions_to_bytes.assert_not_called()


class TestLineConfigurationMessage(object):

    """Test get_line_configuration_message."""

    @pytest.mark.parametrize("machine_bytes", [
        b'\x00' * 20, b'asdasdasdas', b'\x97'])
    @pytest.mark.parametrize("last_line", [True, False])
    @pytest.mark.parametrize("line_number", [0, 1, 267, -33])
    def test_get_normal_line(self, cache, machine, machine_bytes, last_line,
                             get_line, line_number):
        if last_line:
            get_line.return_value = None
            assert cache.get(line_number + 1) is None
        get_line.return_value = []
        is_last = cache.is_last(line_number)
        assert is_last == last_line
        machine.needle_positions_to_bytes.return_value = machine_bytes
        expected_line_bytes = bytes([line_number & 255]) + \
            machine_bytes + bytes([last_line])
        expected_line_bytes += crc8.crc8(expected_line_bytes).digest()
        line_bytes = cache.get_line_configuration_message(line_number)
        assert line_bytes == expected_line_bytes

    @pytest.mark.parametrize("line", [1, 4, 88])
    def test_cache_crc(self, monkeypatch, cache, machine, line):
        get_line.return_value = []
        machine.needle_positions_to_bytes.return_value = b'123'
        line_bytes = cache.get_line_configuration_message(line)
        monkeypatch.setattr(needle_position_cache, "crc8", Mock())
        cached_line_bytes = cache.get_line_configuration_message(line)
        assert line_bytes == cached_line_bytes

    @pytest.mark.parametrize("line_number", [111, 1111, 0, -12])
    def test_get_nonexistent_line(self, cache, get_line, line_number):
        get_line.return_value = None
        empty_last_line = bytes([line_number & 255]) + \
            b"\x00" * 25 + b'\x01'  # last line flag
        empty_last_line += crc8.crc8(empty_last_line).digest()
        line = cache.get_line_configuration_message(line_number)
        assert line == empty_last_line
