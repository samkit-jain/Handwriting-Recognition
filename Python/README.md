# Handwriting Recognition (Python)

Tested on Python 3.6.7

Model accuracy when trained on EMNIST balanced dataset: 78.14%
NOTE: The default training parameters were used. To get better results, you can try changing the training parameters or maybe some pre-processing.

## Setup

1. Create a virtual environment
2. Install dependencies: `pip install -r requirements.txt`

## Dataset Creation

The model uses the extended MNIST dataset. To setup the dataset, run `python dataset.py`. To know the CLI options, append it with `-h` or `--help`.

## Model Training

To train the model, run `python model.py`. To know the CLI options, append it with `-h` or `--help`. The model is saved at `models/classifier.joblib`.

## Model application

Run `python drawer.py`. It will open a window. Draw the characters over there and **press ESC key to close the window**. It will then run predictions on the characters drawn and publish result to console and display the image in a window with it's title being the predicted label. **Press ESC key to close the window and run predictions on next image.**

## Screenshots

<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/canvas.png" title="Canvas"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_5.png" title="Character identified as 5"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_E.png" title="Character identified as E"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_4.png" title="Character identified as 4"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_5E4.png" title="Console output"><br/>