"""
Database Builder & SQL Execution Engine
Project: Retail Business Intelligence & Customer Analytics Platform

1. Creates a SQLite relational database `sql/retail_bi.db`.
2. Executes DDL schema from `sql/01_schema.sql`.
3. Loads Star Schema CSV files from `data/processed/`.
4. Executes and validates all SQL analytics scripts (02 through 08).
"""
import sqlite3
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
DB_PATH = SQL_DIR / "retail_bi.db"


def initialize_database():
    """Create database and execute DDL schema."""
    if DB_PATH.exists():
        DB_PATH.unlink()
        
    print(f"Initializing SQLite database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    schema_file = SQL_DIR / "01_schema.sql"
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()
        
    # Execute schema script
    cursor.executescript(schema_sql)
    conn.commit()
    print("Database schema created successfully.")
    return conn


def load_data_to_db(conn: sqlite3.Connection):
    """Load processed CSV files into corresponding database tables."""
    tables = [
        "dim_date",
        "dim_customer",
        "dim_product",
        "dim_geography",
        "dim_ship_mode",
        "fact_sales"
    ]
    
    for table in tables:
        csv_path = PROCESSED_DIR / f"{table}.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Required table CSV not found: {csv_path}")
            
        df = pd.read_csv(csv_path)
        df.to_sql(table, conn, if_exists="append", index=False)
        print(f"Loaded {len(df):,} rows into '{table}'")
        
    conn.commit()
    print("All tables loaded into database successfully.")


def run_sql_file(conn: sqlite3.Connection, sql_file_path: Path):
    """Execute all semicolon-separated queries in a SQL file and validate results."""
    print(f"\nExecuting: {sql_file_path.name}")
    with open(sql_file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split queries by semicolon while ignoring comments
    statements = [s.strip() for s in content.split(";") if s.strip()]
    
    cursor = conn.cursor()
    executed_count = 0
    for idx, stmt in enumerate(statements, 1):
        # Skip pure comment blocks
        lines = [line for line in stmt.split("\n") if not line.strip().startswith("--")]
        clean_stmt = "\n".join(lines).strip()
        if not clean_stmt:
            continue
            
        try:
            cursor.execute(clean_stmt)
            rows = cursor.fetchall()
            executed_count += 1
        except Exception as e:
            print(f"Error in {sql_file_path.name} (Query {idx}):\n{clean_stmt}\nError: {e}")
            raise e
            
    print(f"  Successfully executed {executed_count} queries in {sql_file_path.name}")


def validate_all_sql_scripts(conn: sqlite3.Connection):
    """Run all SQL analytics scripts from 02 to 08."""
    scripts = sorted([f for f in SQL_DIR.glob("*.sql") if f.name != "01_schema.sql"])
    for script in scripts:
        run_sql_file(conn, script)
    print("\n>>> ALL SQL SCRIPTS VALIDATED SUCCESSFULLY WITH ZERO ERRORS! <<<")


def main():
    conn = initialize_database()
    load_data_to_db(conn)
    validate_all_sql_scripts(conn)
    conn.close()


if __name__ == "__main__":
    main()

