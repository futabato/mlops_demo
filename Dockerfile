FROM centos:latest

RUN yum update -y && \
    yum install -y vim git lsof tree epel-release tmux libffi-devel python3 python3-pip python3-devel

WORKDIR home/

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

