FROM python:3.9

COPY . .
WORKDIR /
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD [ "uvicorn", "rokit_app.rokitAPI.main:app", "--host", "0.0.0.0", "--reload"]
