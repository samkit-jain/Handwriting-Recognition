# Handwriting Recognition

Software to recognize handwriting. Uses EMNIST dataset for training.

See [Python README](Python/README.md) for more details.

# Screenshots

## Python

<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/canvas.png" title="Canvas"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_5.png" title="Character identified as 5"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_E.png" title="Character identified as E"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_4.png" title="Character identified as 4"><br/>
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/label_5E4.png" title="Console output"><br/>

## Android

<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/screen21.png" width="300">
<img src="https://github.com/samkit-jain/Handwriting-Recognition/blob/master/Screenshots/image13.png" width="700">

# Checklist

- [x] Recognize digit
- [x] Recognize letter
- [x] Recognize multiple digits
- [x] Recognize multiple letters
- [ ] Recognize continuous handwriting
- [ ] Recognize different languages
- [x] Android app support

# How to run

For dataset creation - `python dataset.py`<br/>
For training - `python model.py`<br/>
For drawing and predicting - `python drawer.py`<br/>
For Android (**UNTESTED IN RELEASE 3.0**) - `python hr_py.py` then install `app_debug.apk` in your phone, open app, draw digit and click `Predict`

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
