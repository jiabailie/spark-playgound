from pathlib import Path

from pyspark.sql import functions as F
from pyspark.sql.window import Window

from spark_session_utils import create_spark_session


def main() -> None:
    spark = create_spark_session("spark-playground-window-functions")

    input_path = Path(__file__).resolve().parent.parent / "data" / "sales.jsonl"
    sales = (
        spark.read.json(str(input_path))
        .withColumn("event_time", F.to_timestamp("event_time"))
    )

    customer_window = Window.partitionBy("customer_id").orderBy("event_time")
    category_window = Window.partitionBy("category").orderBy(F.desc("amount"))

    result = (
        sales.withColumn("running_amount", F.round(F.sum("amount").over(customer_window), 2))
        .withColumn("customer_order_rank", F.row_number().over(customer_window))
        .withColumn("category_amount_rank", F.dense_rank().over(category_window))
        .orderBy("customer_id", "event_time")
    )

    result.show(truncate=False)
    spark.stop()


if __name__ == "__main__":
    main()
