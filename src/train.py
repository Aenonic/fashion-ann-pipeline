"""
Model training script for Fashion-MNIST ANN.
Builds Sequential ANN: Flatten -> Dense (ReLU) -> Dropout -> Dense(10, Softmax).
Saves trained model to models/model.h5 and training history to models/history.csv.
"""
import os
import yaml
import numpy as np
import pandas as pd
import tensorflow as tf

def train():
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    
    dense_units = int(params["train"]["dense_units"])
    dropout_rate = float(params["train"]["dropout_rate"])
    learning_rate = float(params["train"]["learning_rate"])
    epochs = int(params["train"]["epochs"])
    batch_size = int(params["train"]["batch_size"])
    
    processed_dir = os.path.join("data", "processed")
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    print("Loading preprocessed training and validation data...")
    x_train = np.load(os.path.join(processed_dir, "train_images.npy"))
    y_train = np.load(os.path.join(processed_dir, "train_labels.npy"))
    x_val = np.load(os.path.join(processed_dir, "val_images.npy"))
    y_val = np.load(os.path.join(processed_dir, "val_labels.npy"))
    
    print(f"Building Sequential ANN: Flatten -> Dense({dense_units}, ReLU) -> Dropout({dropout_rate}) -> Dense(10, Softmax)")
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(dense_units, activation="relu"),
        tf.keras.layers.Dropout(dropout_rate),
        tf.keras.layers.Dense(10, activation="softmax")
    ])
    
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    model.summary()
    
    print(f"Training for {epochs} epochs with batch size {batch_size}...")
    history = model.fit(
        x_train,
        y_train,
        validation_data=(x_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )
    
    # Save model and history
    model_path = os.path.join(models_dir, "model.h5")
    history_path = os.path.join(models_dir, "history.csv")
    
    model.save(model_path)
    pd.DataFrame(history.history).to_csv(history_path, index=False)
    
    print(f"Model saved to {model_path}")
    print(f"History saved to {history_path}")

if __name__ == "__main__":
    train()
