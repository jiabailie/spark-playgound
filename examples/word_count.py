from pathlib import Path

from pyspark.sql import functions as F

from spark_session_utils import create_spark_session


def main() -> None:
    spark = create_spark_session("spark-playground-word-count")

    input_path = Path(__file__).resolve().parent.parent / "README.md"
    lines = spark.read.text(str(input_path))

    words = (
        lines.select(F.explode(F.split(F.lower(F.col("value")), r"\W+")).alias("word"))
        .where(F.col("word") != "")
    )

    result = words.groupBy("word").count().orderBy(F.desc("count"), F.asc("word"))
    result.show(20, truncate=False)
    spark.stop()
    


if __name__ == "__main__":
    main()
