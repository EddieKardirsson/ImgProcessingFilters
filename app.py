import cv2
import numpy as np

# dummy function that does nothing
def dummy(value):
    pass

# define convolution kernels
identity_kernel = np.array([[0,0,0],
                            [0,1,0],
                            [0,0,0]])

sharpen_kernel = np.array([[0,-1,0],
                           [-1,5,-1],
                           [0,-1,0]])

gaussian_kernel1 = cv2.getGaussianKernel(3,0)
gaussian_kernel2 = cv2.getGaussianKernel(7,0)

box_kernel = np.array([[1,1,1],
                       [1,1,1],
                       [1,1,1]], np.float32) /9.0

kernels = [identity_kernel, sharpen_kernel, gaussian_kernel1, gaussian_kernel2, box_kernel]

# Read in an image, make a grayscale copy
color_original = cv2.imread('test.jpg')
gray_original = cv2.cvtColor(color_original, cv2.COLOR_BGR2GRAY)

# create the UI (window and trackbars)
cv2.namedWindow('app', cv2.WINDOW_AUTOSIZE)

# arguments: trackbarName, windowName, value (initial value), count (max value), onChange (event handler)
cv2.createTrackbar('grayscale', 'app', 0, 1, dummy)
cv2.createTrackbar('filter', 'app', 0, len(kernels)-1, dummy)
cv2.createTrackbar('brightness', 'app', 50, 100, dummy)
cv2.createTrackbar('contrast', 'app', 1, 100, dummy)

# Main UI loop
while True:
    # Read trackbar values
    grayscale = cv2.getTrackbarPos('grayscale', 'app')
    kernel_idx = cv2.getTrackbarPos('filter', 'app')
    brightness = cv2.getTrackbarPos('brightness', 'app')
    contrast = cv2.getTrackbarPos('contrast', 'app')

    # Filters
    color_modified = cv2.filter2D(color_original, -1, kernels[kernel_idx])
    gray_modified = cv2.filter2D(gray_original, -1, kernels[kernel_idx])

    # Brightness & Contrast
    color_modified = cv2.addWeighted(color_modified, contrast, np.zeros_like(color_original), 0, brightness - 50)
    gray_modified = cv2.addWeighted(gray_modified, contrast, np.zeros_like(gray_original), 0, brightness - 50)

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