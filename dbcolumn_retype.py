import mysql.connector

def generate_alter_statements(host, user, password, database, table_name, column_name, new_data_type):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor(dictionary=True)

    statements = []

    # Get column definition including comment, nullability, default, auto_increment
    cursor.execute("""
        SELECT COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, EXTRA, COLUMN_COMMENT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
    """, (database, table_name, column_name))
    col_def = cursor.fetchone()

    if not col_def:
        raise Exception("Column not found.")

    nullable = "NULL" if col_def["IS_NULLABLE"] == "YES" else "NOT NULL"
    default = f"DEFAULT '{col_def['COLUMN_DEFAULT']}'" if col_def["COLUMN_DEFAULT"] is not None else ""
    extra = col_def["EXTRA"]
    comment = f"COMMENT '{col_def['COLUMN_COMMENT']}'" if col_def["COLUMN_COMMENT"] else ""

    # Find foreign key constraints referencing this column
    cursor.execute("""
        SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME = %s AND REFERENCED_COLUMN_NAME = %s
    """, (database, table_name, column_name))
    referencing = cursor.fetchall()

    # Drop foreign key constraints
    for ref in referencing:
        statements.append(f"ALTER TABLE `{ref['TABLE_NAME']}` DROP FOREIGN KEY `{ref['CONSTRAINT_NAME']}`;")

    # Alter the column in the target table
    alter_target = f"""
        ALTER TABLE `{table_name}` 
        MODIFY COLUMN `{column_name}` {new_data_type} {nullable} {default} {extra} {comment};
    """
    statements.append(alter_target.strip())

    # Alter the referencing columns to match the new data type and preserve comments
    for ref in referencing:
        cursor.execute("""
            SELECT COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, EXTRA, COLUMN_COMMENT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
        """, (database, ref["TABLE_NAME"], ref["COLUMN_NAME"]))
        ref_col_def = cursor.fetchone()

        ref_nullable = "NULL" if ref_col_def["IS_NULLABLE"] == "YES" else "NOT NULL"
        ref_default = f"DEFAULT '{ref_col_def['COLUMN_DEFAULT']}'" if ref_col_def["COLUMN_DEFAULT"] is not None else ""
        ref_extra = ref_col_def["EXTRA"]
        ref_comment = f"COMMENT '{ref_col_def['COLUMN_COMMENT']}'" if ref_col_def["COLUMN_COMMENT"] else ""

        alter_ref = f"""
            ALTER TABLE `{ref['TABLE_NAME']}` 
            MODIFY COLUMN `{ref['COLUMN_NAME']}` {new_data_type} {ref_nullable} {ref_default} {ref_extra} {ref_comment};
        """
        statements.append(alter_ref.strip())

    # Reapply foreign key constraints with ON UPDATE CASCADE and ON DELETE RESTRICT
    for ref in referencing:
        statements.append(f"""
            ALTER TABLE `{ref['TABLE_NAME']}` 
            ADD CONSTRAINT `{ref['CONSTRAINT_NAME']}` 
            FOREIGN KEY (`{ref['COLUMN_NAME']}`) 
            REFERENCES `{table_name}`(`{column_name}`) 
            ON UPDATE CASCADE ON DELETE RESTRICT;
        """.strip())

    cursor.close()
    conn.close()

    return statements

# Example usage:
if __name__ == "__main__":
    host = input("Connection URL: ")
    user = input("username: ")
    password = input("password: ")
    database = input("database: ")
    table_name = input("table: ")
    column_name = input("column: ")
    new_data_type = input("target datatype: ")  # Example target data type

    sql_statements = generate_alter_statements(host, user, password, database, table_name, column_name, new_data_type)

    for stmt in sql_statements:
        print(stmt)
