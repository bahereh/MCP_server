# python -m pip install -r requirements.txt
 
from mcp.server.fastmcp import FastMCP
from pathlib import Path
import logging
import os
import sys
import pandas as pd
import nbformat
from dotenv import load_dotenv
from sqlalchemy import create_engine
from data.validation import parse_datetime, validate_status
from data.services import get_service_code
from db.get_oracle_connection import get_oracle_connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
# -------------------------------------------------------
# Load environment variables
# -------------------------------------------------------
load_dotenv()

host = os.getenv("ORACLE_HOST")
port = os.getenv("ORACLE_PORT")
service = os.getenv("ORACLE_SERVICE")
user = os.getenv("ORACLE_USER")
password = os.getenv("ORACLE_PASSWORD")


dsn = f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service}"
engine = create_engine(dsn)
# -------------------------------------------------------
# Project paths
# -------------------------------------------------------
PROJECT_ROOT = Path(r"E:\root_path")

DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DB_DIR = PROJECT_ROOT / "db"


# -------------------------------------------------------
# Create MCP server
# -------------------------------------------------------

mcp = FastMCP("research-mcp-server")
print (mcp)

# --------------------------------------------

@mcp.tool()
def get_service_records(
    app_service_name: str,
    status: str,
    start_time: str,
    end_time: str
) -> dict:

    try:

        status_clean = validate_status(status)

        start_dt = parse_datetime(start_time)
        end_dt = parse_datetime(end_time)

        service_code = get_service_code(app_service_name, dsn)
        print(status_clean,start_dt,end_dt,service_code[0],service_code, type(service_code))

        if not service_code:
            return {"error": "Unknown service"}
        sql = """
                select
                    user_id
                    capturedate
                from sch1.vw_trasnaction1
                where
                    service_id = :service_id
                    and capturedate between :start_dt and :end_dt
                    and status = :status
                order by capturedate asc
                """
        params = {
                "service_id": service_code,
                "start_dt": start_dt,
                "end_dt": end_dt,
                "status": status_clean
            }

        logging.info("Executing SQL query:")
        logging.info(sql)
        logging.info(f"Params: {params}")

        with get_oracle_connection() as engine:
            
            data = pd.read_sql(sql, engine, params=params)

        return {
                "rows": data.to_dict(orient="records"),
                "count": len(data)
            }

    except Exception as e:
        logging.exception("get_service_records failed")

        return {"error": str(e)}



# -------------------------------------------------------
# Safety helper
# -------------------------------------------------------

def safe_path(base_dir: Path, relative_path: str) -> Path:
    """
    Prevents the model from reading files outside allowed folders.
    This protects against path traversal such as ../../secret.txt
    """
    requested_path = (base_dir / relative_path).resolve()
    base_dir = base_dir.resolve()

    if not str(requested_path).startswith(str(base_dir)):
        raise ValueError("Access denied: path is outside the allowed directory.")

    return requested_path

# -------------------------------------------------------
# Main entry point
# -------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="sse")
