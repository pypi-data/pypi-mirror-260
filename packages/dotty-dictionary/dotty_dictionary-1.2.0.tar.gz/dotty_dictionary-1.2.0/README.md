# dotty-dictionary

[![PyPI version](https://badge.fury.io/py/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary)
[![Testsuite](https://github.com/01Joseph-Hwang10/dotty-dictionary/workflows/Test%20and%20Lint/badge.svg)](https://github.com/01Joseph-Hwang10/dotty-dictionary/actions?query=workflow%3A"Test+and+Lint")
[![Python version](https://img.shields.io/pypi/pyversions/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary)
[![Project Status](https://img.shields.io/pypi/status/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary/)
[![Supported Interpreters](https://img.shields.io/pypi/implementation/dotty-dictionary.svg)](https://pypi.org/project/dotty-dictionary/)
[![License](https://img.shields.io/pypi/l/dotty-dictionary.svg)](https://github.com/pawelzny/dotty-dictionary/blob/master/LICENSE)

`dotty-dictionary` is a Python library that provides a dictionary-like object that allows you to access nested dictionaries using dot notation.

`dotty-dictionary` is a fork of [pawelzny/dotty_dict](https://github.com/pawelzny/dotty_dict) that provides additional features and improvements.

## Features

- Simple wrapper around python dictionary and dict like objects
- Two wrappers with the same dict are considered equal
- Access to deeply nested keys with dot notation: dot['deeply.nested.key']
- Create, read, update and delete nested keys of any length
- Expose all dictionary methods like .get, .pop, .keys and other
- Access dicts in lists by index dot['parents.0.first_name']
- Support for setting value in multidimensional lists
- Support for accessing lists with slices
- Support for flattening nested dictionary keys from a dotty dictionary and vice versa
- Support for iteration over nested dictionary keys (e.g. `for key in dotty_dict_instance`)

## Installation

```bash
pip install dotty-dictionary
```

- Package: <https://pypi.org/project/dotty-dictionary>
- Source: <https://github.com/01Joseph-Hwang10/dotty-dictionary>

## Quick Example

Create new dotty using factory function.

```py
from dotty_dictionary import dotty
dot = dotty({'plain': {'old': {'python': 'dictionary'}}})
dot['plain.old']
{'python': 'dictionary'}
```

You can start with empty dotty

```py
from dotty_dictionary import dotty
dot = dotty() # Alias: `Dotty.empty()`
dot['very.deeply.nested.thing'] = 'spam'
dot
Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}}}}, separator='.', esc_char='\\')

dot['very.deeply.spam'] = 'indeed'
dot
Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}, 'spam': 'indeed'}}}, separator='.', esc_char='\\')

del dot['very.deeply.nested']
dot
Dotty(dictionary={'very': {'deeply': {'spam': 'indeed'}}}, separator='.', esc_char='\\')

dot.get('very.not_existing.key')
None
```

More examples can be found in the [examples](https://github.com/01Joseph-Hwang10/dotty-dictionary/tree/master/examples) directory.

> [!NOTE]\
> Using integer in dictionary keys will be treated as embedded list index.

## Flattening and Unflattening

You can utilize `to_flat_dict` and `from_flat_dict` to convert dotty to and from flat dictionary.

```py
from dotty_dictionary import Dotty
dot = Dotty.from_flat_dict({'very.deeply.nested.thing': 'spam', 'very.deeply.spam': 'indeed'})
dot
Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}, 'spam': 'indeed'}}}, separator='.', esc_char='\\')

dot.to_flat_dict()
{'very.deeply.nested.thing': 'spam', 'very.deeply.spam': 'indeed'}
```

## Custom Types && Encoders

By default, `dotty-dictionary` only considers `dict` as a mapping type, and `list` as a sequence type and will provide a dot notation access for them. However, you can also provide custom types to be considered as mapping or sequence types.

```py
from collections.abc import MutableMapping
from dataclasses import dataclass
from dotty_dictionary import Dotty, DottyEncoder


@dataclass
class User(MutableMapping):
    name: str
    age: int

class CustomJSONEncoder(DottyEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return {"name": obj.name, "age": obj.age}
        return super().default(obj)

dictionary = {
    "a": { 
        "b": { "c": 1, "d": 2 },
        "e": (3, {"f": 4}, (5, 6, 7)), # Has Tuple
    },
    "g": 8,
    "h": User(name="John", age=25), # Has Custom Dataclass
}
dot = Dotty(
    dictionary,
    mapping_types=(dict, User),
    sequence_types=(list, tuple),
    json_encoder=CustomJSONEncoder,
)

dot["a.e.1.f"]
4

dot["h.name"]
"John"

dot["h.age"] = 26
dot["h.age"]
26
```

Full example can be found on [tests/test_dotty_custom_types.py](https://github.com/01Joseph-Hwang10/dotty-dictionary/tree/master/tests/test_dotty_custom_types.py)


## Contributing

Any contribution is welcome! Check out [CONTRIBUTING.md](https://github.com/01Joseph-Hwang10/dotty-dictionary/blob/master/.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/01Joseph-Hwang10/dotty-dictionary/blob/master/.github/CODE_OF_CONDUCT.md) for more information on how to get started.

## License

`dotty-dictionary` is licensed under a [MIT License](https://github.com/01Joseph-Hwang10/dotty-dictionary/blob/master/LICENSE).
