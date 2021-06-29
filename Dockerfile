FROM continuumio/miniconda3

ARG DEBIAN_FRONTEND="noninteractive"

RUN mkdir /mlops-demo
ARG $project_dir

RUN apt update -y && apt upgrade -y
RUN apt install -y python3-pip python3 python-dev
RUN apt clean
RUN rm -rf /var/cache/apr/archives/* /var/lib/apt/lists/*

ADD requirements.txt $project_dir
ADD exp/ $project_dir
ADD hydra/ $project_dir
ADD mlflow/ $project_dir
ADD README.md $project_dir

#WORKDIR $project_dir

RUN pip install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

