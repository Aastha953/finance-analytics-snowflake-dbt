import pandas as pd
from pathlib import Path


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)


cost_centers = [
    ["CC001", "Finance Operations", "Finance", "Northeast", "Sarah Johnson"],
    ["CC002", "Corporate Finance", "Finance", "West", "Michael Brown"],
    ["CC003", "Enterprise Sales", "Sales", "Northeast", "David Wilson"],
    ["CC004", "Regional Sales", "Sales", "Southeast", "Jennifer Davis"],
    ["CC005", "Digital Marketing", "Marketing", "West", "Robert Miller"],
    ["CC006", "Operations", "Operations", "Midwest", "Lisa Anderson"],
    ["CC007", "Information Technology", "IT", "Northeast", "James Taylor"],
    ["CC008", "Human Resources", "Human Resources", "Southeast", "Emily Thomas"],
    ["CC009", "Procurement", "Procurement", "Midwest", "Daniel Moore"],
    ["CC010", "Manufacturing East", "Manufacturing", "Northeast", "Jessica Martin"],
    ["CC011", "Manufacturing West", "Manufacturing", "West", "Christopher Lee"],
    ["CC012", "Supply Chain", "Operations", "Southwest", "Amanda White"],
    ["CC013", "FP&A", "Finance", "Northeast", "Matthew Harris"],
    ["CC014", "Customer Success", "Sales", "West", "Ashley Clark"],
    ["CC015", "Corporate Services", "Operations", "Southeast", "Ryan Lewis"],
]


columns = [
    "cost_center_id",
    "cost_center_name",
    "department",
    "region",
    "manager",
]


df = pd.DataFrame(
    cost_centers,
    columns=columns
)


output_file = DATA_DIR / "cost_centers.csv"

df.to_csv(
    output_file,
    index=False
)


print("Cost Centers created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()
print(df.to_string(index=False))