from fastapi import FastAPI

VERSION = "0.1.0"

app = FastAPI()


@app.get("/version")
async def read_version():
    return {"name:": "Templates Demo", "api_version": VERSION}
