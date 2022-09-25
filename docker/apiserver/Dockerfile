FROM python:3.10-alpine

RUN mkdir -p /opt/xfuzz
WORKDIR /opt/xfuzz

COPY ../../dev.requirements.txt .
COPY ../../requirements.txt .

RUN apk add --no-cache --virtual build-deps build-base musl-dev && \
        python3 -m pip install --no-cache-dir -r dev.requirements.txt && \
        apk del build-deps

CMD [ "python3", "-m", "uvicorn", "test.interactive:server", "--port", "5000", "--host", "0.0.0.0" ]
