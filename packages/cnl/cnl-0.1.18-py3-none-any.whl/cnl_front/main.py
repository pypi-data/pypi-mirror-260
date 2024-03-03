import uvicorn
from cnl_front.static_server import app
from fastapi import FastAPI


def main(host: str = "0.0.0.0", port: int = 5007):
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
