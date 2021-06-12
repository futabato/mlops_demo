FROM continuumio/miniconda3

ARG DEBIAN_FRONTEND="noninteractive"

RUN apt update -y && apt upgrade -y
RUN apt install -y python3-pip python3 python-dev
RUN apt clean
RUN rm -rf /var/cache/apr/archives/* /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install h5py==2.10.0
RUN pip3 install mlflow
RUN pip3 install tensorflow-cpu
RUN pip3 install keras
RUN pip3 install boto3

RUN mkdir -p /mlops-demo
WORKDIR /mlops-demo
