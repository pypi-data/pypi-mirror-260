FROM python:3.11

WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

COPY komodo /code/komodo/
COPY sample /code/sample/

EXPOSE 8042
CMD ["uvicorn", "sample.server:SAMPLE_APP", "--host", "0.0.0.0", "--port", "8042", "--reload"]
