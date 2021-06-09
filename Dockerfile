FROM python:3.8.5

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install h5py==2.10.0
RUN pip install mlflow
RUN pip install tensorflow-cpu

