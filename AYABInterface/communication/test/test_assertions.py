"""Special assertions for tests."""


def assert_identify(message, expected_true=[]):
    """Make sure the messages "is_*" are True or False."""
    true = set()
    expected_true = set(expected_true)
    for method_name in dir(message):
        if method_name.startswith("is_"):
            test_method = getattr(message, method_name)
            if test_method():
                true.add(method_name)
    assert true == expected_true

__all__ = ["assert_identify"]
