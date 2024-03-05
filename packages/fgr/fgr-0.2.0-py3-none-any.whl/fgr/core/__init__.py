"""
Overview
========

**Owner:** dan@1howardcapital.com

**Maintainer:** dan@1howardcapital.com

**Summary:** Zero-dependency python framework for object oriented development.

---

Usage
-----

```py
import fgr
```

"""

from . import codec
from . import constants
from . import dtypes
from . import enums
from . import exceptions
from . import fields
from . import log
from . import meta
from . import modules
from . import objects
from . import patterns
from . import query
from . import utils

utils._resolve_remaining_type_refs()

__version__ = '0.0.0'
