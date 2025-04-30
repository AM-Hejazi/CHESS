@@ -1,8 +1,9 @@
import logging
import os
from typing import List, Dict
# query via our DatabaseManager
from ..runner.database_manager import DatabaseManager

# Read mode & db_id from env
DB_MODE = os.getenv("DATA_MODE", "dev")
DB_ID   = os.getenv("DB_NAME")  # use your DB_NAME as the identifier
@@ -11,7 +12,7 @@ DB_ID   = os.getenv("DB_NAME")  # use your DB_NAME as the identifier

def get_db_all_tables(db_path: str = None) -> List[str]:
    """

    Retrieves all table names from the SQL Server database via DatabaseManager.
    """
    try:
        dm = DatabaseManager(DB_MODE, DB_ID)
        rows = dm.fetch_all(
            "SELECT TABLE_NAME "
            "FROM INFORMATION_SCHEMA.TABLES "
@@ -20,7 +21,7 @@ def get_db_all_tables(db_path: str = None) -> List[str]:
        )
        return [r[0] for r in rows]
    except Exception as e:
        logging.error(f"Error in get_db_all_tables: {e}")
        raise

def get_table_all_columns(db_path: str = None, table_name: str = None) -> List[str]:
@@ -29,7 +30,7 @@ def get_table_all_columns(db_path: str = None, table_name: str = None) -> List[str]:
    """
    try:
        dm = DatabaseManager(DB_MODE, DB_ID)
        rows = dm.fetch_all(
            "SELECT COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.COLUMNS "
@@ -39,12 +40,12 @@ def get_table_all_columns(db_path: str = None, table_name: str = None) -> List[str]:
        )
        return [r[0] for r in rows]
    except Exception as e:
        logging.error(f"Error in get_table_all_columns for {table_name}: {e}")
        raise

def get_db_schema(db_path: str = None) -> Dict[str, List[str]]:
    """
#    Retrieves the schema of the database via DatabaseManager.
    """
    try:
        tables = get_db_all_tables()
