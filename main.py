from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import JSONResponse
from spotify import *

app = FastAPI()

@app.get('/analyze')
async def analyze(track_id: str):
    track_info = get_analysis(track_id)
    data = analyze_track(track_info)
    colors = analyze_album_cover(track_id)
    return JSONResponse(content={
        "analysis": data,
        "colors": colors
    })

@app.get('/get_track')
async def get_track(track_name: str):
    return JSONResponse(content=get_id_from_name(track_name))

@app.get("/")
async def root():
    return "I'm a teapot"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)