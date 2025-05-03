import logging
import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

DB_MODE = os.getenv("DATA_MODE", "prod")
DB_ID   = os.getenv("DB_NAME")

def get_db_all_tables() -> List[str]:
    """
    Retrieves all table names with schema (e.g. 'Wamas.ART') from the SQL Server database.
    """
    from runner.database_manager import DatabaseManager
    try:
        dm = DatabaseManager(DB_MODE, DB_ID)
        rows = dm.fetch_all(
            "SELECT TABLE_SCHEMA, TABLE_NAME "
            "FROM INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_TYPE = 'BASE TABLE';"
        )
        # return 'schema.table'
        return [f"{schema}.{tbl}" for schema, tbl in rows]
    except Exception as e:
        logging.error(f"Error in get_db_all_tables: {e}")
        raise

def get_table_all_columns(table_name: str) -> List[str]:
    """
    Retrieves all column names for a given fully‐qualified table (schema.table).
    """
    from runner.database_manager import DatabaseManager
    try:
        # split off the schema
        schema, tbl = table_name.split(".", 1)
        dm = DatabaseManager(DB_MODE, DB_ID)
        rows = dm.fetch_all(
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?;",
            (schema, tbl)
        )
        return [r[0] for r in rows]
    except Exception as e:
        logging.error(f"Error in get_table_all_columns for {table_name}: {e}")
        raise

def get_db_schema() -> Dict[str, List[str]]:
    """
    Retrieves the full schema (schema.table → [columns]).
    """
    try:
        schema: Dict[str, List[str]] = {}
        for full_tbl in get_db_all_tables():
            schema[full_tbl] = get_table_all_columns(full_tbl)
        return schema
    except Exception as e:
        logging.error(f"Error in get_db_schema: {e}")
        raise
