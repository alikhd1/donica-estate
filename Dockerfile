FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./count.txt /code/count.txt
COPY ./fake_data.py /code/fake_data.py

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["python", "fake_data.py"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]
