# Data Utility Packages: _Core_

[![test](https://github.com/korawica/ddeutil/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/korawica/ddeutil/actions/workflows/tests.yml)
[![python support version](https://img.shields.io/pypi/pyversions/ddeutil)](https://pypi.org/project/ddeutil/)
[![size](https://img.shields.io/github/languages/code-size/korawica/ddeutil)](https://github.com/korawica/ddeutil)

**Table of Contents**:

- [Installation](#installation)
- [Features](#features)
  - [Base Utility Functions](#base-utility-functions)
    - [Hash](#hash)
    - [Checker](#checker)
    - [Convert](#convert)
  - [Utility Functions](#utility-functions)
    - [Date Utilities](#date-utilities)

The **Core Utility** package implements the utility functions and objects
that was created on sub-package namespace, `ddeutil`, design for independent
installation. I make this package able to extend with any sub-extension with this
namespace. This namespace able to scale out the coding with folder
structure design. You can add any extension features and import by
`import ddeutil.{extension}`.

> [!NOTE]
> This package provide the Base Utility functions and objects for any sub-namespace
> package that use for data function or application.

## Installation

```shell
pip install -U ddeutil
```

## Features

### Base Utility Functions

```text
core.base
    - cache
    - checker
    - convert
    - elements
    - hash
    - merge
    - sorting
    - splitter
```

#### Hash

```python
from ddeutil.core import random_str, hash_str

assert hash_str('hello world') == '05751529'
assert len(random_str()) == 8  # Random str with default length, 8
```

#### Checker

```python
from ddeutil.core import can_int, is_int

assert is_int('-3')
assert not is_int('0.0')
assert not is_int('-3.1')

assert can_int('-1.0')
assert not can_int('1.1')
```

#### Convert

```python
from ddeutil.core import str2bool

assert str2bool('yes')
assert not str2bool('no')
assert not str2bool('0')
```

### Utility Functions

```text
core
    - decorator
    - dtutils
```

#### Date Utilities

```python
import datetime
from ddeutil.core.dtutils import next_date

assert (
  next_date(datetime.datetime(2023, 1, 31, 0, 0, 0), mode='day')
  == datetime.datetime(2023, 2, 1, 0, 0)
)
```

## License

This project was licensed under the terms of the [MIT license](LICENSE).
