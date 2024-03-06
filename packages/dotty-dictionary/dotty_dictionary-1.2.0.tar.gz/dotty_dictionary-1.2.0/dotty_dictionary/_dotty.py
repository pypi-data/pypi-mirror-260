from collections.abc import MutableMapping
from ._dotty_dictionary import Dotty


def dotty(
    dictionary: MutableMapping = None,
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
    return Dotty(
        dictionary,
        separator=".",
        esc_char="\\",
        no_list=no_list,
    )
