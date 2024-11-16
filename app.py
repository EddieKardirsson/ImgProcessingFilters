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
    brightness = cv2.getTrackbarPos('brightness', 'app')
    contrast = cv2.getTrackbarPos('contrast', 'app')

    # TODO: Filters

    # Brightness & Contrast
    color_modified = cv2.addWeighted(color_original, contrast, np.zeros_like(color_original), 0, brightness - 50)
    gray_modified = cv2.addWeighted(gray_original, contrast, np.zeros_like(gray_original), 0, brightness - 50)

    # Save and Quit commands:
    key = cv2.waitKey(100)  # Wait fo keypress 100 milliseconds
    if key == ord('q'):
        break
    elif key == ord('s'):
        #TODO: save image function
        pass
    # show the image:
    if grayscale == 0:
        cv2.imshow('app', color_modified)
    elif grayscale == 1:
        cv2.imshow('app', gray_modified)

# window cleanup
cv2.destroyWindow('app')