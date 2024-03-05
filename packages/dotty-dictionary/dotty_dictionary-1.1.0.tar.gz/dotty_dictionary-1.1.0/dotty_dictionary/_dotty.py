from collections.abc import Mapping
from ._dotty_dictionary import Dotty


def dotty(
    dictionary: Mapping = None,
    no_list: bool = False,
) -> Dotty:
    """Factory function for Dotty class.

    Create Dotty wrapper around existing or new dictionary.

    Parameters:
        dictionary: Any dictionary or dict-like object
        no_list: If set to True then numeric keys will NOT be converted to list indices

    Returns:
        Dotty instance
    """
    if dictionary is None:
        dictionary = {}
    return Dotty(dictionary, separator=".", esc_char="\\", no_list=no_list)
