import cv2
import numpy as np

# dummy function that does nothing
def dummy(value):
    pass

# Read in an image, make a grayscale copy
color_original = cv2.imread('test.jpg')
gray_original = cv2.cvtColor(color_original, cv2.COLOR_BGR2GRAY)

# create the UI (window and trackbars)
cv2.namedWindow('app', cv2.WINDOW_AUTOSIZE)

# arguments: trackbarName, windowName, value (initial value), count (max value), onChange (event handler)
cv2.createTrackbar('grayscale', 'app', 0, 1, dummy)
cv2.createTrackbar('filter', 'app', 0, 1, dummy) # TODO: Update max value to number of filters
cv2.createTrackbar('brightness', 'app', 50, 100, dummy)
cv2.createTrackbar('contrast', 'app', 1, 100, dummy)

# Main UI loop
while True:
    # Read trackbar values
    grayscale = cv2.getTrackbarPos('grayscale', 'app')

    # TODO: Filters

    # TODO: Brightness

    # TODO: Contrast

    # Save and Quit commands:
    key = cv2.waitKey(100)  # Wait fo keypress 100 milliseconds
    if key == ord('q'):
        break
    elif key == ord('s'):
        #TODO: save image function
        pass
    # show the image:
    if grayscale == 0:
        #TODO: Replace "color_original" with modified image variable
        cv2.imshow('app', color_original)
    elif grayscale == 1:
        cv2.imshow('app', gray_original)

# window cleanup
cv2.destroyWindow('app')