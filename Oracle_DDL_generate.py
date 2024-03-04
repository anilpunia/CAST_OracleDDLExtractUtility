import cx_Oracle
import time

def check_privileges(connection):
    cursor = connection.cursor()

    # Check if the user has DBA or ALL privileges
    query = """
    SELECT granted_role
    FROM DBA_ROLE_PRIVS
    WHERE granted_role IN ('DBA', 'ALL')
    """
    cursor.execute(query)
    privileges = [row[0] for row in cursor.fetchall()]

    cursor.close()
    return privileges

def get_table_info(connection, schema_name):
    cursor = connection.cursor()

    # Get table names in the specified schema
    query = """
    SELECT table_name, column_name, data_type
    FROM all_tab_columns
    WHERE owner = :schema_name
    ORDER BY table_name, column_id
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    table_info = {}
    for row in rows:
        table_name = row[0]
        column_name = row[1]
        data_type = row[2]

        if table_name not in table_info:
            table_info[table_name] = {'columns': []}

        table_info[table_name]['columns'].append({'name': column_name, 'type': data_type})

    cursor.close()
    return table_info

def get_function_info(connection, schema_name):
    cursor = connection.cursor()

    # Get function information with definition
    query = """
    SELECT a.object_name, a.argument_name, a.data_type, a.package_name
    FROM all_arguments a
    JOIN all_objects o ON a.owner = o.owner AND a.object_name = o.object_name
    WHERE a.owner = :schema_name
    AND o.object_type = 'FUNCTION'
    ORDER BY a.object_name, a.sequence
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    functions = {}
    for row in rows:
        function_name = row[0]
        argument_name = row[1]
        data_type = row[2]
        package_name = row[3]

        if function_name not in functions:
            functions[function_name] = {'args': []}

        functions[function_name]['args'].append({'name': argument_name, 'type': data_type, 'package': package_name})

    cursor.close()
    return functions

def get_procedure_info(connection, schema_name):
    cursor = connection.cursor()

    # Get procedure information with definition
    query = """
    SELECT a.object_name, a.argument_name, a.data_type, a.package_name
    FROM all_arguments a
    JOIN all_objects o ON a.owner = o.owner AND a.object_name = o.object_name
    WHERE a.owner = :schema_name
    AND o.object_type = 'PROCEDURE'
    ORDER BY a.object_name, a.sequence

    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    procedures = {}
    for row in rows:
        procedure_name = row[0]
        argument_name = row[1]
        data_type = row[2]
        package_name = row[3]

        if procedure_name not in procedures:
            procedures[procedure_name] = {'args': []}

        procedures[procedure_name]['args'].append({'name': argument_name, 'type': data_type, 'package': package_name})

    cursor.close()
    return procedures

def get_trigger_info(connection, schema_name):
    cursor = connection.cursor()

    # Get trigger information with definition
    query = """
    SELECT trigger_name, table_name, trigger_type, triggering_event, table_owner, base_object_type
    FROM all_triggers
    WHERE owner = :schema_name
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    triggers = []
    for row in rows:
        trigger_name = row[0]
        table_name = row[1]
        trigger_type = row[2]
        triggering_event = row[3]
        table_owner = row[4]
        base_object_type = row[5]

        triggers.append({
            'name': trigger_name,
            'table': table_name,
            'type': trigger_type,
            'event': triggering_event,
            'owner': table_owner,
            'base_object_type': base_object_type
        })

    cursor.close()
    return triggers

def get_sequence_info(connection, schema_name):
    cursor = connection.cursor()

    # Get sequence information
    query = """
    SELECT sequence_name
    FROM all_sequences
    WHERE sequence_owner = :schema_name
    """
    cursor.execute(query, schema_name=schema_name)
    sequences = [row[0] for row in cursor.fetchall()]

    cursor.close()
    return sequences

