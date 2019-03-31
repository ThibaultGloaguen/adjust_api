FROM python:3.7
ADD requirements.txt /code/
WORKDIR /code
VOLUME /code
ENV PYTHONPATH "${PYTHONPATH}:/code"
RUN pip install -r requirements.txt
ADD . /code
