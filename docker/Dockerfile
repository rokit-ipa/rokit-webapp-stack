FROM python:3
WORKDIR /

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "FastAPI.main:app --reload", "--host", "0.0.0.0", "--port", "80" ]