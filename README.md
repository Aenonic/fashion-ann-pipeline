# Fashion-MNIST ANN Pipeline with Git, DVC & Google Drive Storage

An end-to-end Machine Learning versioning workflow utilizing TensorFlow 2, Git, DVC (Data Version Control), and Google Drive remote storage.

## Project Overview
This project builds, versions, and reproduces a fully-connected Artificial Neural Network (ANN) classifying 28x28 Fashion-MNIST images into 10 categories, targeting >= 85% test accuracy.

## Architecture & Pipeline
- `src/prepare.py`: Downloads Fashion-MNIST dataset and stores raw numpy arrays.
- `src/preprocess.py`: Normalizes image arrays and performs train/validation splitting.
- `src/train.py`: Trains sequential ANN (Flatten -> Dense ReLU -> Dropout -> Dense Softmax).
- `src/evaluate.py`: Evaluates test accuracy, logs `metrics.json`, and outputs confusion matrix.
- `params.yaml`: Single source of truth for pipeline hyperparameters.
- `dvc.yaml`: Stage dependency and metric tracking pipeline.

## Reproduction
```bash
dvc repro
```
