# src/runner/db_wiring.py
from database_utils.db_info import get_db_all_tables, get_table_all_columns, get_db_schema
from database_utils.sql_parser import get_sql_tables, get_sql_columns_dict, get_sql_condition_literals
from database_utils.execution import execute_sql, compare_sqls, validate_sql_query, aggregate_sqls, get_execution_status, subprocess_sql_executor
from .database_manager import DatabaseManager

functions = [
    subprocess_sql_executor,
    execute_sql,
    compare_sqls,
    validate_sql_query,
    aggregate_sqls,
    get_db_all_tables,
    get_table_all_columns,
    get_db_schema,
    get_sql_tables,
    get_sql_columns_dict,
    get_sql_condition_literals,
    get_execution_status
]

DatabaseManager.add_methods_to_class(functions)

