import pyodbc

# Function to create and return database connection
def get_db_connection():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=LAPTOP-PINAHBJ2\\SQLEXPRESS01;"
            "DATABASE=Voting;"
            "Trusted_Connection=yes;"
        )
        return conn

    except Exception as e:
        print("❌ Database connection failed:")
        print(e)
        return None


# Optional: Test connection (run this file directly)
if __name__ == "__main__":
    conn = get_db_connection()

    if conn:
        print("✅ Connected to database successfully!")

        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.tables")

        print("\nTables in database:")
        for row in cursor:
            print(row[0])

        conn.close()
    else:
        print("❌ Could not connect to database.")