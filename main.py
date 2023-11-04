import io

from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pytube import YouTube


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/file")
async def get_file(request: Request, link: str):
    mp3_stream = YouTube(link).streams.filter(only_audio=True).first()

    if mp3_stream.filesize / (1024 * 1024) > 10:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Max file size exceeded"}
        )

    buffer = io.BytesIO()
    mp3_stream.stream_to_buffer(buffer)
    buffer.seek(0)
    
    return StreamingResponse(
        status_code=status.HTTP_200_OK,
        media_type="audio/mpeg",
        content=buffer,
    )
