import uvicorn
from cnl_engine.api.app import app
from cnl_engine.config import config
from fastapi import FastAPI


def main(host: str = config["host"], port: int = config["port"]):
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
