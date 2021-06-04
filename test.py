import os
from mlflow import *

if __name__ == "__main__":
    log.param("param1", 5)

    log.metric("foo", 1)
    log.metric("foo", 2)
    log.metric("foo", 3)

    with open("output.txt") as f:
        f.write("Hello")
    log.artifact("output.txt")
