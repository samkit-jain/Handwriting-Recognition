from Tkinter import *
from scipy import ndimage
import Image, ImageDraw
import matplotlib.image as mpimg
import numpy as np


# Variable initialization
canvas_width = 560
canvas_height = 560
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
master = Tk()
master.title("Draw digit")
size = 28, 28
user_close = 0


# Callback function when the user clicks on "Predict" button
def call_predict():
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
b = Button(master, text="Predict", command=call_predict)


# Callback function to draw in window
# -- Creates circles of color red and outline red on Tkinter window
# -- Perform the same draw operation on PIL Image
def paint(event):
	global w, draw, red

	x1, y1 = (event.x - 20), (event.y - 20)
	x2, y2 = (event.x + 20), (event.y + 20)
	w.create_oval(x1, y1, x2, y2, fill="red", outline="red")
	draw.ellipse([x1, y1, x2, y2], red, outline=red)


# Function that returns the image location
def get_image_src():
	global w, image1, black, white, master, user_close, big_size, small_size

	# Setting up Tkinter window
	w.pack(expand=YES, fill=BOTH)
	w.bind("<B1-Motion>", paint)
	w.configure(background="white")
	b.pack(side=BOTTOM)

	master.protocol("WM_DELETE_WINDOW", closed)
	mainloop()

	filename = ""

	# Check if user clicked "Predict" (0) or closed the window (1)
	if user_close == 0:
		image1.save("step1.png")

		image1 = image1.crop(image1.getbbox())

		image1.save("step2.png")

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
		image1.save("step3.png")

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

		image2.save("step5.png")

		image2 = Image.new("RGB", (28, 28), white)
		image2.paste(image1, (14 - int(round(y, 0)), 14 - int(round(x, 0))))
		image2.save("step6.png")

	return "step6.png"