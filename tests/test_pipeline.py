import os
import subprocess
import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))

def test_ingestion_script():
    script_path = os.path.join(REPO_ROOT, "src", "ingestion.py")
    res = subprocess.run(["python", script_path], cwd=REPO_ROOT, capture_output=True, text=True)
    assert res.returncode == 0, f"Ingestion failed with error: {res.stderr}"
    assert "Ingestion complete" in res.stdout

def test_transformation_script():
    script_path = os.path.join(REPO_ROOT, "src", "transformation_star_schema.py")
    res = subprocess.run(["python", script_path], cwd=REPO_ROOT, capture_output=True, text=True)
    assert res.returncode == 0, f"Transformation failed with error: {res.stderr}"
    assert "Star schema complete" in res.stdout

def test_output_csv_files_exist():
    fact_csv = os.path.join(REPO_ROOT, "data", "processed", "fact_emissions.csv")
    dim_csv = os.path.join(REPO_ROOT, "data", "processed", "dim_producer.csv")
    assert os.path.exists(fact_csv), "fact_emissions.csv should exist"
    assert os.path.exists(dim_csv), "dim_producer.csv should exist"
    assert os.path.getsize(fact_csv) > 0
    assert os.path.getsize(dim_csv) > 0
