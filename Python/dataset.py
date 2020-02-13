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
import zipfile

from os import path as osp
from progress.bar import IncrementalBar
from typing import Dict


class DatasetGenerator:
    """
    Class to download and create dataset for training and testing.
    """

    # link to download EMNIST dataset
    emnist_dataset_url = 'https://www.itl.nist.gov/iaui/vip/cs_links/EMNIST/gzip.zip'

    def __init__(self, balanced: bool = True, download_dir_path: str = '', data_dir_path: str = ''):
        self.balanced = balanced  # whether to use the balanced dataset or not
        self.download_dir_path = download_dir_path
        self.data_dir_path = data_dir_path

        if not(self.download_dir_path and self.download_dir_path.strip()):
            self.download_dir_path = osp.abspath('download/')

        if not(self.data_dir_path and self.data_dir_path.strip()):
            self.data_dir_path = osp.abspath('data/')

        pathlib.Path(self.download_dir_path).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.data_dir_path).mkdir(parents=True, exist_ok=True)

    def create(self):
        """
        Method to setup EMNIST dataset.
        
        Note: When saving to data dir, existing data is not removed.
        """

        print('Setting up EMNIST dataset')

        file_path = osp.abspath(osp.join(self.download_dir_path, osp.basename(DatasetGenerator.emnist_dataset_url)))

        # step 1: download
        DatasetGenerator.download_file(url=DatasetGenerator.emnist_dataset_url, dest=file_path)

        # step 2.1: extract main zip file
        DatasetGenerator.extract_zip_file(zip_fp=file_path)

        # create list to store idx file paths and label mappings
        dtype = 'balanced' if self.balanced else 'byclass'

        # idx paths saved as (image, label) pair
        idx_paths = [
            (
                osp.join(osp.dirname(file_path), 'gzip', f'emnist-{dtype}-train-images-idx3-ubyte.gz'),
                osp.join(osp.dirname(file_path), 'gzip', f'emnist-{dtype}-train-labels-idx1-ubyte.gz')
            ),
            (
                osp.join(osp.dirname(file_path), 'gzip', f'emnist-{dtype}-test-images-idx3-ubyte.gz'),
                osp.join(osp.dirname(file_path), 'gzip', f'emnist-{dtype}-test-labels-idx1-ubyte.gz')
            )
        ]

        label_mapping = {}

        with open(osp.join(osp.dirname(file_path), 'gzip', f'emnist-{dtype}-mapping.txt'), mode='r') as lm:
            for line in lm:
                key, value = line.split()

                label_mapping[key] = chr(int(value))

        # step 2.2: extract smaller gzip files
        for idx_pair in idx_paths:
            for idx_path in idx_pair:
                DatasetGenerator.extract_gzip_file(gzip_fp=idx_path)

        # step 3: save image files
        for idx_pair in idx_paths:
            self.idx_to_image(
                image_file=osp.splitext(idx_pair[0])[0],
                label_file=osp.splitext(idx_pair[1])[0],
                label_mapping=label_mapping
            )

    @staticmethod
    def download_file(url: str, dest: str):
        """
        Method to download a file from url and save at dest
        """

        print(f'Downloading file from {url} and saving to {dest}')

        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length'))
        chunk_size = 4096
        total_steps = int(total_size / chunk_size)
        progress_bar = IncrementalBar(max=total_steps, suffix='%(percent).1f%%')

        with open(dest, mode='wb') as fd:
            for chunk in response.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
                progress_bar.next()

        progress_bar.finish()

    @staticmethod
    def extract_zip_file(zip_fp: str):
        """
        Method to extract a zip file and save it in the same directory as the zip file
        """

        print(f'Extracting {zip_fp}')

        with zipfile.ZipFile(zip_fp, 'r') as unzipped:
            unzipped.extractall(osp.dirname(zip_fp))

    @staticmethod
    def extract_gzip_file(gzip_fp: str):
        """
        Method to extract a gzip file and save it in the same directory as the gzip file
        """

        print(f'Extracting {gzip_fp}')

        with gzip.open(gzip_fp, 'rb') as zipped:
            with open(osp.splitext(gzip_fp)[0], mode='wb') as unzipped:
                shutil.copyfileobj(zipped, unzipped)

    def idx_to_image(self, image_file: str, label_file: str, label_mapping: Dict[str, str] = None):
        print(f'Converting {image_file} to image files')

        with open(image_file, mode='rb') as image_stream, open(label_file, mode='rb') as label_stream:
            # save images dataset
            magic, num_images = struct.unpack('>II', image_stream.read(8))

            if magic != 2051:
                raise ValueError('Magic number invalid')

            num_rows, num_cols = struct.unpack('>II', image_stream.read(8))
            images = np.fromfile(image_stream, dtype=np.dtype(np.uint8).newbyteorder('>'))
            images = images.reshape((num_images, num_rows, num_cols))

            # save labels dataset
            magic, num_labels = struct.unpack('>II', label_stream.read(8))

            if magic != 2049:
                raise ValueError('Magic number invalid')

            labels = np.fromfile(label_stream, dtype=np.dtype(np.uint8).newbyteorder('>'))
            labels = labels.astype('str')

            labels = np.vectorize(lambda x: label_mapping[x])(labels) if label_mapping is not None else labels

            progress_bar = IncrementalBar(max=len(labels), suffix='%(percent).1f%%')

            # create missing directories
            for unique_label in np.unique(labels):
                label_folder = osp.abspath(osp.join(self.data_dir_path, unique_label))
                pathlib.Path(label_folder).mkdir(parents=True, exist_ok=True)

            # save images to data directory
            for label, image in zip(labels, images):
                label_folder = osp.abspath(osp.join(self.data_dir_path, label))
                image_fd, image_dest = tempfile.mkstemp(dir=label_folder, suffix='.png')

                cv2.imwrite(f'{image_dest}', image.T)
                os.close(image_fd)  # if not closed, can get OSError: [Errno 24] Too many open files

                progress_bar.next()

            progress_bar.finish()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Script to download and create training data from EMNIST. Full dataset would be downloaded irrespective of
            unbalanced truth value.
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
        '-ub',
        '--unbalanced',
        dest='unbalanced',
        action='store_true',
        default=False,
        help='Whether to use the unbalanced dataset or not',
    )
    args = parser.parse_args()

    creator = DatasetGenerator(balanced=not args.unbalanced,
                               download_dir_path=args.download_path,
                               data_dir_path=args.data_path)
    creator.create()
