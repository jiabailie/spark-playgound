from pathlib import Path

from spark_session_utils import create_spark_session


def main() -> None:
    spark = create_spark_session("spark-playground-sql-basics")

    input_path = Path(__file__).resolve().parent.parent / "data" / "employees.jsonl"
    employees = spark.read.json(str(input_path))
    employees.createOrReplaceTempView("employees")

    query = """
        select
            city,
            count(*) as employee_count,
            round(avg(salary), 2) as avg_salary
        from employees
        group by city
        order by avg_salary desc, city asc
    """

    spark.sql(query).show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
