FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN apk add build-base libffi-dev
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]
