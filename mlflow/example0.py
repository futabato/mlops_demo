import mlflow

mlflow.set_experiment('minimum_mlflow')

with mlflow.start_run(run_name='minimum_mlflow'):

    mlflow.log_param("param1", 5)

    mlflow.log_metric("foo", 1)
    mlflow.log_metric("foo", 2)
    mlflow.log_metric("foo", 3)

    with open("output.txt", "a") as f:
        f.write("Hello, MLflow!")

    mlflow.log_artifact("output.txt")

