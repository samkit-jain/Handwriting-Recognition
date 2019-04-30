import cv2
import numpy as np

from model import Model


class Drawer:
    def __init__(self):
        self.mouse_pressed = False
        self.img = np.zeros(shape=(1024, 1024, 3), dtype=np.uint8)
        self.char_color = (255, 255, 255)

    def draw(self):
        """
        Method to draw continuous multiple circles on an image. Like a paint brush.
        """

        self.reset()

        window_name = 'Draw character'

        cv2.namedWindow(winname=window_name)
        cv2.setMouseCallback(window_name=window_name, on_mouse=self.mouse_callback)

        # continue till ESC key is pressed
        while True:
            cv2.imshow(winname=window_name, mat=self.img)

            # ESC key pressed
            k = cv2.waitKey(delay=1) & 0xFF
            if k == 27:
                break

        cv2.destroyAllWindows()

    def get_contours(self):
        """
        Method to find contours in an image and crop them and return a list with cropped contours
        """

        images = []
        main_image = self.img
        orig_image = main_image.copy()

        # convert to greyscale and apply Gaussian filtering
        main_image = cv2.cvtColor(src=main_image, code=cv2.COLOR_BGR2GRAY)
        main_image = cv2.GaussianBlur(src=main_image, ksize=(5, 5), sigmaX=0)

        # threshold the image
        _, main_image = cv2.threshold(src=main_image, thresh=127, maxval=255, type=cv2.THRESH_BINARY)

        # find contours in the image
        contours, _ = cv2.findContours(image=main_image.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        # get rectangles containing each contour
        bboxes = [cv2.boundingRect(array=contour) for contour in contours]

        for bbox in bboxes:
            x, y, width, height = bbox[:4]
            images.append(orig_image[y:y + height, x:x + width])

        return images

    def get_images(self):
        images = []

        self.draw()

        char_images = self.get_contours()

        for cimg in char_images:
            images.append(Drawer.convert_to_emnist(img=cimg))

        return images

    def mouse_callback(self, event, x, y, flags, params):
        """
        Callback method for drawing circles on an image
        """

        # left mouse button is pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_pressed = True

        # mouse pointer has moved over the window
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.mouse_pressed:
                cv2.circle(img=self.img, center=(x, y), radius=20, color=self.char_color, thickness=-1)

        # left mouse button is released
        elif event == cv2.EVENT_LBUTTONUP:
            self.mouse_pressed = False
            cv2.circle(img=self.img, center=(x, y), radius=20, color=self.char_color, thickness=-1)

    def reset(self):
        # reset image
        self.img = np.zeros((1024, 1024, 3), np.uint8)

    @staticmethod
    def convert_to_emnist(img):
        """
        Method to make an image EMNIST format compatible. img is a cropped version of the character image.

        Conversion process available in section II-A of the EMNIST paper available at https://arxiv.org/abs/1702.05373v1
        """

        height, width = img.shape[:2]

        # create a square frame with lengths equal to the largest dimension
        emnist_image = np.zeros(shape=(max(height, width), max(height, width), 3), dtype=np.uint8)

        # center the cropped image in it
        offset_height = int(float(emnist_image.shape[0] / 2.0) - float(height / 2.0))
        offset_width = int(float(emnist_image.shape[1] / 2.0) - float(width / 2.0))

        emnist_image[offset_height:offset_height + height, offset_width:offset_width + width] = img

        # resize to 26x26 using bi-cubic interpolation
        emnist_image = cv2.resize(src=emnist_image, dsize=(26, 26), interpolation=cv2.INTER_CUBIC)

        # refit the 26x26 to 28x28 so that characters don't touch the boundaries
        fin_image = np.zeros(shape=(28, 28, 3), dtype=np.uint8)
        fin_image[1:27, 1:27] = emnist_image

        return fin_image


if __name__ == '__main__':
    images = Drawer().get_images()

    for image in images:
        label = Model().predict(img=image)
        cv2.imshow(winname=label, mat=image)
        cv2.waitKey(delay=0)
        cv2.destroyAllWindows()
