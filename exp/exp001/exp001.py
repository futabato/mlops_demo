import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist

import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME
import mlflow.keras
import hydra

def create_model(loss, optimizer, metrics):
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=[28, 28]))
    model.add(keras.layers.Dense(300, activation='relu'))
    model.add(keras.layers.Dense(300, activation='relu'))
    model.add(keras.layers.Dense(10, activation='softmax'))
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return model

def train(model, epoch, batch_size, X_train, y_train, X_valid, y_valid, X_test, y_test):
    history = model.fit(X_train, y_train, epochs=epoch, batch_size=batch_size, validation_data=(X_valid, y_valid))
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    return test_loss, test_accuracy


@hydra.main(config_path="conf", config_name="config")
def main(cfg):
    # 実験番号のロード
    experiment_name = cfg.exp.number
    mlflow.set_experiment(experiment_name)

    remote_server_uri = 'http://127.0.0.1:5000'
    mlflow.set_tracking_uri(remote_server_uri) 

    elastic_ip_uri = 'http://107.22.178.5:5000'
    #mlflow.set_tracking_uri(elastic_ip_uri) 

    # dataの用意。abciのパスをyamlに書くことになりそう。
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train, X_valid = X_train[5000:], X_train[:5000]
    y_train, y_valid = y_train[5000:], y_train[:5000]
    X_train, X_valid = X_train /255, X_valid /255

    # mlflowに記録を始めさせる
    with mlflow.start_run(run_name=experiment_name):

        # configからのロード
        loss = cfg.training.loss
        optimizer = cfg.training.optimizer
        metrics = cfg.training.metrics
        epoch = cfg.training.epoch
        batch_size = cfg.training.batch_size

        model = create_model(loss, optimizer, metrics)
        
        mlflow.keras.autolog()
        test_loss, test_accuracy = train(model, epoch, batch_size, X_train, y_train, X_valid, y_valid, X_test, y_test)
        
        #model.fit(X_train, y_train, epochs=epoch, batch_size=batch_size, validation_data=(X_valid, y_valid))
        
        # mlflow周りの保存
        mlflow.log_param("loss", loss)
        mlflow.log_param("optimizer", optimizer)
        mlflow.log_param("metrics", metrics)
        mlflow.log_param("epoch", epoch)
        mlflow.log_param("batch_size", batch_size)

        mlflow.log_metrics({'loss': test_loss})
        mlflow.log_metrics({'accuracy': test_accuracy})    
        
        mlflow.keras.log_model(model, cfg.exp.number)
        
        # hydraのyamlの保存
        mlflow.log_artifact('.hydra/config.yaml')
        mlflow.log_artifact('.hydra/hydra.yaml')
        mlflow.log_artifact('.hydra/overrides.yaml')

if __name__ == "__main__":
    main()