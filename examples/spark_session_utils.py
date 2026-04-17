from pyspark.sql import SparkSession


def create_spark_session(app_name: str) -> SparkSession:
    master = __import__("os").environ.get("SPARK_MASTER", "local[*]")
    return SparkSession.builder.appName(app_name).master(master).getOrCreate()
