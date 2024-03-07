"""
Overview
========

**Owner:** dan@1howardcapital.com

**Maintainer:** dan@1howardcapital.com

**Summary:** Zero-dependency python framework for object oriented development.
Implement _once_, document _once_, in _one_ place.

---

With fgr, you will quickly learn established best practice... \
or face the consequences of runtime errors that will break your code \
if you deviate from it.

Experienced python engineers will find a framework \
that expects and rewards intuitive magic method implementations, \
consistent type annotations, and robust docstrings.

Implement _pythonically_ with fgr and you will only ever need to: \
implement _once_, document _once_, in _one_ place.

---

Getting Started
---------------

### Installation

Install from command line, with pip:

`$ pip install fgr`

```

"""

from . import core

from . core import log

from .core.fields import Field
from .core.objects import Object

__version__ = '0.3.2-rc.1'
