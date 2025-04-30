import logging
import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

DB_MODE = os.getenv("DATA_MODE", "dev")
DB_ID   = os.getenv("DB_NAME")

def get_db_all_tables(db_path: str = None) -> List[str]:
    """Retrieves all table names from the SQL Server database."""
    from runner.database_manager import DatabaseManager
    try:
        dm = DatabaseManager(DB_MODE, DB_ID)
        rows = dm.fetch_all(
            "SELECT TABLE_NAME "
            "FROM INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_TYPE = 'BASE TABLE';"
        )
        return [r[0] for r in rows]
    except Exception as e:
        logging.error(f"Error in get_db_all_tables: {e}")
        raise

def get_table_all_columns(db_path: str = None, table_name: str = None) -> List[str]:
    """Retrieves all column names for a given table."""
    from runner.database_manager import DatabaseManager
    try:
        dm = DatabaseManager(DB_MODE, DB_ID)
        rows = dm.fetch_all(
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_NAME = ?;",
            (table_name,)
        )
        return [r[0] for r in rows]
    except Exception as e:
        logging.error(f"Error in get_table_all_columns for {table_name}: {e}")
        raise

def get_db_schema(db_path: str = None) -> Dict[str, List[str]]:
    """Retrieves the full schema (tables→columns)."""
    try:
        schema = {}
        for tbl in get_db_all_tables():
            schema[tbl] = get_table_all_columns(table_name=tbl)
        return schema
    except Exception as e:
        logging.error(f"Error in get_db_schema: {e}")
        raise
