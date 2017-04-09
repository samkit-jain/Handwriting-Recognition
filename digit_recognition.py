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
import painte

def show_data(train, test):
	train_count = collections.Counter(train)
	test_count = collections.Counter(test)

	print "Data statistics - "
	print
	print "Total training - ", len(labels_train)
	print "Total testing - ", len(labels_test)
	print
	print "Training - "
	print "0 - ", train_count[0]
	print "1 - ", train_count[1]
	print "2 - ", train_count[2]
	print "3 - ", train_count[3]
	print "4 - ", train_count[4]
	print "5 - ", train_count[5]
	print "6 - ", train_count[6]
	print "7 - ", train_count[7]
	print "8 - ", train_count[8]
	print "9 - ", train_count[9]

	print
	print "Testing - "
	print "0 - ", test_count[0]
	print "1 - ", test_count[1]
	print "2 - ", test_count[2]
	print "3 - ", test_count[3]
	print "4 - ", test_count[4]
	print "5 - ", test_count[5]
	print "6 - ", test_count[6]
	print "7 - ", test_count[7]
	print "8 - ", test_count[8]
	print "9 - ", test_count[9]


def show_menu():
	print
	print "<1> Calculate accuracy"
	print "<2> Recognize digit"
	print "<3> View statistics"
	print "<any other> Exit"
	print
	ch = int(raw_input("Enter choice - "))

	return ch


choice = 0

mnist = fetch_mldata('MNIST original')

x = mnist.data
y = mnist.target

x = x / 255.0

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(x, y, test_size=0, random_state=42)

if os.path.isfile('./classifier_full.pickle'):
	f = open('classifier_full.pickle', 'rb')
	clf = pickle.load(f)

else:
	clf = svm.SVC(kernel="linear")

	t0 = time()
	clf.fit(features_train, labels_train)
	print "Training time: ", round(time() - t0, 3), "s"

	f = open('classifier_full.pickle', 'wb')
	pickle.dump(clf, f)
	f.close()

	f = open('classifier_full.pickle', 'rb')
	clf = pickle.load(f)


while True:
	choice = show_menu()

	if choice == 1:
		t0 = time()
		pred = clf.predict(features_train)
		print "Prediction time: ", round(time() - t0, 3), "s"

		print "Accuracy: ", (accuracy_score(pred, labels_train) * 100), "%"

	elif choice == 2:
		digit_loc = painte.get_image_src()

		for loc in digit_loc:
			digit_image = mpimg.imread(loc)

			gray_digit = np.dot(digit_image[...,:3], [0.299, 0.587, 0.114])
			digit_display = gray_digit

			gray_digit = gray_digit.flatten()

			for i in range(len(gray_digit)):
				gray_digit[i] = 1.0 - gray_digit[i]
				gray_digit[i] = round(gray_digit[i], 8)

			plt.figure()
			plt.imshow(digit_display, cmap=plt.get_cmap('gray'))
			plt.title('Digit is ' + str(int(clf.predict([gray_digit])[0])))
		
		plt.show()

	elif choice == 3:
		show_data(labels_train, labels_test)
	else:
		print "Thank you!"
		break

f.close()
