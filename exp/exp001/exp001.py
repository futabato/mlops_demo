import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist

import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME
import mlflow.keras
import hydra

import os

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
    # hydraを使おうとするとcurrent directoryが変更されてしまうので、以下の設定が必要。
    mlflow.set_tracking_uri("file://" + hydra.utils.get_original_cwd() + "/mlruns")
    
    # 実験番号のロード
    experiment_name = cfg.model.exp.number
    mlflow.set_experiment(experiment_name)
    
    # dataの用意。abciのパスをyamlに書くことになりそう。
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train, X_valid = X_train[5000:], X_train[:5000]
    y_train, y_valid = y_train[5000:], y_train[:5000]
    X_train, X_valid = X_train /255, X_valid /255

    # mlflowに記録を始めさせる
    mlflow.start_run(run_name=experiment_name)
    mlflow.keras.autolog()
    
    # configからのロード
    loss = cfg.model.training.loss
    optimizer = cfg.model.training.optimizer
    metrics = cfg.model.training.metrics
    epoch = cfg.model.training.epoch
    batch_size = cfg.model.training.batch_size

    model = create_model(loss, optimizer, metrics)
    test_loss, test_accuracy = train(model, epoch, batch_size, X_train, y_train, X_valid, y_valid, X_test, y_test)
    
    # mlflow周りの保存
    mlflow.log_param("loss", loss)
    mlflow.log_param("optimizer", optimizer)
    mlflow.log_param("metrics", metrics)
    mlflow.log_param("epoch", epoch)
    mlflow.log_param("batch_size", batch_size)

    mlflow.log_metrics({'loss': test_loss})
    mlflow.log_metrics({'accuracy': test_accuracy})    
    
    #mlflow.keras.log_model(model, cfg.exp.number)
    
    # hydraのyamlの保存
    mlflow.log_artifact('.hydra/config.yaml')
    mlflow.log_artifact('.hydra/hydra.yaml')
    mlflow.log_artifact('.hydra/overrides.yaml')

    mlflow.end_run()

if __name__ == "__main__":
    main()
