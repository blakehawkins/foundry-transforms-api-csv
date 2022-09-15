# Install

```
pipenv install git+ssh://github.com/blakehawkins/foundry-transforms-api-csv#egg=transformscsv
```

# Usage

```
from transformscsv.api import Input, Output, TRANSFORMS_CSV_MAP
from transforms.api import transform_df

global TRANSFORMS_CSV_MAP
OUTPUT_DIR = "test_output"

TRANSFORMS_CSV_MAP["out"] = OUTPUT_DIR
TRANSFORMS_CSV_MAP["in"] = "in.csv"  # Just contains `id\n1\n2\n`

out = Output("out")

@transform_df(out, in_=Input("in"))
def myxform(in_):
  return in_

myxform()

assert(out.get().count() == 2)
```
