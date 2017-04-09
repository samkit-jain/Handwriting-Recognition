import pickle
import os
from time import time
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
from scipy import ndimage
from painte import get_image_src
from os import listdir
from os.path import isfile, join
import collections
import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def train_model():
	co = 0
	char_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

	while co < 26:
		print char_list[co]
		tot = 0
		
		for name in listdir('/home/samkit/Desktop/fs'):
			if name[-3:] == 'png' and (name[0] == char_list[co] or name[0] == char_list[co + 1] or name[0] == char_list[co + 2] or name[0] == char_list[co + 3]):
				tot = tot + 1

		x = np.zeros(shape=(tot,784))
		y = np.array([])

		tot = 0

		#print "Reading letters..."

		t0 = time()

		for name in listdir('/home/samkit/Desktop/fs'):
			if name[-3:] == 'png' and (name[0] == char_list[co] or name[0] == char_list[co + 1] or name[0] == char_list[co + 2] or name[0] == char_list[co + 3]):
				y = np.append(y, np.array(name[0]))
				
				name_im = mpimg.imread('/home/samkit/Desktop/fs/' + name)
				name_im = np.dot(name_im[...,:3], [0.299, 0.587, 0.114])
				name_im = name_im.flatten()

				x[tot] = name_im
				tot = tot + 1

		#print "Read letters..."
		#print "Reading time: ", round(time() - t0, 3), "s"

		x = x / 255.0

		#print "Training..."

		features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(x, y, test_size=0, random_state=42)

		clf = svm.SVC(kernel="linear", probability=True)

		t0 = time()

		clf.fit(features_train, labels_train)

		f = open('classifier_letter' + str((co / 4) + 1) + '.pickle', 'wb')
		pickle.dump(clf, f)
		f.close()

		#f = open('classifier_full.pickle', 'rb')
		#clf = pickle.load(f)

		#print "Trained..."
		#print "Training time: ", round(time() - t0, 3), "s"

		#t0 = time()
		#pred = clf.predict(features_test)
		#print "Prediction time: ", round(time() - t0, 3), "s"
		#print "Accuracy: ", (accuracy_score(pred, labels_test) * 100), "%"

		co += 4


def test_model():
	for i in range(13):
		f = open('classifier_letter' + str(i + 1) + '.pickle', 'rb')
		clf = pickle.load(f)
		f.close()

		t0 = time()
		pred = clf.predict(features_test)
		
		print "Accuracy: ", (accuracy_score(pred, labels_test) * 100), "%"

def recognise_letter():
	letter_loc = get_image_src()

	if letter_loc != "":
		letter_image = mpimg.imread(letter_loc)

		gray_letter = np.dot(letter_image[...,:3], [0.299, 0.587, 0.114])
		letter_display = gray_letter

		gray_letter = gray_letter.flatten()

		for i in range(len(gray_letter)):
			gray_letter[i] = 1.0 - gray_letter[i]
			gray_letter[i] = round(gray_letter[i], 8)

		#plt.imshow(letter_display, cmap=plt.get_cmap('gray'))
		
		for i in range(13):
			f = open('classifier_letter' + str(i + 1) + '.pickle', 'rb')
			clf = pickle.load(f)
			f.close()

			print clf.predict([gray_letter])
			#print clf.predict_log_proba([gray_letter])
			#print clf.predict_proba([gray_letter])
			#print clf.decision_function([gray_letter])
			#break
			print

		#plt.title('letter is ' + str(clf.predict([gray_letter])[0]))
		#plt.show()


train_model()
#test_model()
#recognise_letter()
