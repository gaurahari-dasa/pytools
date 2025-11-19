import mysql.connector

def drop_table_with_dependencies(db_config, table_name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    def drop_table_recursive(table_name, visited):
        if table_name in visited:
            return
        visited.add(table_name)

        # Identify dependent tables
        cursor.execute(f"""
            SELECT table_name, constraint_name
            FROM information_schema.key_column_usage
            WHERE referenced_table_name = '{table_name}';
        """)
        dependencies = cursor.fetchall()

        # Recursively drop dependent tables
        for dep_table, constraint in dependencies:
            drop_table_recursive(dep_table, visited)

        # Drop foreign key constraints to break circular dependencies
        # cursor.execute(f"""
        #     SELECT constraint_name
        #     FROM information_schema.table_constraints
        #     WHERE table_name = '{table_name}' AND constraint_type = 'FOREIGN KEY';
        # """)
        # constraints = cursor.fetchall()
        # for (constraint,) in constraints:
        #     print(f"Dropping foreign key constraint {constraint} from table {table_name}")
        #     cursor.execute(f"ALTER TABLE {table_name} DROP FOREIGN KEY {constraint};")

        # Drop the current table
        print(f"Truncating table {table_name}")
        cursor.execute(f"TRUNCATE TABLE {table_name};")

    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    # Start the recursive drop process
    drop_table_recursive(table_name, set())
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

    conn.commit()
    cursor.close()
    conn.close()

# Example usage
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'your_database'
}
drop_table_with_dependencies(db_config, input('your_table_name? '))