
from fastapi import FastAPI
from .worker.celery_tasks import sample_task
from pydantic import BaseModel


class Item(BaseModel):
    num: int


app = FastAPI()


@app.get("/")
def get():
    return {"Message": "Hello World!"}


@app.post("/")
async def get_body(item: Item):
    sample_task.delay(item.num)
    return {"Status": "200"}