def get_view_info(connection, schema_name):
    cursor = connection.cursor()

    # Get view information with definition
    query = """
    SELECT view_name, text
    FROM all_views
    WHERE owner = :schema_name
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    views = []
    for row in rows:
        view_name = row[0]
        view_definition = row[1]

        views.append({'name': view_name, 'definition': view_definition})

    cursor.close()
    return views

def get_synonym_info(connection, schema_name):
    cursor = connection.cursor()

    # Get synonym information
    query = """
    SELECT synonym_name, table_name
    FROM all_synonyms
    WHERE owner = :schema_name
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    synonyms = []
    for row in rows:
        synonym_name = row[0]
        table_name = row[1]

        synonyms.append({'name': synonym_name, 'table': table_name})

    cursor.close()
    return synonyms

def get_package_info(connection, schema_name):
    cursor = connection.cursor()

    # Get package information with definition
    query = """
    SELECT name, text
    FROM all_source
    WHERE owner = :schema_name
    AND type = 'PACKAGE'
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    packages = {}
    for row in rows:
        package_name = row[0]
        package_definition = row[1]

        packages[package_name] = {'definition': package_definition}

    cursor.close()
    return packages

def get_index_info(connection, schema_name):
    cursor = connection.cursor()

    # Get index information
    query = """
    SELECT i.index_name, i.table_name, i.uniqueness, c.column_name
    FROM all_indexes i
    JOIN all_ind_columns c ON i.index_name = c.index_name
    WHERE i.table_owner = :schema_name
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    indexes = {}
    for row in rows:
        index_name = row[0]
        table_name = row[1]
        uniqueness = row[2]
        column_name = row[3]

        if index_name not in indexes:
            indexes[index_name] = {'table': table_name, 'uniqueness': uniqueness, 'columns': []}

        indexes[index_name]['columns'].append(column_name)

    cursor.close()
    return indexes

def get_materialized_view_info(connection, schema_name):
    cursor = connection.cursor()

    # Get materialized view information with definition
    query = """
    SELECT mview_name, query
    FROM all_mviews
    WHERE owner = :schema_name
    """
    cursor.execute(query, schema_name=schema_name)
    rows = cursor.fetchall()

    materialized_views = []
    for row in rows:
        mview_name = row[0]
        query_definition = row[1]

        materialized_views.append({'name': mview_name, 'definition': query_definition})

    cursor.close()
    return materialized_views


