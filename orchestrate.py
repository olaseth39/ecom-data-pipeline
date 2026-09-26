from prefect import flow, task
import subprocess
import os
import sys

# Define the paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DBT_DIR = os.path.join(BASE_DIR, "ecommerce_dbt")

@task
def run_python_ingestion():
    """Task 1: Runs the Python script to ingest data."""
    print("Running Python ingestion...")
    subprocess.run([sys.executable, "ingest_api.py"], check=True, cwd=BASE_DIR, env=os.environ.copy())

@task
def run_dbt_transformations():
    """Task 2: Runs dbt models to transform data."""
    print("Running dbt transformations...")
    subprocess.run([sys.executable, "-m", "dbt.cli.main", "run"], check=True, cwd=DBT_DIR, env=os.environ.copy())

@task
def run_dbt_tests():
    """Task 3: Runs dbt tests to ensure data quality."""
    print("Running dbt tests...")
    subprocess.run([sys.executable, "-m", "dbt.cli.main", "test"], check=True, cwd=DBT_DIR, env=os.environ.copy())

# Define the Flow
@flow(name="ecommerce_daily_pipeline")
def ecommerce_pipeline():
    run_python_ingestion()
    run_dbt_transformations()
    run_dbt_tests()
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    ecommerce_pipeline()