import argparse
import os
import requests

from progress.bar import IncrementalBar


class DatasetGenerator:
    """
    Class to download and create dataset for training and testing.
    """

    # download URLs
    urls = {
        'mnist': [
            'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',  # training set images
            'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',  # training set labels
            'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',  # testing set images
            'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz',  # testing set labels
        ],
        'nist': []
    }

    def __init__(self, mnist: bool, nist: bool, op: str = None):
        self.mnist = mnist
        self.nist = nist
        self.output_path = op

        if not(self.output_path and self.output_path.strip()):
            self.output_path = ''

    def create(self):
        # download dataset
        self.download_files()
        
        if self.mnist:
            # transform
            pass

        if self.nist:
            # transform
            pass

    def download_files(self):
        """
        Method to download dataset files from MNIST and NIST websites
        """

        dict2 = {
            'mnist': self.mnist,
            'nist': self.nist,
        }
        
        for data_type, should_download in dict2.items():
            if should_download:
                print(f'Downloading {data_type.upper()} dataset\n')
                
                for url in DatasetGenerator.urls[data_type]:
                    file_name = os.path.abspath(os.path.join(self.output_path, os.path.basename(url)))
                    print(f'Downloading file from {url} and saving to {file_name}')

                    response = requests.get(url, stream=True)
                    total_size = int(response.headers.get('content-length'))
                    chunk_size = 4096
                    total_steps = int(total_size / chunk_size)
                    progress_bar = IncrementalBar(max=total_steps, suffix='%(percent).1f%% - %(eta)ds')

                    with open(file_name, 'wb') as fd:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            fd.write(chunk)
                            progress_bar.next()

                    progress_bar.finish()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Script to download and create training data from MNIST or NIST images.
            """,
        usage='%(prog)s [options]',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help='Path where dataset should be saved.',
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

    creator = DatasetGenerator(mnist=args.mnist, nist=args.nist, op=args.output)
    creator.create()
