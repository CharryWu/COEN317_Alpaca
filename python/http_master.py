from typing import *

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

favicon_path = 'favicon.ico'

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}/{product_id}/")
def read_item(item_id: int, product_id:int):
    return {"item_id": item_id, "product_id": product_id}