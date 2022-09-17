from . import Input, Output, TRANSFORMS_CSV_MAP, transform_df

import os
import shutil

global TRANSFORMS_CSV_MAP

TRANSFORMS_CSV_MAP["out"] = "out.csv"
TRANSFORMS_CSV_MAP["in"] = "in.csv"

def test_xform():
  out = Output("out")

  @transform_df(out, in_=Input("in"))
  def myxform(in_):
    return in_

  myxform()

  print(out.get().collect())
  assert(out.get().count() == 2)
