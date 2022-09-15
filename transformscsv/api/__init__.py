from pyspark.sql import SparkSession
from transforms.api import transform_df, Input as IInput, Output as IOutput

TRANSFORMS_CSV_MAP = {}

class Input(IInput):
  def __init__(self, path):
    self._path = path

  def val(self):
    global TRANSFORMS_CSV_MAP
    spark = SparkSession.builder.master("local[1]").appName("transforms").getOrCreate()
    return spark.read.csv(TRANSFORMS_CSV_MAP[self._path], header=True)

class Output(IOutput):
  def __init__(self, path):
    self._path = path

  def write(self, v):
    global TRANSFORMS_CSV_MAP
    v.coalesce(1).write.csv(TRANSFORMS_CSV_MAP[self._path], header=True)

  def get(self):
    global TRANSFORMS_CSV_MAP
    spark = SparkSession.builder.master("local[1]").appName("transforms").getOrCreate()
    return spark.read.csv(TRANSFORMS_CSV_MAP[self._path], header=True)
