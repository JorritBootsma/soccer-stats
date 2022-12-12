# This file contains more general SQL helper functions

def get_all_table_names(eng):
    all_tables = eng.execute(
        """
        SELECT
            table_schema || '.' || table_name
        FROM
            information_schema.tables
        WHERE
            table_type = 'BASE TABLE'
        AND
            table_schema NOT IN ('pg_catalog', 'information_schema');
        """
    ).fetchall()
    table_names = [tables_info[0] for tables_info in all_tables]
    return table_names
