FROM python:3.9.12-alpine3.15

RUN adduser -D nodelabeler
WORKDIR /usr/src/app
COPY --chown=nodelabeler:nodelabeler requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=nodelabeler:nodelabeler app.py ./
RUN chmod +x ./app.py

USER nodelabeler

CMD [ "python", "./app.py" ]