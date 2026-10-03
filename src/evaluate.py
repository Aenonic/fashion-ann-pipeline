"""
Model evaluation script for Fashion-MNIST ANN.
Computes test loss and accuracy, generates confusion matrix image,
and writes evaluation metrics to metrics.json at project root.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import tensorflow as tf

CLASS_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

def evaluate():
    processed_dir = os.path.join("data", "processed")
    model_path = os.path.join("models", "model.h5")
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    print(f"Loading trained model from {model_path}...")
    model = tf.keras.models.load_model(model_path)
    
    print("Loading test data...")
    test_images = np.load(os.path.join(processed_dir, "test_images.npy"))
    test_labels = np.load(os.path.join(processed_dir, "test_labels.npy"))
    
    print("Evaluating model performance on test set...")
    loss, accuracy = model.evaluate(test_images, test_labels, verbose=1)
    print(f"Test Loss: {loss:.4f}, Test Accuracy: {accuracy:.4f}")
    
    # Generate predictions & confusion matrix
    y_pred_probs = model.predict(test_images)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    cm = confusion_matrix(test_labels, y_pred)
    
    # Plot confusion matrix
    fig, ax = plt.subplots(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASS_NAMES)
    disp.plot(cmap=plt.cm.Blues, ax=ax, xticks_rotation=45)
    plt.title(f"Fashion-MNIST Confusion Matrix (Accuracy: {accuracy*100:.2f}%)")
    plt.tight_layout()
    
    cm_path = os.path.join(reports_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Confusion matrix saved to {cm_path}")
    
    # Write metrics.json at root
    metrics = {
        "test_loss": float(loss),
        "test_accuracy": float(accuracy)
    }
    
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
    print("Metrics written successfully to metrics.json")

if __name__ == "__main__":
    evaluate()
