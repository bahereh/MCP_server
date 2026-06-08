import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_oracle_connection():
    print(f'----------------STARTING [get_oracle_connection ()]----------------')
    host = os.getenv("ORACLE_HOST")
    port = os.getenv("ORACLE_PORT")
    service = os.getenv("ORACLE_SERVICE")
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")

    if not all([host, port, service, user, password]):
        raise ValueError("Missing Oracle configuration")

    dsn = f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}"
    engine = create_engine(dsn)
    return engine