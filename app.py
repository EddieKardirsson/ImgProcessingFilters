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

sepia_kernel = np.array([[0.1655, 0.317, 0.191],
                        [0.139, 0.443, 0.4245],
                        [0.5965, 0.4945, 0.1895]])

bluetone_kernel = np.array([[0.433, 0.55, 0.189],
                         [0.389, 0.51, 0.168],
                         [0.322, 0.41, 0.141]])

greentone_kernel = np.array([[0.393, 0.199, 0.3],
                         [0.4, 0.2, 0.43],
                         [0.3, 0.15, 0.4]])

redtone_kernel = np.array([[0.4, 0.2, 0.1],
                           [0.2, 0.3, 0.2],
                           [0.6, 0.3, 0.2]])


kernels = [identity_kernel, sharpen_kernel, gaussian_kernel1, gaussian_kernel2, box_kernel]

# Read in an image, make a grayscale copy
color_original = cv2.imread('test.jpg')
gray_original = cv2.cvtColor(color_original, cv2.COLOR_BGR2GRAY)
sepia_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), sepia_kernel)
bluetone_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), bluetone_kernel)
greentone_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), greentone_kernel)
redtone_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), redtone_kernel)

# create the UI (window and trackbars)
cv2.namedWindow('app', cv2.WINDOW_AUTOSIZE)

# arguments: trackbarName, windowName, value (initial value), count (max value), onChange (event handler)
cv2.createTrackbar('grayscale', 'app', 0, 5, dummy)
cv2.createTrackbar('filter', 'app', 0, len(kernels)-1, dummy)
cv2.createTrackbar('brightness', 'app', 50, 100, dummy)
cv2.createTrackbar('contrast', 'app', 1, 100, dummy)

count = 1

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
    sepia_modified = cv2.filter2D(sepia_original, -1, kernels[kernel_idx])
    bluetone_modified = cv2.filter2D(bluetone_original, -1, kernels[kernel_idx])
    greentone_modified = cv2.filter2D(greentone_original, -1, kernels[kernel_idx])
    redtone_modified = cv2.filter2D(redtone_original, -1, kernels[kernel_idx])

    # Brightness & Contrast
    color_modified = cv2.addWeighted(color_modified, contrast, np.zeros_like(color_original), 0, brightness - 50)
    gray_modified = cv2.addWeighted(gray_modified, contrast, np.zeros_like(gray_original), 0, brightness - 50)
    sepia_modified = cv2.addWeighted(sepia_modified, contrast, np.zeros_like(sepia_original), 0, brightness - 50)
    bluetone_modified = cv2.addWeighted(bluetone_modified, contrast, np.zeros_like(bluetone_original), 0, brightness - 50)
    greentone_modified = cv2.addWeighted(greentone_modified, contrast, np.zeros_like(greentone_original), 0, brightness - 50)
    redtone_modified = cv2.addWeighted(redtone_modified, contrast, np.zeros_like(redtone_original), 0, brightness - 50)

    # Save and Quit commands:
    key = cv2.waitKey(100)  # Wait fo keypress 100 milliseconds
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Save image
        if grayscale == 0:
            cv2.imwrite('../output-{}.png'.format(count), color_modified)
        elif grayscale == 1:
            cv2.imwrite('../output-{}.png'.format(count), gray_modified)
        elif grayscale == 2:
            cv2.imwrite('../output-{}.png'.format(count), sepia_modified)
        elif grayscale == 3:
            cv2.imwrite('../output-{}.png'.format(count), bluetone_modified)
        elif grayscale == 4:
            cv2.imwrite('../output-{}.png'.format(count), greentone_modified)
        elif grayscale == 5:
            cv2.imwrite('../output-{}.png'.format(count), redtone_modified)
        count += 1

    # show the image:
    if grayscale == 0:
        cv2.imshow('app', color_modified)
    elif grayscale == 1:
        cv2.imshow('app', gray_modified)
    elif grayscale == 2:
        cv2.imshow('app', sepia_modified)
    elif grayscale == 3:
        cv2.imshow('app', bluetone_modified)
    elif grayscale == 4:
        cv2.imshow('app', greentone_modified)
    elif grayscale == 5:
        cv2.imshow('app', redtone_modified)


# window cleanup
cv2.destroyWindow('app')