"""
Data preparation script for Fashion-MNIST.
Downloads dataset from tf.keras.datasets and saves raw numpy arrays.
"""
import os
import numpy as np
import tensorflow as tf

def prepare():
    raw_dir = os.path.join("data", "raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    print("Downloading Fashion-MNIST dataset...")
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
    
    print(f"Loaded train shapes: {x_train.shape}, {y_train.shape}")
    print(f"Loaded test shapes: {x_test.shape}, {y_test.shape}")
    
    np.save(os.path.join(raw_dir, "train_images.npy"), x_train)
    np.save(os.path.join(raw_dir, "train_labels.npy"), y_train)
    np.save(os.path.join(raw_dir, "test_images.npy"), x_test)
    np.save(os.path.join(raw_dir, "test_labels.npy"), y_test)
    
    print(f"Saved raw arrays successfully to {raw_dir}/")

if __name__ == "__main__":
    prepare()
