FROM python:3.6-slim

RUN mkdir /opt/estimator

WORKDIR /opt/estimator

ADD . .

RUN pip install -r prod_requirements.txt

EXPOSE 5000

ENV FLASK_APP=run.py

CMD ["flask", "run", "--host", "0.0.0.0"]
