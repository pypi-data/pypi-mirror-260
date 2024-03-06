import json
from typing import Any, Iterable
from ._dotty_encoder import DottyEncoder

__authors__ = ["Joseph Hwang", "Pawel Zadrozny"]
__copyright__ = "Copyright (c) 2024, Joseph Hwang. Originally written by Pawel Zadrozny"


class Dotty:
    """Dictionary object wrapper with dot notation access.

    Dotty wraps dictionary and provides proxy for quick accessing to deeply
    nested keys and values using dot notation.

    Dot notation can be customize in special cases. Let's say dot character
    has special meaning, and you want to use other character for accessing
    deep keys.

    Dotty does not copy original dictionary but it operates on it.
    All changes made in original dictionary are reflected in dotty wrapped dict
    and vice versa.

    Parameters:
        dictionary (Any): Any dictionary or dict-like object
        separator (str): Character used to chain deep access.
        esc_char (str): Escape character for separator.
        no_list (bool): If set to True then numeric keys will NOT be converted to list indices
    """

    def __init__(
        self,
        dictionary: dict[str, Any],
        separator: str = ".",
        esc_char: str = "\\",
        no_list: bool = False,
    ):
        if not isinstance(dictionary, dict):
            raise AttributeError("Dictionary must be type of dict")
        else:
            self._data: dict[str, Any] = dictionary
        self.separator = separator
        self.esc_char = esc_char
        self.no_list = no_list

    def __repr__(self):
        return (
            f"Dotty(dictionary={self._data}), "
            f"separator={repr(self.separator)}, "
            f"esc_char={repr(self.esc_char)})"
        )

    def __str__(self):
        return str(self._data)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other: dict):
        try:
            return sorted(self._data.items()) == sorted(other.items())
        except AttributeError:
            return False

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def __contains__(self, item):
        def search_in(items: list[str], data: dict) -> bool:
            """Recursively search for deep key in dict.

            Parameters:
                items: List of dictionary keys
                data: Portion of dictionary to operate on

            Returns:
                bool: Predicate of key existence
            """
            key = items.pop(0)
            if key.isdigit():
                idx = int(key)
                if idx < len(data):
                    if items:
                        return search_in(items, data[idx])
                    else:
                        return data[idx]
                else:
                    return False

            if items and key in data:
                return search_in(items, data[key])
            return key in data

        return search_in(self._split(item), self._data)

    def __getitem__(self, item):
        def get_from(items: list[str], data: dict) -> Any:
            """Recursively get value from dictionary deep key.

            Parameters:
                items: List of dictionary keys
                data: Portion of dictionary to operate on

            Returns:
                Value from dictionary

            Raises:
                KeyError: If key does not exist
            """
            key = items.pop(0)
            if isinstance(data, list) and key.isdigit() and not self.no_list:
                key = int(key)
            elif key not in data and isinstance(data, dict):
                key = self._find_data_type(key, data)
            elif isinstance(data, list) and ":" in key and not self.no_list:
                # TODO: fix C417 Unnecessary use of map - use a generator expression instead.
                list_slice = slice(
                    *map(lambda x: None if x == "" else int(x), key.split(":"))
                )  # noqa: C417
                if items:
                    return [get_from(items.copy(), x) for x in data[list_slice]]
                else:
                    return data[list_slice]
            try:
                data = data[key]
            except TypeError:
                raise KeyError("List index must be an integer, got {}".format(key))
            if items and data is not None:
                return get_from(items, data)
            else:
                return data

        return get_from(self._split(item), self._data)

    def __setitem__(self, key, value):
        def set_to(items: list[str], data: dict):
            """Recursively set value to dictionary deep key.

            Parameters:
                items: List of dictionary keys
                data: Portion of dictionary to operate on
            """
            key = items.pop(0)
            if items:
                if items[0].isdigit():
                    next_item = []
                else:
                    next_item = {}

                if key.isdigit():
                    key = int(key)
                    try:
                        if not data[key]:
                            data[key] = next_item
                    except IndexError:
                        self.set_list_index(data, key, next_item)
                    set_to(items, data[key])
                else:
                    if not data.get(key):
                        data[key] = next_item
                    set_to(items, data[key])

            else:
                if key.isdigit():
                    self.set_list_index(data, key, value)
                else:
                    data[key] = value

        set_to(self._split(key), self._data)

    def __delitem__(self, key):
        def del_key(items: list[str], data: dict):
            """Recursively remove deep key from dict.

            Parameters:
                items: List of dictionary keys
                data: Portion of dictionary to operate on

            Raises:
                KeyError: If key does not exist
            """
            key = items.pop(0)
            if key.isdigit():
                key = int(key)
            if items:
                del_key(items, data[key])
            else:
                del data[key]

        del_key(self._split(key), self._data)

    def copy(self) -> "Dotty":
        """Returns a shallow copy of dictionary wrapped in Dotty.

        Returns:
            Shallow copy of wrapped dictionary
        """
        return Dotty(
            self._data.copy(),
            self.separator,
            self.esc_char,
            self.no_list,
        )

    @staticmethod
    def empty(*args, **kwargs) -> "Dotty":
        """Create empty Dotty instance.

        Returns:
            Empty Dotty instance
        """
        return Dotty({}, *args, **kwargs)

    @staticmethod
    def from_flat_dict(data: dict, *args, **kwargs) -> "Dotty":
        """Create Dotty instance from flat dictionary.

        Parameters:
            data: Flat dictionary
            separator: Character used to chain deep access

        Returns:
            Dotty instance
        """
        dotty = Dotty({}, *args, **kwargs)
        for k, v in data.items():
            dotty[k] = v
        return dotty

    @staticmethod
    def fromkeys(seq: Iterable[str], value: Any = None) -> "Dotty":
        """Create a new dictionary with keys from seq and values set to value.

        New created dictionary is wrapped in Dotty.

        Parameters:
            seq: Sequence of elements which is to be used as keys for the new dictionary
            value: Value which is set to each element of the dictionary

        Returns:
            Dotty instance
        """
        return Dotty(dict.fromkeys(seq, value))

    @staticmethod
    def set_list_index(
        data: list,
        index: int | str,
        value: Any,
    ):
        """Set value in list at specified index.
        All the values before target index should stay unchanged
        or be filled with None.

        Parameters:
            data: List where value should be set
            index: String or Int of target index
            value: Target value to put under index
        """
        for _ in range(len(data), int(index) + 1):
            data.append(None)
        else:
            data[int(index)] = value

    def clear(self):
        self._data.clear()

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from deep key or default if key does not exist.

        This method match 1:1 with dict .get method except that it
        accepts deeply nested key with dot notation.

        Parameters:
            key: Single key or chain of keys
            default: Default value if deep key does not exist

        Returns:
            Any or default value
        """
        try:
            return self.__getitem__(key)
        except (KeyError, IndexError):
            return default

    def keys(self):
        """Returns the keys of the category structure.

        Returns:
            The keys of the category structure.
        """
        return self._data.keys()

    def items(self):
        """Returns the items of the category structure.

        Returns:
            The items of the category structure.
        """
        return self._data.items()

    def pop(self, key: str, default: Any = None) -> Any:
        """Pop key from Dotty.

        This method match 1:1 with dict .pop method except that
        it accepts deeply nested key with dot notation.

        Parameters:
            key: Single key or chain of keys
            default: If default is provided will be returned

        Returns:
            Any or default value

        Raises:
            KeyError: If key does not exist and default has not been provided
        """

        def pop_from(items: list, data: dict):
            key = items.pop(0)
            if key not in data:
                return default
            if items:
                data = data[key]
                return pop_from(items, data)
            else:
                return data.pop(key, default)

        return pop_from(self._split(key), self._data)

    def setdefault(self, key: str, default: Any = None) -> Any:
        """Get key value if exist otherwise set default value under given key
        and return its value.

        This method match 1:1 with dict .setdefault method except that
        it accepts deeply nested key with dot notation.

        Parameters:
            key: Single key or chain of keys
            default: Default value for not existing key

        Returns:
            Any value
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            self.__setitem__(key, default)
            return default

    def to_dict(self) -> dict:
        """Return wrapped dictionary.

        This method does not copy wrapped dictionary.

        Returns:
            Wrapped dictionary
        """
        return json.loads(self.to_json())

    def to_flat_dict(self, no_list: bool | None = None) -> dict:
        """Return wrapped dictionary as flat dictionary.

        Parameters:
            no_list: If set to True then numeric keys will NOT be converted to list indices
                     In other words, list values will be given as is.
                     Defaults to the value set in the constructor.

        Returns:
            Wrapped dictionary as flat dictionary
        """
        if no_list is None:
            no_list = self.no_list

        def flatten(d: dict, parent_key: str = ""):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{self.separator}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten(v, new_key).items())
                elif isinstance(v, list) and not no_list:
                    for i, item in enumerate(v):
                        items.extend(flatten({str(i): item}, new_key).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        return flatten(self.to_dict())

    def to_flat_json(self, no_list: bool | None = None) -> str:
        """Return wrapped dictionary as flat json string.

        Parameters:
            no_list: If set to True then numeric keys will NOT be converted to list indices
                     In other words, list values will be given as is.
                     Defaults to the value set in the constructor.

        Returns:
            Wrapped dictionary as flat json string
        """
        return json.dumps(self.to_flat_dict(no_list), cls=DottyEncoder)

    def to_json(self) -> str:
        """Return wrapped dictionary as json string.

        This method does not copy wrapped dictionary.

        Returns:
            Wrapped dictionary as json string
        """
        return json.dumps(self._data, cls=DottyEncoder)

    def update(self, data: dict[str, Any]):
        self._data.update(data)

    def values(self):
        """Returns the values of the category structure.

        Returns:
            The values of the category structure.
        """
        return self._data.values()

    @staticmethod
    def _find_data_type(item: Any, data: dict) -> Any:
        """This method returns item in datatype that exists in data dict.

        Method creates set of types present in dict keys
        and then iterates through them trying to convert item
        into one of types and check whether item under this type
        exists in dict keys. If yes then it'll return converted item.
        Otherwise item stays the same type as it was on entry.

        Parameters:
            item: Item to convert to proper type
            data: Dictionary to check for proper type

        Returns:
            Converted or unchanged item
        """
        data_types = [type(i) for i in data.keys()]
        for t in set(data_types):
            try:
                if t(item) in data:
                    item = t(item)
                    return item
            except ValueError:
                pass
        return item

    def _split(self, key: str) -> list[str]:
        """Split dot notated chain of keys.

        Works with custom separators and escape characters.

        Parameters:
            key: Single key or chain of keys

        Returns:
            List of keys
        """
        if not isinstance(key, str):
            return [key]
        esc_stamp = (self.esc_char + self.separator, "<#esc#>")
        skp_stamp = ("\\" + self.esc_char + self.separator, "<#skp#>" + self.separator)

        stamp_esc = ("<#esc#>", self.separator)
        stamp_skp = ("<#skp#>", self.esc_char)

        key = key.replace(*skp_stamp).replace(*esc_stamp)
        keys = key.split(self.separator)
        for i, k in enumerate(keys):
            keys[i] = k.replace(*stamp_esc).replace(*stamp_skp)

        return keys
