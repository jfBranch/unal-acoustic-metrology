import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


"""
Programed by Felipe Maldonado,
Universidad Nacional de Colombia, Faculty of Engineering,
Department of Electrical and Electronic Engineering.
Created on 2022/03.
"""
__autor__ = 'Juan Felipe Maldonado'
__version__ = '1.0 Beta'

path = "Images/Test1"
img_name = "5(1).jpg"  # Sample just for showing results of processing
descriptor = cv.SIFT_create(contrastThreshold=0.02, edgeThreshold=1, sigma=0.01)  # Creates a SIFT descriptor
# Four key points for computing SIFT descriptor
key_points = [cv.KeyPoint(7, 7, 16), cv.KeyPoint(7, 13, 16),
              cv.KeyPoint(13, 7, 16), cv.KeyPoint(13, 13, 16)]
X = []
y = []
img = cv.imread(path + "/" + img_name, cv.IMREAD_GRAYSCALE)  # Read image in gray scale
img_col = cv.cvtColor(cv.imread(path + "/" + img_name), cv.COLOR_BGR2RGB)  # Read image in gray scale
img_blur = cv.GaussianBlur(img.copy(), ksize=(0, 0), sigmaX=1.5)  # Gaussian filtering
mayor_axis = max(img_blur.shape)  # The largest axis
# Normalize size
digit_scaled = cv.resize(img_blur, (0, 0), fx=32 / mayor_axis,
                         fy=32 / mayor_axis, interpolation=cv.INTER_CUBIC)
# Build an image of 32 x 32 pixels with padding
if digit_scaled.shape[0] >= digit_scaled.shape[1]:
    digit_scaled = np.pad(digit_scaled, ((0, 0), ((32 - digit_scaled.shape[1]) // 2,
                                                  (32 - digit_scaled.shape[1]) // 2)), 'constant')
else:
    digit_scaled = np.pad(digit_scaled, (((32 - digit_scaled.shape[0]) // 2,
                                          (32 - digit_scaled.shape[0]) // 2), (0, 0)), 'constant')

img_bin = cv.threshold(digit_scaled, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]  # Otsu binarization
# -- SIFT DESCRIPTOR --
_, features = descriptor.compute(img_bin, key_points)  # Computes SIFT descriptor
X.append(features.flatten())  # Add the features vector of the actual training sample
y.append(img_name)  # Add the class of the actual training sample
# -- Plots results --
plt.imshow(img, cmap='gray'), plt.show()
plt.imshow(img_col), plt.show()
plt.imshow(img_blur, cmap='gray'), plt.show()
plt.imshow(digit_scaled, cmap='gray'), plt.show()
plt.imshow(img_bin, cmap='gray'), plt.show()

# -- Plots SIFT features by sample --
plt.scatter(range(len(X[0])), X[0], s=8, c='b', marker='s', label='Muestra de número 5')
plt.grid(visible=True), plt.legend(), plt.show()
