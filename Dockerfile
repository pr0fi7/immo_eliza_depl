FROM python:3.9-slim

WORKDIR /immo-eliza-deployment

COPY requirements.txt .
COPY ./src ./src



RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "./src/main.py"]
