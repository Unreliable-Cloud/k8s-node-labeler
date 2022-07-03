FROM python:3.9.12-alpine3.15

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
RUN chmod +x ./app.py

CMD [ "ddtrace-run", "python", "./app.py" ]
