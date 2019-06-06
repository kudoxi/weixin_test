
FROM ubuntu:16.04
RUN apt-get -y update

RUN apt-get install -y python3.5
RUN apt-get install -y build-essential libssl-dev libffi-dev python3-dev
RUN apt-get -y update

#RUN cp /usr/bin/python /usr/bin/python_bak
#RUN rm /usr/bin/python
#RUN ln -s /usr/bin/python3.5 /usr/bin/python
RUN apt-get install -y python3-pip
#RUN apt-get install -y python-dev python-pip
#RUN apt-get install -y python-setuptools

ENV TIME_ZONE=Asia/Shanghai CODE_DIR=/code
ENV SPIDER=/weixin_test

RUN mkdir /weixin_test
WORKDIR /weixin_test
ADD . /weixin_test
          
RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE > /etc/timezone
RUN pip3 install -r requirements.txt
         
COPY requirements.txt /tmp/requirements.txt

#WORKDIR $CODE_DIR
VOLUME $CODE_DIR
EXPOSE 80 8080 8000 5000
