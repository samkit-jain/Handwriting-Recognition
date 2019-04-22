import argparse
import cv2
import gzip
import numpy as np
import os
import pathlib
import requests
import shutil
import struct
import tempfile

from progress.bar import IncrementalBar


class DatasetGenerator:
    """
    Class to download and create dataset for training and testing.
    """

    # download URLs
    mnist_train_images_url = 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz'  # training set images
    mnist_train_labels_url = 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz'  # training set labels
    mnist_test_images_url = 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz'  # testing set images
    mnist_test_labels_url = 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'  # testing set labels

    def __init__(self, mnist: bool, nist: bool, download_path: str = '', data_path: str = ''):
        self.mnist = mnist
        self.nist = nist
        self.download_path = download_path
        self.data_path = data_path

        if not(self.download_path and self.download_path.strip()):
            self.download_path = 'download/'

        if not(self.data_path and self.data_path.strip()):
            self.data_path = 'data/'

        pathlib.Path(self.download_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.data_path).mkdir(parents=True, exist_ok=True)

    def create(self):
        if self.mnist:
            self.setup_mnist_dataset()

        if self.nist:
            # transform
            pass

    def setup_mnist_dataset(self):
        """
        Method to setup MNIST dataset
        """

        print(f'Downloading MNIST dataset\n')

        urls_file_map = {
            DatasetGenerator.mnist_train_images_url: '',
            DatasetGenerator.mnist_train_labels_url: '',
            DatasetGenerator.mnist_test_images_url: '',
            DatasetGenerator.mnist_test_labels_url: ''
        }

        for url in urls_file_map.keys():
            file_path = os.path.abspath(os.path.join(self.download_path, os.path.basename(url)))
            urls_file_map[url] = file_path

            # step 1: download
            DatasetGenerator.download_file(url=url, dest=file_path)

            # step 2: extract
            DatasetGenerator.extract_gz_file(gz_fp=file_path)

        # step 3: save
        self.idx_to_image(
            image_file=os.path.splitext(urls_file_map[DatasetGenerator.mnist_train_images_url])[0],
            label_file=os.path.splitext(urls_file_map[DatasetGenerator.mnist_train_labels_url])[0]
        )
        self.idx_to_image(
            image_file=os.path.splitext(urls_file_map[DatasetGenerator.mnist_test_images_url])[0],
            label_file=os.path.splitext(urls_file_map[DatasetGenerator.mnist_test_labels_url])[0]
        )

    @staticmethod
    def download_file(url, dest):
        """
        Method to download a file from url and save at dest
        """

        print(f'Downloading file from {url} and saving to {dest}')

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length'))
        chunk_size = 4096
        total_steps = int(total_size / chunk_size)
        progress_bar = IncrementalBar(max=total_steps, suffix='%(percent).1f%% - %(eta)ds')

        with open(dest, mode='wb') as fd:
            for chunk in response.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
                progress_bar.next()

        progress_bar.finish()

    @staticmethod
    def extract_gz_file(gz_fp):
        """
        Method to download a file from url and save at dest
        """

        print(f'Extracting {gz_fp}')

        with gzip.open(gz_fp, 'rb') as zipped:
            with open(os.path.splitext(gz_fp)[0], mode='wb') as unzipped:
                shutil.copyfileobj(zipped, unzipped)

    def idx_to_image(self, image_file, label_file):
        print(f'Converting {image_file} to image files')

        with open(image_file, mode='rb') as image_stream, open(label_file, mode='rb') as label_stream:
            # save images dataset
            magic, num_images = struct.unpack(">II", image_stream.read(8))

            if magic != 2051:
                raise ValueError('Magic number invalid')

            num_rows, num_cols = struct.unpack(">II", image_stream.read(8))
            images = np.fromfile(image_stream, dtype=np.dtype(np.uint8).newbyteorder('>'))
            images = images.reshape((num_images, num_rows, num_cols))

            # save labels dataset
            magic, num_labels = struct.unpack(">II", label_stream.read(8))

            if magic != 2049:
                raise ValueError('Magic number invalid')

            labels = np.fromfile(label_stream, dtype=np.dtype(np.uint8).newbyteorder('>'))

            # save images to data directory
            for label, image in zip(labels, images):
                label_folder = os.path.abspath(os.path.join(self.data_path, str(label)))
                pathlib.Path(label_folder).mkdir(parents=True, exist_ok=True)
                image_dest = tempfile.mktemp(dir=label_folder, suffix='.png')

                cv2.imwrite(f'{image_dest}', image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Script to download and create training data from MNIST or NIST images.
            """,
        usage='%(prog)s [options]',
    )
    parser.add_argument(
        '-dop',
        '--download-path',
        dest='download_path',
        type=str,
        help='Path where dataset should be downloaded.',
    )
    parser.add_argument(
        '-dap',
        '--data-path',
        dest='data_path',
        type=str,
        help='Path where dataset images should be saved.',
    )
    parser.add_argument(
        '-m',
        '--mnist',
        dest='mnist',
        action='store_true',
        default=False,
        help='Download and create training dataset with images from MNIST dataset.',
    )
    parser.add_argument(
        '-n',
        '--nist',
        dest='nist',
        default=False,
        action='store_true',
        help='Download and create training dataset with images from NIST dataset.',
    )
    args = parser.parse_args()

    creator = DatasetGenerator(mnist=args.mnist,
                               nist=args.nist,
                               download_path=args.download_path,
                               data_path=args.data_path)
    creator.create()
