FROM python:3.10.12

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

CMD [ "fastapi", "run", "app/main.py" ]