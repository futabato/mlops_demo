import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NAME

experiment_name = 'exp001'
mlflow.set_experiment(experiment_name)

mlflow.set_tag(MLFLOW_RUN_NAME, 'mnist_classification')

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train, X_valid = X_train[5000:], X_train[:5000]
y_train, y_valid = y_train[5000:], y_train[:5000]
X_train, X_valid = X_train /255, X_valid /255

with mlflow.start_run(run_name='three-layers-network', nested=True):
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=[28, 28]))
    model.add(keras.layers.Dense(300, activation='relu'))
    model.add(keras.layers.Dense(300, activation='relu'))
    model.add(keras.layers.Dense(10, activation='softmax'))

    loss = 'sparse_categorical_crossentropy'
    optimizer = 'adam'
    metrics = ['accuracy']
    epoch = 30
    batch_size = 128

    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    model.fit(X_train, y_train, epochs=epoch, batch_size=batch_size, validation_data=(X_valid, y_valid))

    mlflow.log_param("loss", loss)
    mlflow.log_param("optimizer", optimizer)
    mlflow.log_param("metrics", metrics)
    mlflow.log_param("epoch", epoch)
    mlflow.log_param("batch_size", batch_size)

    test_loss, test_accuracy = model.evaluate(X_test, y_test)

    mlflow.log_metrics({'loss': test_loss})
    mlflow.log_metrics({'accuracy': test_accuracy})

    mlflow.keras.log_model(model, 'three-layers-network')
