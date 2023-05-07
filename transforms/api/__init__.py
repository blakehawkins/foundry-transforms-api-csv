import os
from pathlib import Path
import shutil
import tempfile

from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from transformsbase.api import transform_df as transform_df_base, Input as IInput, Output as IOutput

TRANSFORMS_CSV_MAP: dict[str, str] = {}

transform_df = transform_df_base


class Input(IInput):
  def __init__(self, path: str, *, spark_conf: dict[str, str] | None = None):
    self._path = path
    self._spark_conf = spark_conf or {}

  def val(self) -> DataFrame:
    global TRANSFORMS_CSV_MAP
    spark_builder = SparkSession.builder.master("local[1]").appName("transforms")
    for k, v in self._spark_conf.items():
        spark_builder.config(k, v)
    spark = spark_builder.getOrCreate()
    return spark.read.csv(TRANSFORMS_CSV_MAP[self._path], header=True)

class Output(IOutput):
  def __init__(self, path: str, *, spark_conf: dict[str, str] | None = None):
    self._path = path
    self._spark_conf = spark_conf or {}

  def write(self, v: DataFrame) -> None:
    global TRANSFORMS_CSV_MAP
    with tempfile.TemporaryDirectory() as tmpdir:
      path = Path(tmpdir) / "spark"
      v.coalesce(1).write.csv(str(path), header=True)
      wrote = path / [fi for fi in os.listdir(path) if fi.endswith(".csv")][0]
      shutil.move(wrote, TRANSFORMS_CSV_MAP[self._path]), 

  def get(self) -> DataFrame:
    global TRANSFORMS_CSV_MAP
    spark = SparkSession.builder.master("local[1]").appName("transforms").getOrCreate()
    return spark.read.csv(TRANSFORMS_CSV_MAP[self._path], header=True)
