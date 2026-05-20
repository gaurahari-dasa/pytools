import mysql.connector

def drop_table_with_dependencies(db_config, table_name, execute):
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
            WHERE referenced_table_name = '{table_name}' AND
            referenced_table_schema = '{db_config['database']}';
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
        sql = f"DROP TABLE {table_name};"
        print(sql)
        if (execute == 'yes'):
            cursor.execute(sql)

    cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
    # Start the recursive drop process
    drop_table_recursive(table_name, set())
    cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

    conn.commit()
    cursor.close()
    conn.close()

# Example usage
import getpass

db_config = {
    'user': input('DB username: '),
    'password': getpass.getpass('DB password: '),
    'host': input('DB host: '),
    'database': input('DB name: ')
}
while True:
    table = input('Table name (or "quit" to exit): ')
    if table.lower() == 'quit':
        break
    try:
        print('--- Dry run ---')
        drop_table_with_dependencies(db_config, table, 'no')
        print('--- End dry run ---')
    except Exception as e:
        print(f'Error: {e}')
        continue
    execute = input('Execute on DB (yes/no)? ')
    if execute.lower() == 'yes':
        try:
            drop_table_with_dependencies(db_config, table, execute)
        except Exception as e:
            print(f'Error: {e}')