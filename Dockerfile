FROM python:latest
WORKDIR .
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python","app.py"]