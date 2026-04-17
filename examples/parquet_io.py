from pathlib import Path

from pyspark.sql import functions as F

from spark_session_utils import create_spark_session


def main() -> None:
    spark = create_spark_session("spark-playground-parquet-io")

    root = Path(__file__).resolve().parent.parent
    input_path = root / "data" / "employees.jsonl"
    output_path = root / "data" / "output" / "employees_parquet"

    employees = spark.read.json(str(input_path))
    enriched = employees.withColumn("salary_band", F.when(F.col("salary") >= 135000, "high").otherwise("standard"))

    enriched.write.mode("overwrite").parquet(str(output_path))

    reloaded = spark.read.parquet(str(output_path)).orderBy("employee_id")
    reloaded.show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
