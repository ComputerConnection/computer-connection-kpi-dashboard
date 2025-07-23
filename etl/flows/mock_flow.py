import json
from pathlib import Path

from prefect import flow, task

@task
def load_data():
    data = json.loads(Path('mocks/sample.json').read_text())
    print(f"Loaded {len(data)} records")

@flow
def mock_flow():
    load_data()

if __name__ == "__main__":
    mock_flow()
