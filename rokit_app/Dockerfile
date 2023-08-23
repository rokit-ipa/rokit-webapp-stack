FROM python:3.9
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./rokit_app ./rokit_app
WORKDIR /
CMD [ "uvicorn", "rokit_app.rokitAPI.main:app", "--host", "0.0.0.0", "--port", "8000"]

