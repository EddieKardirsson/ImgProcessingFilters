import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# dummy function that does nothing
def dummy(value):
    pass

# Create a Tkinter window for loading and saving images in the filesystem
root = tk.Tk()
root.withdraw()  # Hide the window

def load_image():
    file_path = filedialog.askopenfilename(title="select and image", filetypes=[("Image files", ".jpg .jpeg .png .bmp .webp")])
    if file_path:
        image = cv2.imread(file_path)
        return image

def save_image(image):
    file_path = filedialog.asksaveasfilename(title="Save an image", defaultextension=".jpg", confirmoverwrite=True,
                                             filetypes=[("JPG", ".jpg"),
                                                        ("JPEG", ".jpeg"),
                                                        ("PNG", ".png"),
                                                        ("Bitmap", ".bmp"),
                                                        ("WEBP", ".webp")])
    if file_path:
        cv2.imwrite(file_path, image)

def resize_window():
    global height, width, _
    if color_original is not None:
        height, width, _ = color_original.shape
        cv2.resizeWindow(application_name, width - 25, height)  # Add some extra space for the sliders

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


def create_window():
    global application_name
    application_name = 'app'
    cv2.namedWindow(application_name, cv2.WINDOW_AUTOSIZE)


# create the UI (window and trackbars)
create_window()


def generate_copies():
    global gray_original, sepia_original, bluetone_original, greentone_original, redtone_original
    gray_original = cv2.cvtColor(color_original, cv2.COLOR_BGR2GRAY)
    sepia_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), sepia_kernel)
    bluetone_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), bluetone_kernel)
    greentone_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), greentone_kernel)
    redtone_original = cv2.transform(cv2.cvtColor(gray_original, cv2.COLOR_GRAY2BGR), redtone_kernel)

# Read in an image, make copies for the grayscale effects
color_original = load_image()
generate_copies()

# Resize the window depending on image format and size
resize_window()

# Add sliders to the window
def create_sliders():
    cv2.createTrackbar('grayscale', application_name, 0, 5, dummy)
    cv2.createTrackbar('filter', application_name, 0, len(kernels) - 1, dummy)
    cv2.createTrackbar('brightness', application_name, 50, 100, dummy)
    cv2.createTrackbar('contrast', application_name, 1, 100, dummy)

create_sliders()

# Main UI loop
while True:
    # Read trackbar values
    grayscale = cv2.getTrackbarPos('grayscale', application_name)
    kernel_idx = cv2.getTrackbarPos('filter', application_name)
    brightness = cv2.getTrackbarPos('brightness', application_name)
    contrast = cv2.getTrackbarPos('contrast', application_name)

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

    # TODO: Implement a save function so user can save the image anywhere in the filesystem. Default: My Documents\Pictures
    # Save, Load and Quit commands:
    key = cv2.waitKey(100)  # Wait fo keypress 100 milliseconds
    if key == ord('q'):
        break
    elif key == ord('s'):
        if grayscale == 0:
            save_image(color_modified)
        elif grayscale == 1:
            save_image(gray_modified)
        elif grayscale == 2:
            save_image(sepia_modified)
        elif grayscale == 3:
            save_image(bluetone_modified)
        elif grayscale == 4:
            save_image(greentone_modified)
        elif grayscale == 5:
            save_image(redtone_modified)
    elif key == ord('l'):
        # Load new image
        cv2.destroyWindow(application_name)
        color_original = load_image()
        if color_original is not None:
            # Update the image variables
            generate_copies()
            # Resize the window to fit the new image
            create_window()
            resize_window()
            create_sliders()

    # show the image:
    if grayscale == 0:
        cv2.imshow(application_name, color_modified)
    elif grayscale == 1:
        cv2.imshow(application_name, gray_modified)
    elif grayscale == 2:
        cv2.imshow(application_name, sepia_modified)
    elif grayscale == 3:
        cv2.imshow(application_name, bluetone_modified)
    elif grayscale == 4:
        cv2.imshow(application_name, greentone_modified)
    elif grayscale == 5:
        cv2.imshow(application_name, redtone_modified)


# window cleanup
cv2.destroyWindow(application_name)