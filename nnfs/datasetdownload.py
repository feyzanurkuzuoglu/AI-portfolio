URL = 'https://nnfs.io/datasets/fashion_mnist_images.zip'
FILE = 'fashion_mnist_images.zip'
FOLDER = 'fashion_mnist_images'
import os
import urllib
import urllib.request
from zipfile import ZipFile

if not os.path.isfile(FILE):
    print(f'Downloading {URL} and saving as {FILE}...')
    urllib.request.urlretrieve(URL, FILE)
print('Unzipping images...')
with ZipFile(FILE) as zip_images:
    zip_images.extractall(FOLDER)
print("Done!")

labels = os.listdir('fashion_mnist_images/train')
print(labels)
files = os.listdir('fashion_mnist_images/train/0')
print(files[:10])
print(len(files))