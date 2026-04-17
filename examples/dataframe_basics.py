from pathlib import Path

from pyspark.sql import functions as F

from spark_session_utils import create_spark_session


def main() -> None:
    spark = create_spark_session("spark-playground-dataframe-basics")

    input_path = Path(__file__).resolve().parent.parent / "data" / "employees.jsonl"
    employees = spark.read.json(str(input_path))

    print("Schema:")
    employees.printSchema()

    print("Raw data:")
    employees.show(truncate=False)

    print("Employees in Shanghai with salary >= 125000:")
    (
        employees.where((F.col("city") == "Shanghai") & (F.col("salary") >= 125000))
        .select("employee_id", "name", "team", "salary")
        .orderBy(F.desc("salary"))
        .show(truncate=False)
    )

    print("Average salary by team:")
    (
        employees.groupBy("team")
        .agg(
            F.count("*").alias("employee_count"),
            F.round(F.avg("salary"), 2).alias("avg_salary"),
            F.max("salary").alias("max_salary"),
        )
        .orderBy("team")
        .show(truncate=False)
    )

    spark.stop()


if __name__ == "__main__":
    main()
