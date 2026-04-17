from pathlib import Path

from pyspark.sql import functions as F

from spark_session_utils import create_spark_session


def main() -> None:
    spark = create_spark_session("spark-playground-joins")

    root = Path(__file__).resolve().parent.parent / "data"
    employees = spark.read.json(str(root / "employees.jsonl"))
    departments = spark.read.json(str(root / "departments.jsonl"))

    result = (
        employees.join(departments, on="team", how="left")
        .select("employee_id", "name", "team", "manager", "salary", "budget")
        .withColumn("salary_share_pct", F.round(F.col("salary") / F.col("budget") * 100, 2))
        .orderBy("team", F.desc("salary"))
    )

    result.show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
