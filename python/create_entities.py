import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


entities = [
    [
        "US001",
        "Apex Manufacturing USA",
        "USA",
        "USD"
    ],
    [
        "US002",
        "Apex Distribution USA",
        "USA",
        "USD"
    ],
    [
        "CA001",
        "Apex Canada",
        "Canada",
        "CAD"
    ],
]


columns = [
    "entity_id",
    "entity_name",
    "country",
    "currency"
]


df = pd.DataFrame(
    entities,
    columns=columns
)


output_file = DATA_DIR / "entities.csv"

df.to_csv(
    output_file,
    index=False
)


print("Entities created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()
print(df.to_string(index=False))