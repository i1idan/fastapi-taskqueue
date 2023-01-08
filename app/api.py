
import logging
import tempfile
from fastapi import FastAPI, UploadFile, File
from fastapi.encoders import jsonable_encoder
from .worker.celery_tasks import upload_attachment_to_s3, clean_shared_volume
from datetime import datetime, timedelta

app = FastAPI()


@app.get("/")
def get():
    return {"Message": "Hello World!"}


@app.post("/")
async def get_file(file: UploadFile = File()):

    if not file.filename.endswith(".zip"):

        return jsonable_encoder({'status': '422',
                                 'message': 'File is not a zip file'})

    directory_path = tempfile.mkdtemp()
    file_location = f"{directory_path}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    upload_attachment_to_s3.delay(file_location)

    # example of scheduled task
    now = datetime.now()
    later = now + timedelta(minutes=1)
    clean_shared_volume.apply_async(args=(directory_path,), eta=later)

    return {"Status": "200"}
