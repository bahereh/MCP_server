import os
from dotenv import load_dotenv
import oracledb

# 1. Manually load your env (just in case)
load_dotenv()

host = os.getenv("ORACLE_HOST")
port = os.getenv("ORACLE_PORT")
service = os.getenv("ORACLE_SERVICE")
user = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")

print(f"Attempting to connect to {host}:{port} with service {service}...")

try:
    # 2. Try the simplest possible connection
    conn = oracledb.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        service_name=service
    )
    print("✅ SUCCESS! Connected to Oracle!")
    conn.close()
except Exception as e:
    print("❌ FAILED! Here is the error:")
    print(e)
