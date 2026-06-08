from sqlalchemy import create_engine
import pandas as pd



def get_service_code(app_service_name: str,dsn) -> int | None:
    sql = f"""
        SELECT service_id
        FROM sch1.services
        WHERE lower(service_name) = {app_service_name}
    """
    engine = create_engine(dsn)
    df = pd.read_sql(sql, engine) 
    service_id = df.service_id
    return service_id
