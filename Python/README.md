# Handwriting Recognition (Python)

Tested on Python 3.6.7

Model accuracy when trained on EMNIST balanced dataset: 65.30%
NOTE: Except `k`, the default training parameters were used. To get better results, you can try changing the training parameters or some pre-processing.

## Dataset Creation

The model uses the extended MNIST dataset. To setup the dataset, run `python dataset.py`. To know the CLI options, append it with `-h` or `--help`.

## Model Training

To train the model, run `python model.py`. To know the CLI options, append it with `-h` or `--help`. The model is saved at `models/classifier.joblib`