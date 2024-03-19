FROM python:3.12.2-slim

COPY . /src

WORKDIR /src

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf requirements.txt

RUN python run_codegen.py

CMD ["python", "main.py"]