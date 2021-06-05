import os
import mlflow

mlflow.start_run()

mlflow.log_param("param1", 5)

mlflow.log_metric("foo", 1)
mlflow.log_metric("foo", 2)
mlflow.log_metric("foo", 3)

with open("output.txt", "a") as f:
    f.write("Hello")

mlflow.log_artifact("output.txt")

mlflow.end_run()
