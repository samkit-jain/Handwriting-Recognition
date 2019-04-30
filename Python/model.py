import argparse
import cv2
import imghdr
import numpy as np
import os
import pathlib

from halo import Halo
from joblib import dump, load
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler


class Model:
    def __init__(self, data_dir_path: str = '', skip_evaluation: bool = False):
        self.skip_evaluation = skip_evaluation
        self.data_dir_path = data_dir_path

        if not(self.data_dir_path and self.data_dir_path.strip()):
            self.data_dir_path = 'data/'

        models_dir_path = os.path.abspath('models/')
        pathlib.Path(models_dir_path).mkdir(parents=True, exist_ok=True)

        self.joblib_path = os.path.join(models_dir_path, 'classifier.joblib')

    def predict(self, img):
        """
        Method to run prediction on a single image.
        """

        clf = load(self.joblib_path)

        img = np.dot(img[..., :3], [0.299, 0.587, 0.114])
        img = img.flatten()

        label = clf.predict([img])[0]
        print(f'Image predicted to be: {label}')

        return label

    def read_dataset(self):
        """
        Method to read image dataset in numpy array for training the model.

        The structure of the data dir at `data_dir_path` should be:
            data
            ├── a
            |   ├── 1.png
            |   ├── 2.png
            |   └── ...
            ├── b
            |   ├── 1.png
            |   ├── 2.png
            |   └── ...
            └── ...

        Sub directory name is the name of the label and contains MNIST format compliant handwritten images
        of the character denoted by that label.
        """

        base_sep_count = self.data_dir_path.count(os.sep)
        features = []
        labels = []

        spinner = Halo(text='Reading', spinner='dots')
        spinner.start()

        for subdir, dirs, files in os.walk(self.data_dir_path, topdown=True):
            # go only 2 levels deep
            if subdir.count(os.sep) - base_sep_count == 1:
                del dirs[:]
                continue

            for filename in files:
                filepath = os.path.join(subdir, filename)

                if imghdr.what(filepath) == 'png':
                    labels.append([os.path.basename(os.path.dirname(filepath))])

                    name_im = cv2.imread(filename=filepath)
                    name_im = np.dot(name_im[..., :3], [0.299, 0.587, 0.114])
                    name_im = name_im.flatten()

                    features.append(list(name_im))

        spinner.succeed(text='Finished reading')

        features = np.array(features)
        labels = np.array(labels).ravel()

        return features, labels

    def train(self):
        """
        Method to train a kNN classifier.
        """

        # step 1: get the dataset
        x, y = self.read_dataset()

        # split into training and testing
        features_train, features_test, labels_train, labels_test = train_test_split(x, y, test_size=0.2, random_state=0)

        spinner = Halo(text='Training', spinner='dots')
        spinner.start()

        # step 2: train the model
        pipeline_knn_clf = Pipeline([('scaler', MinMaxScaler()), ('classifier', KNeighborsClassifier())])
        pipeline_knn_clf.fit(features_train, labels_train)

        spinner.succeed(text='Finished training')

        if self.skip_evaluation:
            print('Skipping running evaluation')

        else:
            spinner = Halo(text='Evaluating', spinner='dots')
            spinner.start()

            # step 3: evaluate the model
            labels_pred = pipeline_knn_clf.predict(features_test)
            score = accuracy_score(labels_test, labels_pred)

            spinner.succeed(text='Finished evaluation')

            print(f'Accuracy (max=1.0): {score}')

        # persist model
        dump(pipeline_knn_clf, self.joblib_path)

        print(f'Model saved at {self.joblib_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Script to train a kNN Classifier model.
            """,
        usage='%(prog)s [options]',
    )
    parser.add_argument(
        '-dap',
        '--data-path',
        dest='data_path',
        type=str,
        help='Path where dataset images are saved.',
    )
    parser.add_argument(
        '-se',
        '--skip-evaluation',
        dest='skip_evaluation',
        action='store_true',
        default=False,
        help='Whether to skip running evaluations or not.',
    )
    args = parser.parse_args()

    model = Model(data_dir_path=args.data_path, skip_evaluation=args.skip_evaluation)
    model.train()
