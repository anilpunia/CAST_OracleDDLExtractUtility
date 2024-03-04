# import getpass

# import oracledb

# un = 'system'
# cs = 'QAPARTPG/orclpdb'
# #pw = getpass.getpass(f'Enter password for {un}@{cs}: ')
# pw = 'cast'
# with oracledb.connect(user=un, password=pw, dsn=cs) as connection:
#     with connection.cursor() as cursor:
#         sql = """select sysdate from dual"""
#         for r in cursor.execute(sql):
#             print(r)

import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r'C:\oracle\instantclient_21_12')
# Replace the following with your own Oracle connection information
username = "PLSQL_DIAGS_XXL"
password = "cast"
host = "QAPARTPG"
port = "1521"
service_name = "orclpdb"

# Create a connection object
connection = cx_Oracle.connect(username, password, host + ":" + port + "/" + service_name)

try:
    # Execute a simple query to check the connection status
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM DUAL")
    result = cursor.fetchone()
    print("Connection is active:", result[0] == 1)

except cx_Oracle.Error as error:
    print("Connection is not active:", error)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()