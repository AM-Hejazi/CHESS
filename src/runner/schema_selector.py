def select_schema(task):
    """
    Select schema subset based on IR retrieval results.
    You can improve it later based on scores, types, etc.
    """
    if task.retrieved_tables is None or task.retrieved_columns is None:
        return None  # fallback: use full schema if IR failed

    table_names = task.retrieved_tables['id'].tolist()
    column_names = task.retrieved_columns['id'].tolist()

    selected_schema = {
        "tables": table_names,
        "columns": column_names
    }
    return selected_schema