def generate_ddl(dbname, user, password, host, port, schema_name, tables, functions, procedures, triggers, sequences, views, synonyms, packages, indexes, materialized_views):
    ddl_statements = []

    # Create schema
    ddl_statements.append(f"CREATE USER {schema_name} IDENTIFIED BY {password};")
    ddl_statements.append(f"GRANT CONNECT, RESOURCE TO {schema_name};")

    # Generate DDL for tables
    for table_name, table_info in tables.items():
        columns = table_info['columns']

        # Create table
        ddl_statements.append(f"\nCREATE TABLE {table_name} (")

        # Add columns
        for column in columns:
            ddl_statements.append(f"    {column['name']} {column['type']},")

        # Remove trailing comma from the last column
        ddl_statements[-1] = ddl_statements[-1][:-1]

        # Close table creation statement
        ddl_statements.append(");")

    # Generate DDL for functions
    for function_name, function_info in functions.items():
        args = function_info['args']

        # Create function
        ddl_statements.append(f"\nCREATE OR REPLACE FUNCTION {function_name} (")

        # Add arguments
        for arg in args:
            ddl_statements.append(f"    {arg['name']} {arg['type']},")

        # Remove trailing comma from the last argument
        ddl_statements[-1] = ddl_statements[-1][:-1]

        return_type = 'NUMBER'  # Modify based on actual return type
        ddl_statements.append(f") RETURN {return_type} AS")
        ddl_statements.append(f"BEGIN")
        ddl_statements.append(f"    -- Function body here")
        ddl_statements.append(f"END {function_name};")

    # Generate DDL for procedures
    for procedure_name, procedure_info in procedures.items():
        args = procedure_info['args']

        # Create procedure
        ddl_statements.append(f"\nCREATE OR REPLACE PROCEDURE {procedure_name} (")

        # Add arguments
        for arg in args:
            ddl_statements.append(f"    {arg['name']} {arg['type']},")

        # Remove trailing comma from the last argument
        ddl_statements[-1] = ddl_statements[-1][:-1]

        ddl_statements.append(f") AS")
        ddl_statements.append(f"BEGIN")
        ddl_statements.append(f"    -- Procedure body here")
        ddl_statements.append(f"END {procedure_name};")

    # Generate DDL for triggers
    for trigger_info in triggers:
        trigger_name = trigger_info['name']
        table_name = trigger_info['table']
        trigger_type = trigger_info['type']
        event = trigger_info['event']
        owner = trigger_info['owner']
        base_object_type = trigger_info['base_object_type']

        # Create trigger
        ddl_statements.append(f"\nCREATE OR REPLACE TRIGGER {trigger_name}")
        ddl_statements.append(f"    {trigger_type} {event} ON {owner}.{table_name}")
        ddl_statements.append(f"BEGIN")
        ddl_statements.append(f"    -- Trigger body here")
        ddl_statements.append(f"END {trigger_name};")

    # Generate DDL for sequences
    for sequence_name in sequences:
        ddl_statements.append(f"\nCREATE SEQUENCE {sequence_name};")

    # Generate DDL for views
    for view_info in views:
        view_name = view_info['name']
        view_definition = view_info['definition']

        ddl_statements.append(f"\nCREATE OR REPLACE VIEW {view_name} AS")
        ddl_statements.append(f"    {view_definition};")
    
    # Generate DDL for synonyms
    for synonym_info in synonyms:
        synonym_name = synonym_info['name']
        table_name = synonym_info['table']

        ddl_statements.append(f"\nCREATE SYNONYM {synonym_name} FOR {table_name};")

    # Generate DDL for packages
    for package_name, package_info in packages.items():
        package_definition = package_info['definition']

        ddl_statements.append(f"\nCREATE OR REPLACE PACKAGE {package_name} AS")
        ddl_statements.append(f"    {package_definition};")

    # Generate DDL for indexes
    for index_name, index_info in indexes.items():
        table_name = index_info['table']
        uniqueness = index_info['uniqueness']
        columns = index_info['columns']

        ddl_statements.append(f"\nCREATE {'' if uniqueness == 'UNIQUE' else 'NON '}UNIQUE INDEX {index_name} ON {table_name} (")

        for column in columns:
            ddl_statements.append(f"    {column},")

        ddl_statements[-1] = ddl_statements[-1][:-1]  # Remove trailing comma
        ddl_statements.append(");")

    # Generate DDL for materialized views
    for mview_info in materialized_views:
        mview_name = mview_info['name']
        query_definition = mview_info['definition']

        ddl_statements.append(f"\nCREATE MATERIALIZED VIEW {mview_name} AS")
        ddl_statements.append(f"    {query_definition};")

    return '\n'.join(ddl_statements)

# def get_dsn(host, port, service_name_or_sid):
#     if ':' in service_name_or_sid:
#         # SID format: host:port/sid
#         return cx_Oracle.makedsn(host, port, service_name_or_sid)
#     else:
#         # Service name format
#         return cx_Oracle.makedsn(host, port, service_name=service_name_or_sid)

# Function to try both connection options
def try_connecting(user, password, host, port, service_name):
    # First connection option using cx_Oracle.makedsn
    try:
        dsn_tns = cx_Oracle.makedsn(host, port, service_name=service_name)
        connection = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
        return connection
    except cx_Oracle.DatabaseError:
        pass

    # Second connection option
    try:
        connection = cx_Oracle.connect(user=user, password=password,
                                       dsn=f"{host}:{port}/{service_name}",
                                       encoding="UTF-8")
        return connection
    except cx_Oracle.DatabaseError:
        pass

    # If both connection attempts fail, return None
    return None

