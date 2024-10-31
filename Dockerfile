FROM python:3.12.5

WORKDIR /api_with_aiohtp_client

COPY requirements.txt /api_with_aiohtp_client/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api_with_aiohtp_client/requirements.txt

COPY /server/main.py  server/
COPY /server/models.py  server/
COPY /server/client.py  server/
COPY /server/async_client.py  server/

CMD ["fastapi","run","server/main.py","--port","8000"]
