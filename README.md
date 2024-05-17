# panderaext

Extension of pandera type checking

# Installation

```bash
pip install panderaext
```

# Usage

```python
import pandas as pd
import pandera as pa

from panderaext.schema_helper import get_schema_columns

cols = get_schema_columns(MyDataset)
...
```
