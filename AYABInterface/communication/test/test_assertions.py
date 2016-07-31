"""Special assertions for tests."""


def assert_identify(message, expected_true=[]):
    """Make sure the messages "is_*" are True or False."""
    true = set()
    false = set()
    expected_false = set()
    expected_true = set(expected_true)
    for method_name in dir(message):
        if method_name.startswith("is_"):
            test_method = getattr(message, method_name)
            result = test_method()
            if method_name not in expected_true:
                expected_false.add(method_name)
            if result is True:
                true.add(method_name)
            if result is False:
                false.add(method_name)
    assert false == expected_false, "Methods return False"
    assert true == expected_true, "Methods return True"

__all__ = ["assert_identify"]
