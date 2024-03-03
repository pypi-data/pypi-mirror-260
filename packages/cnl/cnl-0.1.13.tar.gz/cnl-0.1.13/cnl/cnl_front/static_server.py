import os
from importlib import resources

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# STATIC_FILES_DIR = resources.files("cnl_front").joinpath("static")
STATIC_FILES_DIR = (
    "/Users/philip/Documents/projects/cnl/cnl_reconciled/cnl/cnl_front/static"
)


@app.get("/")
async def serve_index():
    return FileResponse(f"{STATIC_FILES_DIR}/index.html")


@app.get("/{slug:path}")
async def main_web(slug: str):
    # serve static file
    if "." in slug.split("/")[-1]:
        return FileResponse(f"{STATIC_FILES_DIR}/{slug}")
    # serve html page
    file_path = f"{STATIC_FILES_DIR}/{slug}.html"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse(
            f"{STATIC_FILES_DIR}/404.html",
            status_code=404,
        )


# https://nextjs.org/docs/app/building-your-application/deploying/static-exports#deploying
