import pyodbc

conn_string = (
    "Engine = mssql;"
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=HELSB-OPS-21;"
    "Database=SFMSDB;"
    "UID= '';"
    "PWD= ;"
)

try:
    connection = pyodbc.connect(conn_string)
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")
