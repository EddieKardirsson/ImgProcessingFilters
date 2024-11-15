import cv2
import numpy as np

# dummy function that does nothing
def dummy(value):
    pass

# create the UI (window and trackbars)
cv2.namedWindow('app')

# arguments: trackbarName, windowName, value (initial value), count (max value), onChange (event handler)
cv2.createTrackbar('contrast', 'app', 1, 100, dummy)
cv2.createTrackbar('brightness', 'app', 50, 100, dummy)
cv2.createTrackbar('filter', 'app', 0, 1, dummy) # TODO: Update max value to number of filters
cv2.createTrackbar('grayscale', 'app', 0, 1, dummy)

# Main UI loop
while True:
    key = cv2.waitKey(100)  # Wait fo keypress 100 milliseconds
    if key == ord('q'):
        break
    elif key == ord('s'):
        #TODO: save image function
        pass

# window cleanup
cv2.destroyWindow('app')