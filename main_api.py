from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from Dobot_full import start_process 
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os


app = FastAPI()

executor = ThreadPoolExecutor()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_files_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_files_dir), name="static")


async def run_in_threadpool(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(executor, lambda: func(*args, **kwargs))

# Endpoint to serve the web page.
@app.get("/", response_class=HTMLResponse)
async def get():
    with open('index.html', 'r') as file:
        content = file.read()
    return HTMLResponse(content=content)

# Endpoint to start detection and movement of the Dobot.

@app.get("/start-detection/")
async def start_detection():
    try:
        await run_in_threadpool(start_process)
        return {"message": "Detection successfully initiated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
