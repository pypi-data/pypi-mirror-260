# print_versions

Package for listing versions of python packages used in a Jupyter notebook.

## Installation

```sh
pip install print-versions
```

## Usage

Print versions in ```requirements.txt``` format:

```python
from print_versions import print_versions

import numpy as np
from pandas import DataFrame

print_versions(globals())

# numpy==1.25.2
# pandas==1.5.3
```

Get versions as a dict:

```python
from print_versions import get_versions

import numpy as np
from pandas import DataFrame

get_versions(globals())

# {'numpy': '1.25.2', 'pandas': '1.5.3'}