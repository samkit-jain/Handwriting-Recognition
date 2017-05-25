from Tkinter import *
from scipy import ndimage
import Image, ImageDraw
import matplotlib.image as mpimg
import numpy as np
from os import listdir
from os.path import isfile, join


# Variable initialization
canvas_width = 560
canvas_height = 560
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
size = 28, 28
user_close = 0

char_value = raw_input("Enter character you want to draw: ")

files = []
count = 0

for name in listdir('.'):
	if isfile(join('.', name)):
		if name[0] == char_value and name[-4:] == '.png':
			count = count + 1



master = Tk()
master.title("Draw anything")


# Callback function when the user clicks on "Done" button
def call_done():
	global master

	master.destroy()


# Callback function when the user closes the window
def closed():
	global user_close, master

	user_close = 1
	master.destroy()


image1 = Image.new("RGB", (canvas_width, canvas_height), black)
draw = ImageDraw.Draw(image1)

w = Canvas(master, width=canvas_width, height=canvas_height + 20)
b = Button(master, text="Done", command=call_done)


# Callback function to draw in window
# -- Creates circles of color red and outline red on Tkinter window
# -- Perform the same draw operation on PIL Image
def paint(event):
	global w, draw, red

	x1, y1 = (event.x - 20), (event.y - 20)
	x2, y2 = (event.x + 20), (event.y + 20)
	w.create_oval(x1, y1, x2, y2, fill="red", outline="red")
	draw.ellipse([x1, y1, x2, y2], red, outline=red)


# Setting up Tkinter window
w.pack(expand=YES, fill=BOTH)
w.bind("<B1-Motion>", paint)
w.configure(background="white")
b.pack(side=BOTTOM)

master.protocol("WM_DELETE_WINDOW", closed)
mainloop()

filename = ""

# Check if user clicked "Done" (0) or closed the window (1)
if user_close == 0:
	image1 = image1.crop(image1.getbbox())
	w1, h1 = image1.size
	
	image2 = Image.new("RGB", (28, 28), white)

	datas = image1.getdata()
	newdata = []

	for item in datas:
		if item[0] == 255 and item[1] == 255 and item[2] == 255: # Red -> Black
			newdata.append(white)
		elif item[0] == 0 and item[1] == 0 and item[2] == 0: # Black -> White
			newdata.append(white)
		else:
			newdata.append(black)

	image1.putdata(newdata)
	image1.thumbnail((20, 20), Image.ANTIALIAS)

	image2.paste(image1, (0, 0))
	#WHERE IS IMAGE2.SAVE(STEP4.PNG)

	digit_image = mpimg.imread("step4.png")

	gray_digit = np.dot(digit_image[...,:3], [0.299, 0.587, 0.114])
	gray_digit = gray_digit.flatten()


	for i in range(len(gray_digit)):
		gray_digit[i] = 1.0 - gray_digit[i]
		gray_digit[i] = round(gray_digit[i], 8)


	# Calculating center of mass of the image
	x, y = ndimage.measurements.center_of_mass(gray_digit.reshape(28, 28))

	image2 = image2.transform(image2.size, Image.AFFINE, (1, 0, y - 14, 0, 1, x - 14), fill=0)

	image2 = Image.new("RGB", (28, 28), white)
	image2.paste(image1, (14 - int(round(y, 0)), 14 - int(round(x, 0))))
	image2.save(char_value + "_" + str(count) + ".png")