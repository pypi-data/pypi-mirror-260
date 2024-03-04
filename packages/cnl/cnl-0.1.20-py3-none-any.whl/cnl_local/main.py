import uvicorn
from cnl_local.api.app import app
from cnl_local.db.db_management.create_tables import create_tables
from cnl_local.utils.utils import create_needed_folders
from fastapi import FastAPI


def main(host: str = "0.0.0.0", port: int = 5009):
    create_needed_folders()
    create_tables()
    uvicorn.run(app, host=host, port=port, log_level="critical")


if __name__ == "__main__":
    main()
