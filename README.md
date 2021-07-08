## install

```
$ git clone https://github.com/futabato/mlops-demo
$ cd $_
```

### pip install

```
$ pip install -r requirements.txt
```

### docker

```
$ docker build -t mlops_demo .
$ docker run --rm -it -v "${PWD}:/home" --name mlops_demo -p 5000:5000 mlops_demo /bin/bash
```

- mlflow/
  - mlflowを説明するために必要な最小限のコード
- hydra/
  - hydraを説明するために必要な最小限のコード
- exp/
  - mlflowとhydraを組み合わせて実験管理を行うための最小限のコード

