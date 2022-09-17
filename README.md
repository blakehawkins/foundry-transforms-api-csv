# Install

```
pipenv install git+ssh://github.com/blakehawkins/foundry-transforms-api#egg=transformsbase
pipenv install git+ssh://github.com/blakehawkins/foundry-transforms-api-csv#egg=transforms
```

# Usage

```
from transforms.api import Input, Output, transform_df, TRANSFORMS_CSV_MAP

# Mock out shrinkwrap/catalog
global TRANSFORMS_CSV_MAP

TRANSFORMS_CSV_MAP["out"] = "out.csv"
TRANSFORMS_CSV_MAP["in"] = "in.csv"  # Just contains `id\n1\n2\n`

out = Output("out")

# Define xform
@transform_df(out, in_=Input("in"))
def myxform(in_):
  return in_

# Run it manually
myxform()

# Contents are also written to out.csv
assert(out.get().count() == 2)
```

If you want a transform to work cross-platform between csv and foundry, you can instead write a pipeline.py file that
calls into your transform -- see below.

foundryxform.py:

```
from transforms.api import transform_df, Input, Output

import pyspark.sql.functions as F


@transform_df(
    Output("ri.foundry.main.dataset.6e9e9ed9-1278-4fb9-a6cd-cde6fdb2e344"),
    thing1=Input("ri.foundry.main.dataset.9b9a2914-1e63-4433-96bd-7a7beb49f9f2"),
    thing2=Input("ri.foundry.main.dataset.8b6d914c-dd36-4bb7-86f7-f86e31f6d52a")
)
def foundryxform(thing1, thing2):
    # ...
```

mypipeline.py:

```
from foundryxform import foundryxform
from transforms.api import TRANSFORMS_CSV_MAP

global TRANSFORMS_CSV_MAP

TRANSFORMS_CSV_MAP["ri.foundry.main.dataset.9b9a2914-1e63-4433-96bd-7a7beb49f9f2"] = "testinput.csv"
TRANSFORMS_CSV_MAP["ri.foundry.main.dataset.8b6d914c-dd36-4bb7-86f7-f86e31f6d52a"] = "testinput2.csv"

foundryxform()
```

Since mypipeline.py is not run by foundry infrastructure, this file can be commited into the same repo as official
templates and run in parallel.

# Warning/note

Palantir maintains an open source fork of spark -- you may have inconsistencies if you try to use both
transforms-api-csv and foundry. transforms-api-csv is *not* supported software.
