FROM continuumio/anaconda

MAINTAINER QCR

ADD . /src

# RUN apt-get clean && apt-get update
# RUN apt-get install -y build-essential g++

RUN cd /src; wget https://gist.githubusercontent.com/bkj/df4faceba8b0adc81df83bd8777bfd5f/raw/generic-app.py

RUN cd /src; pip install -r requirements.txt

EXPOSE 5000

RUN chmod -x /src/launch.sh
CMD sh /src/launch.sh

