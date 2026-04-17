# Spark Playground

`spark-playground` is a small PySpark sandbox for local experimentation.

It supports:

- direct local PySpark execution
- Docker Compose Spark master/worker setup
- Jupyter notebook access
- basic and advanced Spark examples

## What You Can Do

This project is intended for quick Spark practice with small datasets.

You can use it to:

- learn DataFrame basics
- run Spark SQL queries
- try simple RDD operations
- practice joins
- practice window functions
- read and write parquet
- experiment interactively in Jupyter

## Requirements

### Local Python mode

- Python 3.10+
- Java 8+ or Java 11+

### Docker mode

- Docker
- Docker Compose

## Project Layout

```text
.
├── data/
│   ├── departments.jsonl
│   ├── employees.jsonl
│   ├── sales.jsonl
│   └── output/
├── docker-compose.yml
├── examples/
│   ├── dataframe_basics.py
│   ├── joins.py
│   ├── parquet_io.py
│   ├── rdd_basics.py
│   ├── spark_session_utils.py
│   ├── sql_basics.py
│   ├── window_functions.py
│   └── word_count.py
├── notebooks/
│   └── getting_started.ipynb
├── requirements.txt
└── README.md
```

## Quick Start

### Local mode

```bash
cd /Users/yangruiguo/Documents/spark-playground
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python examples/dataframe_basics.py
```

### Docker mode

```bash
cd /Users/yangruiguo/Documents/spark-playground
docker compose up -d
docker compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-playground/examples/dataframe_basics.py
```

## Option 1: Local Python Usage

Create and activate a virtual environment:

```bash
cd /Users/yangruiguo/Documents/spark-playground
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run examples directly with Python:

```bash
python examples/dataframe_basics.py
python examples/sql_basics.py
python examples/rdd_basics.py
python examples/word_count.py
python examples/joins.py
python examples/window_functions.py
python examples/parquet_io.py
```

If your local environment already exposes Spark CLI tools, you can also use:

```bash
spark-submit examples/dataframe_basics.py
spark-submit examples/joins.py
spark-submit examples/window_functions.py
spark-submit examples/parquet_io.py
```

### Expected local behavior

- each script starts a Spark session with `local[*]`
- output is printed directly to your terminal
- `parquet_io.py` writes parquet files under `data/output/employees_parquet`

## Option 2: Docker Compose Spark Setup

Start the Spark cluster and Jupyter:

```bash
cd /Users/yangruiguo/Documents/spark-playground
docker compose up -d
```

Services:

- Spark master endpoint: `spark://localhost:7077`
- Spark master UI: `http://localhost:8080`
- Spark worker UI: `http://localhost:8081`
- Jupyter: `http://localhost:8888`

Check containers:

```bash
docker compose ps
```

### Submit jobs to the Docker Spark cluster

Run from the Spark master container:

```bash
docker compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-playground/examples/dataframe_basics.py
docker compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-playground/examples/sql_basics.py
docker compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-playground/examples/joins.py
docker compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-playground/examples/window_functions.py
docker compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-playground/examples/parquet_io.py
```

## Jupyter Usage

Open:

```text
http://localhost:8888
```

Use token:

```text
spark
```

A starter notebook is included at:

- [getting_started.ipynb](/Users/yangruiguo/Documents/spark-playground/notebooks/getting_started.ipynb)

Inside the Jupyter container, the project is mounted at:

```text
/home/jovyan/work
```

That means:

- notebooks can read `/home/jovyan/work/data/...`
- notebooks can reuse code from `/home/jovyan/work/examples/...`

## Example Guide

### `examples/dataframe_basics.py`

Use this first.

It:

- reads `employees.jsonl`
- prints schema and sample rows
- filters employees by city and salary
- aggregates average salary by team

### `examples/sql_basics.py`

Use this to practice Spark SQL.

It:

- reads employee data
- creates a temporary SQL view
- runs grouped aggregation by city

### `examples/rdd_basics.py`

Use this for basic RDD API practice.

It:

- creates a small RDD
- applies `map`
- applies `filter`
- calculates a sum

### `examples/word_count.py`

Use this for a simple text-processing example.

It:

- reads this `README.md`
- tokenizes text into words
- counts the most common words

### `examples/joins.py`

Use this to practice joins.

It:

- reads employees and departments
- joins them by `team`
- calculates salary share against department budget

### `examples/window_functions.py`

Use this to practice analytic functions.

It:

- reads sales events
- parses timestamps
- computes running totals by customer
- computes ranking by category and amount

### `examples/parquet_io.py`

Use this to practice file IO.

It:

- reads JSONL employee data
- creates a derived column
- writes parquet output
- reads the parquet back and prints it

## Verifying That Things Work

### Local mode

Run:

```bash
python examples/dataframe_basics.py
```

You should see:

- a schema printout
- employee rows
- grouped salary output

### Docker mode

1. Start the stack:

```bash
docker compose up -d
```

2. Open the Spark master UI:

```text
http://localhost:8080
```

3. Submit one job:

```bash
docker compose exec spark-master spark-submit --master spark://spark-master:7077 /opt/spark-playground/examples/dataframe_basics.py
```

4. Refresh the Spark UI and confirm the application appears.

## Common Commands

Stop the Docker stack:

```bash
docker compose down
```

Remove containers and any anonymous volumes:

```bash
docker compose down -v
```

Rebuild local parquet output from scratch:

```bash
rm -rf data/output/employees_parquet
python examples/parquet_io.py
```

## Troubleshooting

### `java` not found

Install a JDK and make sure `java -version` works before running local PySpark.

### `spark-submit` not found

Use the direct Python commands instead, or run through Docker Compose.

### Jupyter page asks for token

Use:

```text
spark
```

### Docker Spark job cannot find files

Use the mounted path inside containers:

```text
/opt/spark-playground/examples/...
```

for Spark containers, and:

```text
/home/jovyan/work/...
```

for the Jupyter container.

## Notes

- local scripts default to `local[*]`
- Docker-based execution targets `spark://spark-master:7077`
- the sample datasets are intentionally small so results are easy to inspect
- parquet output is ignored by `.gitignore`
- local PySpark metadata files such as `spark-warehouse/` and `metastore_db/` are also ignored
