FROM python:latest

WORKDIR /usr/local/bin

COPY api_flask.py .
COPY requirements.txt .

COPY templates/ /usr/local/bin/templates
COPY static/ /usr/local/bin/static

RUN pip install -r requirements.txt

RUN ls -laR /usr/local/bin/templates/*
RUN ls -laR /usr/local/bin/static/*


COPY . .
EXPOSE 5100
EXPOSE 8000

CMD ["python3", "api_flask.py"]

