import os
import sys
from pathlib import Path
import snowflake.connector

TABLES = {"budget": "RAW_BUDGET", "forecast": "RAW_FORECAST"}
DATA = Path(__file__).resolve().parents[1] / "data"

conn = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"],
    user=os.environ["SNOWFLAKE_USER"],
    authenticator="SNOWFLAKE_JWT",
    private_key_file=os.environ["HOME_SNOWFLAKE_KEY"],
    private_key_file_pwd=os.environ["SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"],
    role="ACCOUNTADMIN",
    warehouse="FINANCE_BI_WH",
    database="FINANCE_ANALYTICS",
    schema="RAW",
)
cur = conn.cursor()

for name in sys.argv[1:]:
    table = TABLES[name]
    csv_path = (DATA / f"{name}.csv").as_posix()
    print(f"\n--- Reloading {table} from {name}.csv ---")
    cur.execute(f"PUT 'file://{csv_path}' @FINANCE_STAGE AUTO_COMPRESS=TRUE OVERWRITE=TRUE")
    cur.execute("BEGIN")
    cur.execute(f"DELETE FROM {table}")
    cur.execute(f"""
        COPY INTO {table}
        FROM @FINANCE_STAGE/{name}.csv.gz
        FILE_FORMAT = (FORMAT_NAME = 'CSV_FORMAT')
        ON_ERROR = 'ABORT_STATEMENT'
        FORCE = TRUE
    """)
    cur.execute("COMMIT")
    rows = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {rows:,} rows loaded")

cur.close()
conn.close()