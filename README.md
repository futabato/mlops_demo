# mlops_demo

Manage machine learning experiments using MLflow and Hydra.

## Install

```
$ git clone https://github.com/futabato/mlops_demo
$ cd mlops_demo/
```

### pip install

```
$ pip install -r requirements.txt
```

### docker

```
$ docker build -t mlops_demo .
$ docker run --rm -it -v "${PWD}:/home" --name mlops_demo -p 5000:5000 -p 8888:8888 mlops_demo /bin/bash
```

## Hands-on

- `mlflow/`
  - mlflowを説明するためのコード。
- `hydra/`
  - hydraを説明するためのコード。
- `Integration/`
  - mlflowとhydraを組み合わせた実験管理を説明するためのコード。

## Launching the Tracking UI

```
$ mlflow ui
```

or

```
$ mlflow ui -h `hostname`
```

access <http://localhost:5000>

## Slide

<https://speakerdeck.com/futabato/mlflowtohydrawoli-yong-sitashi-yan-guan-li>  

