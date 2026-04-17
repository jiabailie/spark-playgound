from spark_session_utils import create_spark_session


def main() -> None:
    spark = create_spark_session("spark-playground-rdd-basics")

    sc = spark.sparkContext
    numbers = sc.parallelize(range(1, 11))

    squares = numbers.map(lambda value: (value, value * value))
    evens = squares.filter(lambda item: item[0] % 2 == 0)

    print("Squares:")
    print(squares.collect())

    print("Even squares:")
    print(evens.collect())

    print("Sum of numbers:")
    print(numbers.sum())

    spark.stop()


if __name__ == "__main__":
    main()
