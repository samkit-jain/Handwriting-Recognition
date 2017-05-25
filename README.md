# Handwriting Recognition

Software to recognize handwriting.


# Screenshots

<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/Handwritten%20Character%20Recognition.png" width="500"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/Handwritten%20Character%20Recognition%20(1).png" width="500"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/Handwritten%20Character%20Recognition%20(2).png" width="500">


# Stats (Digit)

Dataset used - <a href="http://yann.lecun.com/exdb/mnist/">MNIST</a>  
Algorithm - Support Vector Machines (kernel = linear)<br/>
Training time - 1,036.442 seconds<br/>
Prediction time - 1,636.704 seconds<br/>
Accuracy - 96.92%


# Stats (Letter)

Dataset used - <a href="https://www.nist.gov/srd/nist-special-database-19">NIST</a><br/>
Algorithm - k-Nearest Neighbours (k = 165)<br/>
Training time - 8 seconds<br/>
Testing time - 1,340 seconds<br/>
Accuracy - 74.13%


# Checklist

- [x] Recognize digit
- [x] Recognize letter
- [x] Recognize multiple digits
- [x] Recognize multiple letters
- [ ] Recognize handwriting
- [ ] Recognize different languages
- [x] Android app support


# How to run

For digit - `python digit_recognition.py`<br/>
For letter - `python letter_recognition.py`<br/>
For Android - `python hr_py.py` then install `app_debug.apk` in your phone, open app, draw digit and click `Predict`


# Files info

`android_rec.py` - Helper script. Receives as input the image from `hr_py.py` and returns the predicted digit<br/>

`digit_recognition.py` - The main script to interact with the user. Gives the option of recognizing a digit, training the model, testing the model and visualizing the dataset. Linear SVM is used to train the model and the model is saved in a pickle file that can be called again to test the model without having to train the model again and again. Selecting the  “Recognise digit” option opens up a Tkinter window where the user can draw multiple digits and get the predicted value.<br/>

`letter_recognition.py` - The main script to interact with the user. Gives the option of  recognizing a letter and testing the model. k-Nearest Neighbors with neighbors = 165 is used to train the model and the model is saved in a pickle file that can be called again to test the model without having to train the model again and again. Calling the “Recognise letter” option opens up a Tkinter window where the user can draw multiple letters and get the predicted value.<br/>

`extract_font (NIST).py` - Script to extract raw images of the NIST dataset and convert them to comply with the MNIST dataset configuration.<br/>

`extract_font (TTF).py` - Script to extract raw images from the font dataset and convert them to comply with the MNIST dataset configuration.<br/>

`hr_py.py` - Python script that creates a local server. The Android app when run on the phone sends the user drawn digit to the server and the server downloads it. The image is then passed to the ​android_rec.py ​which converts it to a 28x28 pixel image and returns back the result.<br/>

`painte.py` - Helper class involved with setting up the UI. Setups the Tkinter window, waits for user to draw the digit or letter, converts the image and returns it.<br/>

`MainActivity.java` - The single Java file of the Android app that creates the UI, waits for user to draw the image, connects with the server, sends the image to the server.


# License

Copyright 2016 Samkit Jain

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
