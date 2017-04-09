import pickle
import os
from time import time
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.grid_search import GridSearchCV
from sklearn.datasets import fetch_mldata
from sklearn import cross_validation
from sklearn.neighbors import KNeighborsClassifier
from scipy import ndimage
import collections
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from painte import get_image_src2

def ret_val():
	if os.path.isfile('./classifier_full.pickle'):
		f = open('classifier_full.pickle', 'rb')
		clf = pickle.load(f)

	digit_loc = get_image_src2()

	digit_image = mpimg.imread(digit_loc)

	gray_digit = np.dot(digit_image[...,:3], [0.299, 0.587, 0.114])
	digit_display = gray_digit

	gray_digit = gray_digit.flatten()

	for i in range(len(gray_digit)):
		gray_digit[i] = 1.0 - gray_digit[i]
		gray_digit[i] = round(gray_digit[i], 8)

	return str(int(clf.predict([gray_digit])[0]))