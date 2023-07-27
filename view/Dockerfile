FROM python:3.9

COPY . .
WORKDIR /
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "view.rokitAPI.main:app", "--host", "0.0.0.0"]
