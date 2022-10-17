FROM tiangolo/uvicorn-gunicorn:python3.9

RUN apt-get update

WORKDIR /code

ADD app/requirements.txt /code/requirements.txt
ADD .env /code/.env

RUN pip install  -r /code/requirements.txt
RUN pip install "uvicorn[standard]" gunicorn
RUN pip3 install --upgrade pip


CMD gunicorn app.api:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 