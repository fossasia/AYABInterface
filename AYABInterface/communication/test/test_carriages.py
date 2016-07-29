"""test the different types of supported carriages."""
from AYABInterface.communication.carriages import NullCarriage, KnitCarriage, \
    HoleCarriage, UnknownCarriage, id_to_carriage_type
import pytest
from test_assertions import assert_identify


@pytest.mark.parametrize("carriage_type,tests", [
    (NullCarriage, []), (KnitCarriage, ["is_knit_carriage"]),
    (HoleCarriage, ["is_hole_carriage"]),
    (UnknownCarriage, ["is_unknown_carriage"])])
def test_carriage_tests(carriage_type, tests):
    assert_identify(carriage_type(0), tests)


@pytest.mark.parametrize("carriage_id,tests", [
    (0, []), (1, ["is_knit_carriage"]), (2, ["is_hole_carriage"]),
    (3, ["is_unknown_carriage"]), (8, ["is_unknown_carriage"])])
def test_creation_from_id(carriage_id, tests):
    assert_identify(id_to_carriage_type(carriage_id)(0), tests)


@pytest.mark.parametrize("carriage_type", [
    NullCarriage, KnitCarriage, HoleCarriage, UnknownCarriage])
@pytest.mark.parametrize("needle_position", [1, 4, 55, 199])
def test_needle_position(carriage_type, needle_position):
    assert carriage_type(needle_position).needle_position == needle_position
