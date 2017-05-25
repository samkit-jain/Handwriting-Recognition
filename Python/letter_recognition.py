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
from sklearn.neighbors import KNeighborsClassifier


def train_model():
	tot = 0

	for name in listdir('/home/samkit/Desktop/fs2'):
		if name[-3:] == 'png':
			tot = tot + 1

	x = np.zeros(shape=(tot,784))
	y = np.array([])

	tot = 0

	print "Reading letters..."

	t0 = time()

	for name in listdir('/home/samkit/Desktop/fs2'):
		if name[-3:] == 'png':
			y = np.append(y, np.array(name[0]))
			
			name_im = mpimg.imread('/home/samkit/Desktop/fs2/' + name)
			name_im = np.dot(name_im[...,:3], [0.299, 0.587, 0.114])
			name_im = name_im.flatten()

			x[tot] = name_im
			tot = tot + 1

	print "Read letters..."
	print "Reading time: ", round(time() - t0, 3), "s"

	x = x / 255.0

	print "Training..."

	features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(x, y, test_size=0, random_state=42)

	
	# Train
	t0 = time()
	clf = KNeighborsClassifier(n_neighbors=165)
	clf.fit(features_train, labels_train)
	print "Trained..."
	print "Training time: ", round(time() - t0, 3), "s"

	# Save to pickle file
	f = open('classifier_knn165.pickle', 'wb')
	pickle.dump(clf, f)
	f.close()


def test_model():
	f = open('classifier_knn165.pickle', 'rb')
	clf = pickle.load(f)
	f.close()

	tot = 0

	for name in listdir('/home/samkit/Desktop/fs2'):
		if name[-3:] == 'png':
			tot = tot + 1

	x = np.zeros(shape=(tot,784))
	y = np.array([])

	print tot
	return

	tot = 0

	t0 = time()

	for name in listdir('/home/samkit/Desktop/fs2'):
		if name[-3:] == 'png':
			y = np.append(y, np.array(name[0]))
			
			name_im = mpimg.imread('/home/samkit/Desktop/fs2/' + name)
			name_im = np.dot(name_im[...,:3], [0.299, 0.587, 0.114])
			name_im = name_im.flatten()

			x[tot] = name_im
			tot = tot + 1

	x = x / 255.0

	features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(x, y, test_size=0, random_state=42)

	t0 = time()
	pred = clf.predict(features_train)
	print "Prediction time: ", round(time() - t0, 3), "s"
	print "Accuracy: ", (accuracy_score(pred, labels_train) * 100), "%"


def recognise_letter():
	letter_loc = get_image_src()

	for loc in letter_loc:
		letter_image = mpimg.imread(loc)

		gray_letter = np.dot(letter_image[...,:3], [0.299, 0.587, 0.114])
		letter_display = gray_letter

		gray_letter = gray_letter.flatten()

		
		for i in range(len(gray_letter)):
			gray_letter[i] = gray_letter[i]
			gray_letter[i] = round(gray_letter[i], 8)
		
		f = open('classifier_knn165.pickle', 'rb')
		clf = pickle.load(f)
		f.close()

		plt.figure()
		plt.imshow(letter_display, cmap=plt.get_cmap('gray'))
		plt.title('letter is ' + clf.predict([gray_letter])[0])

	plt.show()


def show_menu():
	print
	print "<1> Calculate accuracy"
	print "<2> Recognize letter"
	print "<3> Train again"
	print "<any other> Exit"
	print
	ch = int(raw_input("Enter choice - "))

	return ch


choice = 0

while True:
	choice = show_menu()

	if choice == 1:
		test_model()

	elif choice == 2:
		recognise_letter()

	elif choice == 3:
		train_model()

	else:
		print "Thank you!"
		break