# Get user input
user = input("Enter the username: ")
password = input("Enter the password: ")
host = input("Enter the host: ")
port = input("Enter the port: ")
service_name = input("Enter the Oracle service name or SID: ")  # Use SID or service name here
schema_name = input("Enter the schema name: ")
output_file_path = input("Enter the output file path: ")
Oracle_Client = input("Enter the Oracle Client path: ")
Oracle_Client_Path = r"{}".format(Oracle_Client)
#print(f"Oracle Client Path: {Oracle_Client_Path}")
#service_name_or_sid = 'orclpdb'
#user = 'PLSQL_DIAGS_XXL'
#password = 'xxxxx'
#host = 'CASTTEST'
#port = '1521'
#schema_name = 'DEMO'
#output_file_path = 'D:\CAST\Development\VSCode\Generic-Script\ora.sql'

# Connect to the database using oracledb
#with oracledb.connect(user=user, password=password, dsn=f'{host}:{port}/{service_name_or_sid}') as connection:

# Initialize Oracle Client
cx_Oracle.init_oracle_client(lib_dir=Oracle_Client_Path)

# Connect to the database using cx_Oracle
#dsn_tns = get_dsn(host, port, service_name_or_sid)
#print (f"DNS Connection: {dsn_tns}")
#time.sleep(60)
#connection = cx_Oracle.connect(user=user, password=password, dsn=dsn_tns)
connection = try_connecting(user, password, host, port, service_name)
print (f"DNS Connection: {connection}")
if connection is not None:
    # Connection succeeded
    print("Connection successful.")
    # Check privileges
    user_privileges = check_privileges(connection)

    # Print user privileges for troubleshooting
    print(f"User Privileges: {user_privileges}")
        
    # Abort the script if the user does not have DBA or ALL privileges
    if not any(privilege in ('DBA', 'ALL') for privilege in user_privileges):
        print(f"Oracle user ** {user} ** doesn't have enough privileges. Please use user with DBA or ALL privileges. Script aborted.")
    else:

            with connection.cursor() as cursor:
            # Get table, function, procedure, trigger, sequence, and view information
                #print(f"Is connected: {connection.is_healthy()}")
                
                tables_info = get_table_info(connection, schema_name)
                #print(f"Tables: {tables_info}")
                
                functions_info = get_function_info(connection, schema_name)
                #print(f"Functions: {functions_info}")
                
                procedures_info = get_procedure_info(connection, schema_name)
                #print(f"Procedures: {procedures_info}")
                
                triggers_info = get_trigger_info(connection, schema_name)
                #print(f"Triggers: {triggers_info}")
                
                sequences_info = get_sequence_info(connection, schema_name)
                #print(f"Sequences: {sequences_info}")
                
                views_info = get_view_info(connection, schema_name)
                #print(f"Views: {views_info}")
                
                synonyms_info = get_synonym_info(connection, schema_name)
                #print(f"Synonyms: {synonyms_info}")

                packages_info = get_package_info(connection, schema_name)
                #print(f"Packages: {packages_info}")

                indexes_info = get_index_info(connection, schema_name)
                #print(f"Indexes: {indexes_info}")

                materialized_views_info = get_materialized_view_info(connection, schema_name)
                #print(f"Materialized Views: {materialized_views_info}")
                # Generate DDL
                ddl_script = generate_ddl(service_name, user, password, host, port, schema_name, tables_info, functions_info, procedures_info, triggers_info, sequences_info, views_info, synonyms_info, packages_info, indexes_info, materialized_views_info)

                # Write DDL script to a file
                with open(output_file_path, 'w') as output_file:
                    output_file.write(ddl_script)

            # Close the database connection if it exists
            try:
                if connection:
                    connection.close()
                    print("Connection closed successfully.")
            except cx_Oracle.Error as e:
                    print(f"Error while closing connection: {e}")

            print(f"DDL script written to: {output_file_path}")
else:
    # Both connection attempts failed
    print("Failed to establish a connection.")