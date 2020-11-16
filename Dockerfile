FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN pytest --it --cov=. tests/ --benchmark-histogram