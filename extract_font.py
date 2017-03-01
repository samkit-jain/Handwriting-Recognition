import Image, ImageFont, ImageDraw
import time
import os
from scipy import ndimage
import Image, ImageDraw
import matplotlib.image as mpimg
import numpy as np
import math


def convert_im(code, image1):
	image1 = image1.crop(image1.getbbox())
	w1, h1 = image1.size
	
	image2 = Image.new("RGB", (28, 28), (255, 255, 255))

	datas = image1.getdata()
	newdata = []

	"""
	for item in datas:
		if item[0] == 255 and item[1] == 255 and item[2] == 255: # Red -> Black
			newdata.append(white)
		elif item[0] == 0 and item[1] == 0 and item[2] == 0: # Black -> White
			newdata.append(white)
		else:
			newdata.append(black)

	"""

	#image1.putdata(newdata)
	image1.thumbnail((20, 20), Image.ANTIALIAS)

	image2.paste(image1, (0, 0))
	image2.save("step4.png")

	digit_image = mpimg.imread("step4.png")

	gray_digit = np.dot(digit_image[...,:3], [0.299, 0.587, 0.114])
	gray_digit = gray_digit.flatten()


	for i in range(len(gray_digit)):
		gray_digit[i] = 1.0 - gray_digit[i]
		gray_digit[i] = round(gray_digit[i], 8)


	# Calculating center of mass of the image
	x, y = ndimage.measurements.center_of_mass(gray_digit.reshape(28, 28))

	if math.isnan(x) or math.isnan(y):
		return
	
	image2 = image2.transform(image2.size, Image.AFFINE, (1, 0, y - 14, 0, 1, x - 14), fill=0)

	image2 = Image.new("RGB", (28, 28), (255, 255, 255))
	image2.paste(image1, (14 - int(round(y, 0)), 14 - int(round(x, 0))))
	image2.save(chr(code) + str(time.time()) + ".png")


def extractFunction(font_loc):
	white = (255, 255, 255)

	# use a truetype font
	font = ImageFont.truetype(font_loc, 280)
	im = Image.new("RGB", (280, 280), white)
	draw = ImageDraw.Draw(im)

	for code in range(ord('a'), ord('z') + 1):
		w, h = draw.textsize(chr(code), font=font)
		im = Image.new("RGB", (w, h), white)
		draw = ImageDraw.Draw(im)
		draw.text((0, 0), chr(code), font=font, fill="#000000")
		convert_im(code, im)
		#im.save(chr(code) + str(time.time()) + ".png")

	for code in range(ord('A'), ord('Z') + 1):
		w, h = draw.textsize(chr(code), font=font)
		im = Image.new("RGB", (w, h), white)
		draw = ImageDraw.Draw(im)
		draw.text((0, 0), chr(code), font=font, fill="#000000")
		convert_im(code, im)
		#im.save(chr(code) + str(time.time()) + ".png")


cur_dir = '/home/samkit/Desktop/Handwriting Recognition/fonts/'
c = 1

for name in os.listdir(cur_dir):
	if c > 5538:
		extractFunction(cur_dir + '/' + name)
		print c
	c += 1
