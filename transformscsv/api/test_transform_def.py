from . import Input, Output, TRANSFORMS_CSV_MAP

import os
import shutil

from transforms.api import transform_df

global TRANSFORMS_CSV_MAP
OUTPUT_DIR = "test_output"

TRANSFORMS_CSV_MAP["out"] = OUTPUT_DIR
TRANSFORMS_CSV_MAP["in"] = "in.csv"

def test_xform():
  if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)

  out = Output("out")

  @transform_df(out, in_=Input("in"))
  def myxform(in_):
    return in_

  myxform()

  print(out.get().collect())
  assert(out.get().count() == 2)
