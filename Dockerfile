FROM python:3.12.2-slim

ENV BASE_PATH /server

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf requirements.txt

WORKDIR ${BASE_PATH}

CMD ["python", "server.py"]