# Handwriting Recognition (Python)

Tested on Python 3.6.7

Model accuracy when trained on EMNIST balanced dataset: 78.12%
NOTE: The default training parameters were used. To get better results, you can try changing the training parameters or maybe some pre-processing.

## Setup

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`

## Dataset Creation

The model uses the extended MNIST dataset. To setup the dataset, run `python dataset.py`. To know the CLI options, append it with `-h` or `--help`.

## Model Training

To train the model, run `python model.py`. To know the CLI options, append it with `-h` or `--help`. The model is saved at `models/classifier.joblib`