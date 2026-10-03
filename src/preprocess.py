"""
Data preprocessing script for Fashion-MNIST.
Normalizes pixel values to [0, 1] and splits training data into train/val sets.
"""
import os
import yaml
import numpy as np
from sklearn.model_selection import train_test_split

def preprocess():
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    
    val_size = float(params["preprocess"]["test_size"])
    seed = int(params["preprocess"]["seed"])
    
    raw_dir = os.path.join("data", "raw")
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    print(f"Loading raw arrays from {raw_dir}/...")
    train_images = np.load(os.path.join(raw_dir, "train_images.npy"))
    train_labels = np.load(os.path.join(raw_dir, "train_labels.npy"))
    test_images = np.load(os.path.join(raw_dir, "test_images.npy"))
    test_labels = np.load(os.path.join(raw_dir, "test_labels.npy"))
    
    # Teammate normalization: Zero-centered [-1, 1] normalization
    train_images = (train_images.astype("float32") - 128.0) / 128.0
    test_images = (test_images.astype("float32") - 128.0) / 128.0
    
    # Split train into train and validation sets
    x_train, x_val, y_train, y_val = train_test_split(
        train_images,
        train_labels,
        test_size=val_size,
        random_state=seed,
        stratify=train_labels
    )
    
    print(f"Processed train set: {x_train.shape}, labels: {y_train.shape}")
    print(f"Processed val set: {x_val.shape}, labels: {y_val.shape}")
    print(f"Processed test set: {test_images.shape}, labels: {test_labels.shape}")
    
    np.save(os.path.join(processed_dir, "train_images.npy"), x_train)
    np.save(os.path.join(processed_dir, "train_labels.npy"), y_train)
    np.save(os.path.join(processed_dir, "val_images.npy"), x_val)
    np.save(os.path.join(processed_dir, "val_labels.npy"), y_val)
    np.save(os.path.join(processed_dir, "test_images.npy"), test_images)
    np.save(os.path.join(processed_dir, "test_labels.npy"), test_labels)
    
    print(f"Saved processed arrays successfully to {processed_dir}/")

if __name__ == "__main__":
    preprocess()
