"""Utility methods."""


def sum_all(iterable, start):
    """Sum up an iterable starting with a start value.

    In contrast to :func:`sum`, this also works on other types like
    :class:`lists <list>` and :class:`sets <set>`.
    """
    if hasattr(start, "__add__"):
        for value in iterable:
            start += value
    else:
        for value in iterable:
            start |= value
    return start


def number_of_colors(rows):
    """Determine the numer of colors in the rows.

    :rtype: int
    """
    return len(sum_all(map(set, rows), set()))


def next_line(last_line, next_line_8bit):
    """Compute the next line based on the last line and a 8bit next line.

    The behaviour of the function is specified in :ref:`reqline`.

    :param int last_line: the last line that was processed
    :param int next_line_8bit: the lower 8 bits of the next line
    :return: the next line closest to :paramref:`last_line`

    .. seealso:: :ref:`reqline`
    """
    # compute the line without the lowest byte
    base_line = last_line - (last_line & 255)
    # compute the three different lines
    line = base_line + next_line_8bit
    lower_line = line - 256
    upper_line = line + 256
    # compute the next line
    if last_line - lower_line <= line - last_line:
        return lower_line
    if upper_line - last_line < last_line - line:
        return upper_line
    return line


def camel_case_to_under_score(camel_case_name):
    """Return the underscore name of a camel case name.

    :param str camel_case_name: a name in camel case such as
      ``"ACamelCaseName"``
    :return: the name using underscores, e.g. ``"a_camel_case_name"``
    :rtype: str
    """
    result = []
    for letter in camel_case_name:
        if letter.lower() != letter:
            result.append("_" + letter.lower())
        else:
            result.append(letter.lower())
    if result[0].startswith("_"):
        result[0] = result[0][1:]
    return "".join(result)

__all__ = ["sum_all", "number_of_colors", "next_line",
           "camel_case_to_under_score"]
