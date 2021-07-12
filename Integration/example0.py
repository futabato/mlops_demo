import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist

import mlflow
import hydra

import os

def load_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    X_train, X_valid = X_train[5000:], X_train[:5000]
    y_train, y_valid = y_train[5000:], y_train[:5000]
    X_train, X_valid = X_train /255, X_valid /255
    return (X_train, y_train), (X_valid, y_valid), (X_test, y_test)

def create_model(loss, optimizer, metrics, maps):
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=[28, 28]))
    model.add(keras.layers.Dense(maps, activation='relu'))
    model.add(keras.layers.Dense(maps, activation='relu'))
    model.add(keras.layers.Dense(10, activation='softmax'))
    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return model

def train(model, training_data, validation_data, test_data, epoch, batch_size):
    history = model.fit(training_data[0], training_data[1], epochs=epoch, batch_size=batch_size, validation_data=(validation_data))
    test_loss, test_accuracy = model.evaluate(test_data[0], test_data[1])
    return test_loss, test_accuracy

@hydra.main(config_path="conf", config_name="config")
def main(cfg):
    # hydraを使おうとするとworking directoryが変更されてしまうので、以下の設定が必要。
    mlflow.set_tracking_uri("file://" + hydra.utils.get_original_cwd() + "/mlruns")

    # Experimetの指定
    experiment_name = cfg.setting.experiment
    mlflow.set_experiment(experiment_name)

    # 実験番号の指定
    run_name = cfg.setting.run_name

    # mlflowに記録を始めさせる
    with mlflow.start_run(run_name=run_name):
        # Auto Logging
        mlflow.tensorflow.autolog()

        # configからのロード
        loss = cfg.model.training.loss
        optimizer = cfg.model.training.optimizer
        metrics = cfg.model.training.metrics
        epoch = cfg.model.training.epoch
        batch_size = cfg.model.training.batch_size

        maps = cfg.model.model.maps
        dataset = cfg.data

        training_data, validation_data, test_data = load_data()
        model = create_model(loss, optimizer, metrics, maps)
        test_loss, test_accuracy = train(model, training_data, validation_data, test_data, epoch, batch_size)

        # working directoryは`./output/日付/時間/に変更されているためこのパスの指定で良い`
        mlflow.log_artifact('.hydra/config.yaml')
        mlflow.log_artifact('.hydra/hydra.yaml')
        mlflow.log_artifact('.hydra/overrides.yaml')

if __name__ == "__main__":
    main()
