import logging
import os
from typing import List, Dict

from database_manager import DatabaseManager

# Read mode & db_id from env
DB_MODE = os.getenv("DATA_MODE", "dev")
DB_ID   = os.getenv("DB_NAME")  # use your DB_NAME as the identifier

def get_db_all_tables(db_path: str = None) -> List[str]:
    """
    Retrieves all table names from the SQL Server database.
    """
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
    """
    Retrieves all column names for a given table.
    """
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
    """
    Retrieves the schema of the database.
    """
    try:
        tables = get_db_all_tables()
        schema = {}
        for tbl in tables:
            cols = get_table_all_columns(table_name=tbl)
            schema[tbl] = cols
        return schema
    except Exception as e:
        logging.error(f"Error in get_db_schema: {e}")
        raise
