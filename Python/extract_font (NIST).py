import Image, ImageFont, ImageDraw
import time
import os
from scipy import ndimage
import Image, ImageDraw
import matplotlib.image as mpimg
import numpy as np


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


cur_dirs = [
	'/home/samkit/Desktop/Handwriting Recognition/a/',
	'/home/samkit/Desktop/Handwriting Recognition/b/',
	'/home/samkit/Desktop/Handwriting Recognition/c/',
	'/home/samkit/Desktop/Handwriting Recognition/d/',
	'/home/samkit/Desktop/Handwriting Recognition/e/',
	'/home/samkit/Desktop/Handwriting Recognition/f/',
	'/home/samkit/Desktop/Handwriting Recognition/g/',
	'/home/samkit/Desktop/Handwriting Recognition/h/',
	'/home/samkit/Desktop/Handwriting Recognition/i/',
	'/home/samkit/Desktop/Handwriting Recognition/j/',
	'/home/samkit/Desktop/Handwriting Recognition/k/',
	'/home/samkit/Desktop/Handwriting Recognition/l/',
	'/home/samkit/Desktop/Handwriting Recognition/m/',
	'/home/samkit/Desktop/Handwriting Recognition/n/',
	'/home/samkit/Desktop/Handwriting Recognition/o/',
	'/home/samkit/Desktop/Handwriting Recognition/p/',
	'/home/samkit/Desktop/Handwriting Recognition/q/',
	'/home/samkit/Desktop/Handwriting Recognition/r/',
	'/home/samkit/Desktop/Handwriting Recognition/s/',
	'/home/samkit/Desktop/Handwriting Recognition/t/',
	'/home/samkit/Desktop/Handwriting Recognition/u/',
	'/home/samkit/Desktop/Handwriting Recognition/v/',
	'/home/samkit/Desktop/Handwriting Recognition/w/',
	'/home/samkit/Desktop/Handwriting Recognition/x/',
	'/home/samkit/Desktop/Handwriting Recognition/y/',
	'/home/samkit/Desktop/Handwriting Recognition/z/',
	'/home/samkit/Desktop/Handwriting Recognition/A/',
	'/home/samkit/Desktop/Handwriting Recognition/B/',
	'/home/samkit/Desktop/Handwriting Recognition/C/',
	'/home/samkit/Desktop/Handwriting Recognition/D/',
	'/home/samkit/Desktop/Handwriting Recognition/E/',
	'/home/samkit/Desktop/Handwriting Recognition/F/',
	'/home/samkit/Desktop/Handwriting Recognition/G/',
	'/home/samkit/Desktop/Handwriting Recognition/H/',
	'/home/samkit/Desktop/Handwriting Recognition/I/',
	'/home/samkit/Desktop/Handwriting Recognition/J/',
	'/home/samkit/Desktop/Handwriting Recognition/K/',
	'/home/samkit/Desktop/Handwriting Recognition/L/',
	'/home/samkit/Desktop/Handwriting Recognition/M/',
	'/home/samkit/Desktop/Handwriting Recognition/N/',
	'/home/samkit/Desktop/Handwriting Recognition/O/',
	'/home/samkit/Desktop/Handwriting Recognition/P/',
	'/home/samkit/Desktop/Handwriting Recognition/Q/',
	'/home/samkit/Desktop/Handwriting Recognition/R/',
	'/home/samkit/Desktop/Handwriting Recognition/S/',
	'/home/samkit/Desktop/Handwriting Recognition/T/',
	'/home/samkit/Desktop/Handwriting Recognition/U/',
	'/home/samkit/Desktop/Handwriting Recognition/V/',
	'/home/samkit/Desktop/Handwriting Recognition/W/',
	'/home/samkit/Desktop/Handwriting Recognition/X/',
	'/home/samkit/Desktop/Handwriting Recognition/Y/',
	'/home/samkit/Desktop/Handwriting Recognition/Z/' ]

co = 0
black = (0, 0, 0)
white = (255, 255, 255)

for cur_dir in cur_dirs:
	for name in os.listdir(cur_dir):
		image0 = Image.open(cur_dir + name)
		image1 = Image.open(cur_dir + name)
		co += 1

		datas = image1.getdata()
		newdata = []

		for item in datas:
			if item[0] == 255 and item[1] == 255 and item[2] == 255: # White -> Black
				newdata.append(black)
			elif item[0] == 0 and item[1] == 0 and item[2] == 0: # Black -> White
				newdata.append(white)

		image1.putdata(newdata)

		image1 = image0.crop(image1.getbbox())
		#image1.save("step1.png")
		w1, h1 = image1.size

		image2 = Image.new("RGB", (28, 28), (255, 255, 255))

		datas = image1.getdata()
		newdata = []

		image1.thumbnail((20, 20), Image.ANTIALIAS)
		#image1.save("step2.png")

		image2.paste(image1, (0, 0))
		image2.save("step3.png")

		digit_image = mpimg.imread("step3.png")

		gray_digit = np.dot(digit_image[...,:3], [0.299, 0.587, 0.114])
		gray_digit = gray_digit.flatten()

		for i in range(len(gray_digit)):
			gray_digit[i] = 1.0 - gray_digit[i]
			gray_digit[i] = round(gray_digit[i], 8)

		# Calculating center of mass of the image
		x, y = ndimage.measurements.center_of_mass(gray_digit.reshape(28, 28))

		image2 = image2.transform(image2.size, Image.AFFINE, (1, 0, y - 14, 0, 1, x - 14), fill=0)

		image2 = Image.new("RGB", (28, 28), (255, 255, 255))
		image2.paste(image1, (14 - int(round(y, 0)), 14 - int(round(x, 0))))