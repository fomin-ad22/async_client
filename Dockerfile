FROM python:3.12.5

WORKDIR /API_WITH_AIOHTP_CLIENT

COPY requirements.txt /API_WITH_AIOHTP_CLIENT/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /API_WITH_AIOHTP_CLIENT/requirements.txt

COPY /server/main.py  server/
COPY /server/models.py  /API_WITH_AIOHTP_CLIENT/server
COPY /server/client.py  /API_WITH_AIOHTP_CLIENT/server
COPY /server/async_client.py  /API_WITH_AIOHTP_CLIENT/server

CMD [ "uvicorn","run","server/main.py"]
