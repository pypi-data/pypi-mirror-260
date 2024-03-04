from PIL import Image
from scipy.fftpack import fft2, ifft2
import numpy as np
import cv2
from skimage.morphology import binary_opening, binary_closing, disk

import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from skimage import filters, img_as_float
from PIL import Image
import matplotlib.pylab as pylab

import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage.util import random_noise
from skimage import feature
import numpy as np

def generate_noisy_square(size=128, rotation=15, sigma=4, noise_mode='speckle', noise_mean=0.05):
    image = np.zeros((size, size), dtype=float)
    image[size//4:-size//4, size//4:-size//4] = 1
    image = ndi.rotate(image, rotation, mode='constant')
    image = ndi.gaussian_filter(image, sigma)
    image = random_noise(image, mode=noise_mode, mean=noise_mean)
    return image

def canny_edge_detection(image):
    # Compute the Canny filter for two values of sigma
    edges1 = feature.canny(image)
    edges2 = feature.canny(image, sigma=3)
    return edges1, edges2



def apply_convolution(image, kernel):
    convolved_image = cv2.filter2D(image, -1, kernel)
    return convolved_image

def apply_correlation(image, kernel):
    correlated_image = cv2.filter2D(image, -1, kernel)
    return correlated_image

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m / sd)

def process_image(image_path):
    im = Image.open(image_path).convert('L')
    im_array = np.array(im)
    
    freq = fft2(im_array)
    im1 = ifft2(freq).real
    
    snr = signaltonoise(im1, axis=None)
    
    return im_array, im1, snr

def perform_fourier_transform(image_path):
    # Read input image and convert to grayscale
    img = cv2.imread(image_path, 0)

    # Calculate optimal size for Fourier transform
    optimalImg = cv2.copyMakeBorder(img, 0, cv2.getOptimalDFTSize(img.shape[0]) - img.shape[0], 0, cv2.getOptimalDFTSize(img.shape[1]) - img.shape[1], cv2.BORDER_CONSTANT, value=0)

    # Calculate the discrete Fourier transform
    dft_shift = np.fft.fftshift(cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT))

    # Calculate magnitude spectrum
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]) + 1)

    # Reconstruct the image using inverse Fourier transform
    result = cv2.magnitude(cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 0], cv2.idft(np.fft.ifftshift(dft_shift))[:, :, 1])

    return optimalImg, magnitude_spectrum, result

def apply_log_transform(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path)

    # Apply log transform
    log_transformed = 255 * np.log(1 + img.astype(np.float32)) / np.log(1 + np.max(img))

    # Convert the data type
    log_transformed = log_transformed.astype(np.uint8)

    # Save the output image
    cv2.imwrite(output_path, log_transformed)



def apply_gamma_correction(image, gamma_values):
    gamma_corrected_images = []

    for gamma in gamma_values:
        gamma_corrected = np.array(255 * (image / 255) ** gamma, dtype='uint8')
        gamma_corrected_images.append(gamma_corrected)

    return gamma_corrected_images




def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image)
    plt.axis('off')

def plot_hist(channel, title=""):
    plt.hist(np.array(channel).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    plt.xlabel('Pixel Values', size=20)
    plt.ylabel('Frequency', size=20)
    plt.title(title, size=10)

def plot_original(im):
    im_r, im_g, im_b = im.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(im)
    plt.subplot(122)
    plot_hist(im_r, "Red Channel")
    plot_hist(im_g, "Green Channel")
    plot_hist(im_b, "Blue Channel")
    plt.yscale('log')
    plt.show()

def contrast(c):
    return 0 if c < 50 else (255 if c > 150 else int((255 * c - 22950) / 48))

def plot_stretched(imc):
    im_rc, im_gc, im_bc = imc.split()
    plt.style.use('ggplot')
    plt.figure(figsize=(15, 5))
    plt.subplot(121)
    plot_image(imc)
    plt.subplot(122)
    plot_hist(im_rc, "Contrast-Adjusted Red Channel")
    plot_hist(im_gc, "Contrast-Adjusted Green Channel")
    plot_hist(im_bc, "Contrast-Adjusted Blue Channel")
    plt.yscale('log')
    plt.show()



def histogram_equalization(image):
    hist = cv2.calcHist([image],[0],None,[256],[0,256])
    eq = cv2.equalizeHist(image)
    cdf = hist.cumsum()
    cdfnmhist = cdf * hist.max() / cdf.max()
    histeq = cv2.calcHist([eq],[0],None,[256],[0,256])
    cdfeq = histeq.cumsum()
    cdfnmhisteq = cdfeq * histeq.max() / cdf.max()
    
    return eq, hist, cdfnmhist, histeq, cdfnmhisteq


import cv2 as cv

def threshold_image(img, threshold_value):
    ret, thresh = cv.threshold(img, threshold_value, 255, cv.THRESH_BINARY)
    return thresh




import numpy as np
from scipy import signal

import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=20)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def apply_gradient(im):
    ker_x = np.array([[-1, 1]])
    ker_y = np.array([[-1], [1]])
    im_x = signal.convolve2d(im, ker_x, mode='same')
    im_y = signal.convolve2d(im, ker_y, mode='same')
    im_mag = np.sqrt(im_x ** 2 + im_y ** 2)
    im_dir = np.arctan2(im_y, im_x)
    return im_x, im_y, im_mag, im_dir

def apply_laplacian(im):
    ker_laplacian = np.array([[0, -1, 0],
                              [-1, 4, -1],
                              [0, -1, 0]])
    im1 = np.clip(signal.convolve2d(im, ker_laplacian, mode='same'), 0, 1)
    return im1




def plot_img(image, title=""):
    pylab.title(title, size=10)
    pylab.imshow(image)
    pylab.axis('off')


def sobel_edge_detection(image):
    edges_x = filters.sobel_h(image)
    edges_y = filters.sobel_v(image)
    return np.clip(edges_x, 0, 1), np.clip(edges_y, 0, 1)



def generate_noisy_square(size=128, rotation=15, sigma=4, noise_mode='speckle', noise_mean=0.05):
    image = np.zeros((size, size), dtype=float)
    image[size//4:-size//4, size//4:-size//4] = 1
    image = ndi.rotate(image, rotation, mode='constant')
    image = ndi.gaussian_filter(image, sigma)
    image = random_noise(image, mode=noise_mode, mean=noise_mean)
    return image

def canny_edge_detection(image):
    # Compute the Canny filter for two values of sigma
    edges1 = feature.canny(image)
    edges2 = feature.canny(image, sigma=3)
    return edges1, edges2
def plot_canny(image, title="", ax=None):
    if ax is None:
        ax = pylab.gca()
    ax.set_title(title, fontsize=10)
    ax.imshow(image, cmap='gray')
    ax.axis('off')



def erosion(image, kernel_size):
    return cv2.erode(image, np.ones((kernel_size, kernel_size), np.uint8), iterations=1)

def dilation(image, kernel_size):
    return cv2.dilate(image, np.ones((kernel_size, kernel_size), np.uint8), iterations=1)

def opening(image, disk_size):
    return binary_opening(image, disk(disk_size))

def closing(image, disk_size):
    return binary_closing(image, disk(disk_size))
def threshold_image(image, threshold_value):
    _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return binary_image



def load_image(file_path):
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def convert_to_gray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray

def threshold_image(image):
    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh

def segment_image(image):
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=15)
    bg = cv2.dilate(closing, kernel, iterations=1)
    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0)
    ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)
    return fg

def plot_image(image, title=""):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.title(title)
    plt.show()
def plot_images(image, title=""):
    plt.imshow(image, cmap='gray')
    plt.title(title, fontsize=10)
    plt.axis('off')


def fft():
    code = """
import matplotlib.pyplot as plt
from image_func import process_image

# Provide the path to the image file
image_path = r"C:\\Users\\arman\\Pictures\\floweer.jpg"

# Process the image using the process_image function from the sigtonoise package
processed_image, reconstructed_image, snr = process_image(image_path)

# Display the original image
plt.figure(figsize=(10, 5))
plt.imshow(processed_image, cmap='gray')
plt.axis('off')
plt.title('ORIGINAL IMAGE', size=15)
plt.show()

# Display the reconstructed image with SNR
plt.figure(figsize=(10, 5))
plt.imshow(reconstructed_image, cmap='gray')
plt.axis('off')
plt.title(f'IMAGE OBTAINED AFTER RECONSTRUCTION\nSNR: {snr:.2f}', size=15)
plt.show()
"""
    print(code)

def convolution():
    code=r"""
import cv2a
import numpy as np
from image_func import apply_convolution, apply_correlation
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread(r"C:\Users\arman\Pictures\floweer.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define a convolution kernel
conv_kernel = np.ones((3, 3), np.float32) / 9

# Perform convolution
convolved_image = apply_convolution(image, conv_kernel)

# Define a correlation kernel
corr_kernel = np.array([[0, -1, 0],
                        [-1, 5, -1],
                        [0, -1, 0]])

# Perform correlation
correlated_image = apply_correlation(image, corr_kernel)

# Display the results or perform additional processing
# ...
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(image)
axes[0].axis('off')
axes[0].set_title('Original Image')

axes[1].imshow(convolved_image)
axes[1].axis('off')
axes[1].set_title('Convolved Image')

axes[2].imshow(correlated_image)
axes[2].axis('off')
axes[2].set_title('Correlated Image')

plt.tight_layout()
plt.show()
"""
    print(code)

def dft():
    code=r""" import matplotlib.pyplot as plt
from image_func import perform_fourier_transform

# Specify the image path
image_path = r"C:\Users\arman\Pictures\floweer.jpg"

# Perform Fourier transform
optimalImg, DFT, result = perform_fourier_transform(image_path)

# Display the results
images = [optimalImg, DFT, result]
imageTitles = ['Input image', 'DFT', 'Reconstructed image']

for i in range(len(images)):
    plt.subplot(1, 3, i + 1)
    plt.imshow(images[i], cmap='gray')
    plt.title(imageTitles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
"""
    print(code)

def log():
    code=r"""import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_func import apply_log_transform

# Specify the image paths
input_image_path = r"C:\IP practicals\floweer.jpg"
output_image_path = r"C:\IP practicals\floweer1.jpg"

# Apply log transform
apply_log_transform(input_image_path, output_image_path)

# Display the original and log-transformed images
img = cv2.imread(input_image_path)
log_transformed = cv2.imread(output_image_path)

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title('Log-Transformed Image')

plt.show()
"""
    print(code)

def power():
    code=r"""import cv2
import numpy as np
from image_func import apply_gamma_correction

# Specify the image path
image_path = r"C:\IP practicals\floweer.jpg"

# Specify the gamma values
gamma_values = [0.1, 0.5, 1.2, 2.2, 5]

# Read the image
img = cv2.imread(image_path)

# Apply gamma correction
gamma_corrected_images = apply_gamma_correction(img, gamma_values)

# Display the original image
cv2.imshow('Original Image', img)
cv2.waitKey(0)

# Display the gamma-corrected images
for gamma_corrected in gamma_corrected_images:
    cv2.imshow('Gamma Corrected Image', gamma_corrected)
    cv2.waitKey(0)

cv2.destroyAllWindows()
"""
    print(code)

def contrast():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from image_func import plot_original, plot_stretched, contrast

image_path = r"C:\IP practicals\floweer.jpg"
im = Image.open(image_path)

plot_original(im)

imc = im.point(contrast)

plot_stretched(imc)
"""
    print(code)

def histogram():
    code=r"""
import cv2
import matplotlib.pyplot as plt

from image_func import histogram_equalization

# Read the image
image_path = r"C:\IP practicals\floweer.jpg"
img = cv2.imread(image_path, 0)

# Perform histogram equalization
equalized_image, original_hist, original_cdf_hist, equalized_hist, equalized_cdf_hist = histogram_equalization(img)

# Plot the images and histograms
plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.plot(original_hist), plt.plot(original_cdf_hist)
plt.subplot(223), plt.imshow(equalized_image, 'gray')
plt.subplot(224), plt.plot(equalized_hist), plt.plot(equalized_cdf_hist)
plt.xlim([0, 256])
plt.show()
"""
    print(code)

def threshold():
    code=r"""
import cv2
import numpy as np
from matplotlib import pyplot as plt
from image_func import threshold_image

# Load the image
img = cv2.imread(r"C:\IP practicals\floweer.jpg")
# Set the threshold value
threshold_value = 127

# Perform thresholding using the threshold_image function
thresh = threshold_image(img, threshold_value)

# Plot the images manually
titles = ['Original Image', 'Thresholded']
images = [img, thresh]
for i in range(2):
    plt.subplot(1, 2, i + 1)
    plt.imshow(images[i], 'gray', vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)

def gradient():
    code=r"""
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from image_func import plot_image, apply_gradient, apply_laplacian

im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))

# Apply gradient
im_x, im_y, im_mag, im_dir = apply_gradient(im)

# Plot the gradient results
plt.gray()
plt.figure(figsize=(20, 15))
plt.subplot(231)
plot_image(im, 'Original')
plt.subplot(232)
plot_image(im_x, 'Gradient x')
plt.subplot(233)
plot_image(im_y, 'Gradient y')
plt.subplot(234)
plot_image(im_mag, '||Gradient||')
plt.legend(prop={'size': 20})
plt.show()

# Apply Laplacian
im1 = apply_laplacian(im)

# Plot the Laplacian result
plt.gray()
plt.figure(figsize=(10, 5))
plt.subplot(121)
plot_image(im, 'Original')
plt.subplot(122)
plot_image(im1, 'Laplacian Convolved')
plt.show()
"""
    print(code)

def sharpening():
    code=r"""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)

def edge():
    code=r"""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)

def canny():
    code=r"""
import matplotlib.pylab as pylab
from skimage import feature
from image_func import plot_canny, generate_noisy_square, canny_edge_detection

# Generate noisy image of a square
image = generate_noisy_square()

# Perform Canny edge detection
edges1, edges2 = canny_edge_detection(image)

# Display results
# Display results
fig, ax = pylab.subplots(nrows=1, ncols=3, figsize=(8, 3))

plot_canny(image, 'noisy image', ax=ax[0])

plot_canny(edges1, r'Canny filter, $\sigma=1$', ax=ax[1])

plot_canny(edges2, r'Canny filter, $\sigma=3$', ax=ax[2])

pylab.show()


"""
    print(code)

def sobel():
    code=r"""
from skimage.io import imread
from PIL import Image
import matplotlib.pylab as pylab
import numpy as np
from skimage import filters
from image_func import plot_image ,sobel_edge_detection

image_path = r"C:\IP practicals\floweer.jpg"

# Open and convert the image to grayscale
im = Image.open(image_path).convert('L')
im_array = np.array(im)
# Perform Sobel edge detection
edges_x, edges_y = sobel_edge_detection(im_array)

# Display the images
pylab.gray()
pylab.figure(figsize=(15, 15))
pylab.subplot(2, 2, 1)
plot_image(im, 'Original')
pylab.subplot(2, 2, 2)
plot_image(edges_x, 'Sobel X')
pylab.subplot(2, 2, 3)
plot_image(edges_y, 'Sobel Y')
pylab.subplot(2, 2, 4)
plot_image(edges_x + edges_y, 'Sobel X + Y')
pylab.subplots_adjust(wspace=0.1, hspace=0.1)
pylab.show()
"""
    print(code)

def erosion():
    code=r"""
import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
import matplotlib.pylab as pylab
from image_func import threshold_image, erosion, dilation, opening, closing, plot_image


# Erosion and Dilation
img = cv2.imread(r"C:\IP practicals\floweer.jpg", 0)
bw_img = threshold_image(img, 127)

kernel_size = 5
img_erosion = erosion(img, kernel_size)
img_dilation = dilation(img, kernel_size)

plt.figure(figsize=(5, 5))
plot_image(img, "ORIGINAL IMAGE")
plt.show()
plot_image(img_erosion, "EROSION")
plt.show()
plot_image(img_dilation, "DILATION")
plt.show()

# Image opening and closing
im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))
im[im <= 0.5] = 0
im[im > 0.5] = 1

disk_size = 6
im_opening = opening(im, disk_size)
im_closing = closing(im, disk_size)

pylab.gray()
pylab.figure(figsize=(20, 10))
plot_image(im, "original")
plot_image(im_opening, "opening with disk size 6")
plt.show()
plot_image(im_closing, "closing with disk size 6")
pylab.show()
"""
    print(code)

def segmentation():
    code=r"""
from image_func import load_image, convert_to_gray, threshold_image, segment_image,plot_images
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Loading original image
img = load_image(r'C:\IP practicals\floweer.jpg')

# Converting to grayscale
gray = convert_to_gray(img)

# Thresholding image
thresh = threshold_image(gray)

# Segmenting the image
segmented = segment_image(thresh)


# Displaying final output
plt.figure(figsize=(10, 10))
plt.subplot(2, 2, 1)
plot_images(img, "Original Image")
plt.subplot(2, 2, 2)
plot_images(gray, "Grayscale Image")
plt.subplot(2, 2, 3)
plot_images(thresh, "Threshold Image")
plt.subplot(2, 2, 4)
plot_images(segmented, "Segmented Image")
plt.tight_layout()
plt.show()
"""
    print(code)

def all():
    code="""
fft()
convolution()
dft()
log()
power()
contrast()
histogram()
threshold()
gradient()
sharpening()
edge()
canny()
sobel()
erosion()
segmentation()
"""
    print(code)



def onlySegmentation():
    code=r"""
import numpy as np
import cv2
from matplotlib import pyplot as plt

# Loading original image
img = cv2.imread(r'bird.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Converting to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Converting to binary inverted image
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Segmenting the images
kernel = np.ones((3, 3), np.uint8)
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=15)
bg = cv2.dilate(closing, kernel, iterations=1)
dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 0)
ret, fg = cv2.threshold(dist_transform, 0.02 * dist_transform.max(), 255, 0)

# Plotting the images
plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.imshow(img, cmap="gray")
plt.axis('off')
plt.title("Original Image")

plt.subplot(2, 2, 2)
plt.imshow(gray, cmap="gray")
plt.axis('off')
plt.title("GrayScale Image")

plt.subplot(2, 2, 3)
plt.imshow(thresh, cmap="gray")
plt.axis('off')
plt.title("Threshold Image")

plt.subplot(2, 2, 4)
plt.imshow(fg, cmap="gray")
plt.axis('off')
plt.title("Segmented Image")

plt.show()
"""
    print(code)


def onlyErosionDilation():
    code=r"""
import cv2
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
import matplotlib.pylab as pylab
from image_func import threshold_image, erosion, dilation, opening, closing, plot_image


# Erosion and Dilation
img = cv2.imread(r"bird.jpg", 0)
bw_img = threshold_image(img)

kernel_size = 5
img_erosion = erosion(img, kernel_size)
img_dilation = dilation(img, kernel_size)

plt.figure(figsize=(5, 5))
plot_image(img, "ORIGINAL IMAGE")
plt.show()
plot_image(img_erosion, "EROSION")
plt.show()
plot_image(img_dilation, "DILATION")
plt.show()

# Image opening and closing
im = rgb2gray(imread(r"bird.jpg"))
im[im <= 0.5] = 0
im[im > 0.5] = 1

disk_size = 6
im_opening = opening(im, disk_size)
im_closing = closing(im, disk_size)

pylab.gray()
pylab.figure(figsize=(20, 10))
plot_image(im, "original")
plot_image(im_opening, "opening with disk size 6")
plt.show()
plot_image(im_closing, "closing with disk size 6")
pylab.show()
"""
    print(code)


def onlyRobertPrewitt():
    code=r"""
import numpy as np
from skimage import filters
from PIL import Image
import matplotlib.pylab as pylab
from image_func import plot_img

def edge_detection(image_path):
    im = Image.open(image_path).convert('L')
    im_arr = np.asarray(im)
    pylab.gray()
    pylab.figure(figsize=(15, 15))
    pylab.subplot(3, 2, 1), plot_img(im, 'Original Image')
    edges = filters.roberts(im_arr)
    pylab.subplot(3, 2, 2), plot_img(edges, 'Roberts')
    edges = filters.scharr(im_arr)
    pylab.subplot(3, 2, 3), plot_img(edges, 'Scharr')
    edges = filters.sobel(im_arr)
    pylab.subplot(3, 2, 4), plot_img(edges, 'Sobel')
    edges = filters.prewitt(im_arr)
    pylab.subplot(3, 2, 5), plot_img(edges, 'Prewitt')
    edges = np.clip(filters.laplace(im_arr), 0, 1)
    pylab.subplot(3, 2, 6), plot_img(edges, 'Laplace')
    pylab.subplots_adjust(wspace=0.1, hspace=0.1)
    pylab.show()

# Set the path to the image
image_path = r"bird.jpg"

# Call the edge_detection function
edge_detection(image_path)
"""
    print(code)


def onlySobel():
    code=r"""
import numpy as np
from skimage import filters
from skimage.io import imread
import matplotlib.pyplot as plt

im = imread(r"bird.jpg", as_gray=True)

plt.gray()
fig, axes = plt.subplots(2, 2, figsize=(15, 15))

titles = ['Original', 'Sobel x', 'Sobel y', 'Sobel']
images = [im, filters.sobel_h(im), filters.sobel_v(im), filters.sobel(im)]

for ax, title, image in zip(axes.ravel(), titles, images):
    ax.imshow(np.clip(image, 0, 1), cmap='gray')
    ax.set_title(title)
    ax.axis('off')

plt.tight_layout()
plt.show()
"""
    print(code)


def onlyCanny():
    code=r"""
import matplotlib.pyplot as plt
from skimage.util import random_noise
from skimage import feature

# Generate noisy image of a square
image = random_noise(feature.square(128), mode='speckle', mean=0.05)

# Compute the Canny filter for two values of sigma
edges1 = feature.canny(image)
edges2 = feature.canny(image, sigma=3)

# Display results
fig, ax = plt.subplots(1, 3, figsize=(8, 3))

ax[0].imshow(image, cmap='gray')
ax[0].set_title('noisy image', fontsize=10)

ax[1].imshow(edges1, cmap='gray')
ax[1].set_title(r'Canny filter, $\sigma=1$', fontsize=10)

ax[2].imshow(edges2, cmap='gray')
ax[2].set_title(r'Canny filter, $\sigma=3$', fontsize=10)

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()
"""
    print(code)


def onlySharpening():
    code=r"""
import numpy as np
from skimage import filters, img_as_float, color
from skimage.io import imread
import matplotlib.pyplot as plt

def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image, cmap='gray')
    plt.axis('off')

def sharpen_image(image):
    blurred = filters.gaussian(image, sigma=3)
    detail = np.clip(image - blurred, 0, 1)
    alpha_values = [1, 5, 10]

    fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
    axes = axes.ravel()
    axes[0].set_title('Original Image', size=15)
    axes[0].imshow(image, cmap='gray')
    
    axes[1].set_title('Blurred Image (sigma=3)', size=15)
    axes[1].imshow(blurred, cmap='gray')
    
    axes[2].set_title('Detail Image', size=15)
    axes[2].imshow(detail, cmap='gray')
    for i, alpha in enumerate(alpha_values):
        sharpened = np.clip(image + alpha * detail, 0, 1)
        axes[3+i].imshow(sharpened, cmap='gray')
        axes[3+i].set_title(f'Sharpened Image (alpha={alpha})', size=15)
    for ax in axes:
        ax.axis('off')
    fig.tight_layout()
    plt.show()

# Load the grayscale image
image = color.rgb2gray(imread(r"flower.jpg"))

# Perform sharpening and display the results
sharpen_image(image)
"""
    print(code)


def onlyGradientLaplacian():
    code=r"""
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from image_func import plot_image, apply_gradient, apply_laplacian

im = rgb2gray(imread(r"C:\IP practicals\floweer.jpg"))

# Apply gradient
im_x, im_y, im_mag, im_dir = apply_gradient(im)

# Plot the gradient results
plt.gray()
plt.figure(figsize=(20, 15))
plt.subplot(231)
plot_image(im, 'Original')
plt.subplot(232)
plot_image(im_x, 'Gradient x')
plt.subplot(233)
plot_image(im_y, 'Gradient y')
plt.subplot(234)
plot_image(im_mag, '||Gradient||')
plt.legend(prop={'size': 20})
plt.show()

# Apply Laplacian
im1 = apply_laplacian(im)

# Plot the Laplacian result
plt.gray()
plt.figure(figsize=(10, 5))
plt.subplot(121)
plot_image(im, 'Original')
plt.subplot(122)
plot_image(im1, 'Laplacian Convolved')
plt.show()
"""
    print(code)


def onlyContrasting():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def plot_image(image, title=""):
    plt.title(title, size=10)
    plt.imshow(image)
    plt.axis('off')
def plot_hist(channel, title=""):
    plt.hist(np.array(channel).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    plt.xlabel('Pixel Values', size=20)
    plt.ylabel('Frequency', size=20)
    plt.title(title, size=10)
image_path = r"flower.jpg"
im = Image.open(image_path)
im_r, im_g, im_b = im.split()
plt.style.use('ggplot')
plt.figure(figsize=(15, 5))
plt.subplot(121)
plot_image(im)
plt.subplot(122)
plot_hist(im_r, "Red Channel")
plot_hist(im_g, "Green Channel")
plot_hist(im_b, "Blue Channel")
plt.yscale('log')
plt.show()

def contrast(c):
    return 0 if c < 50 else (255 if c > 150 else int((255 * c - 22950) / 48))

imc = im.point(contrast)
im_rc, im_gc, im_bc = imc.split()

plt.style.use('ggplot')
plt.figure(figsize=(15, 5))

plt.subplot(121)
plot_image(imc)
plt.subplot(122)
plot_hist(im_rc, "Contrast-Adjusted Red Channel")
plot_hist(im_gc, "Contrast-Adjusted Green Channel")
plot_hist(im_bc, "Contrast-Adjusted Blue Channel")
plt.yscale('log')
plt.show()
"""
    print(code)


def onlyThresholding():
    code=r"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img = cv.imread(r"C:\Users\Aditi\Pictures\IP\flower.jpg", 0)
ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
ret, thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
ret, thresh3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
ret, thresh4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
ret, thresh5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)
titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
for i in range(6):
    plt.subplot(2, 3, i + 1)
    plt.imshow(images[i], 'gray', vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)


def onlyDFT():
    code=r"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

img=cv2.imread(r"flower.jpg",0)

optimalImg=cv2.copyMakeBorder(img, 0, cv2.getOptimalDFTSize(img.shape[0])
                              -img.shape[0], 0, cv2.getOptimalDFTSize(img.shape[1])
                              -img.shape[1], cv2.BORDER_CONSTANT, value=0)
dft_shift=np.fft.fftshift(cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT))
magnitude_spectrum=20*np.log(cv2.magnitude(dft_shift[:,:,0],
                                           dft_shift[:,:,1])+1)
result=cv2.magnitude(cv2.idft(np.fft.ifftshift(dft_shift))[:,:,0],
                     cv2.idft(np.fft.ifftshift(dft_shift))[:,:,1])

images=[optimalImg, magnitude_spectrum, result]
imagesTitles=["Input", "DFT", "Output"]

for i in range(len(images)):
    plt.subplot(1, 3, i+1)
    plt.imshow(images[i], cmap="gray")
    plt.title(imagesTitles[i])
    plt.xticks([])
    plt.yticks([])
plt.show()
"""
    print(code)


def onlyConvCorr():
    code=r"""
import cv2
import matplotlib.pyplot as plt
import numpy as np
from image_func import apply_convolution, apply_correlation
img=cv2.imread(r"flower.jpg")
#img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

k1=np.ones((3,3), np.float32)/9
c1=apply_convolution(img, k1)

k2=np.array([[0, -1, 0],
             [-1, 5, -1],
             [0, -1, 0]])
c2=apply_correlation(img, k2)

fig, axes=plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(img)
axes[0].axis("off")
axes[0].set_title("Original")

axes[1].imshow(c1)
axes[1].axis("off")
axes[1].set_title("Convolution")
 
axes[2].imshow(c2)
axes[2].axis("off")
axes[2].set_title("Correlation")

plt.tight_layout()
plt.show()
"""
    print(code)


def onlyHaar():
    code=r"""
import cv2
import numpy as np

# Load the image
image = cv2.imread(r"bird.jpg", 0)

# Convert the image to floating-point data type
image_float = np.float32(image)

# Apply the DCT
transformed = cv2.dct(image_float)

# Display the transformed image
cv2.imshow("Transformed Image", transformed)
"""
    print(code)


def onlyColorModel():
    code=r"""
import cv2

# Load the image
image = cv2.imread(r"bird.jpg")

# Convert the image to a different color model
converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the transformed image
cv2.imshow("Converted Image", converted_image)
"""
    print(code)


def onlyHistogram():
    code=r"""
import cv2
from matplotlib import pyplot as plt
img = cv2.imread(r"flower.jpg",0)
hist = cv2.calcHist([img],[0],None,[256],[0,256])
eq = cv2.equalizeHist(img)
cdf = hist.cumsum()
cdfnmhist = cdf * hist.max()/ cdf.max()
histeq = cv2.calcHist([eq],[0],None,[256],[0,256])
cdfeq = histeq.cumsum()
cdfnmhisteq = cdfeq * histeq.max()/ cdf.max()
plt.subplot(221), plt.imshow(img,'gray')
plt.subplot(222), plt.plot(hist), plt.plot(cdfnmhist)
plt.subplot(223), plt.imshow(eq,'gray')
plt.subplot(224), plt.plot(histeq), plt.plot(cdfnmhisteq)
plt.xlim([0,256])
plt.show()
"""
    print(code)


def onlyPowerLaw():
    code=r"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Read the image
img = cv2.imread(r"flower.jpg")
# Display the original image
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()
# Define gamma values
gamma_values = [0.1, 0.5, 1.2, 2.2, 5]
# Apply gamma correction and save edited images
for gamma in gamma_values:
    gamma_corrected = np.array(255 * (img / 255) ** gamma, dtype='uint8')
    cv2.imwrite('gamma_transformed' + str(gamma) + '.jpg', gamma_corrected)
    plt.imshow(cv2.cvtColor(gamma_corrected, cv2.COLOR_BGR2RGB))
    plt.show()
"""
    print(code)


def onlyLog():
    code=r"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
# Read the image
img = cv2.imread(r"C:\Users\Aditi\OneDrive\Pictures\IP\flower.jpg")
# Apply log transform
log_transformed = 255 * np.log(1 + img.astype(np.float32)) / np.log(1 + np.max(img))
# Convert the data type
log_transformed = log_transformed.astype(np.uint8)
# Save the output image
cv2.imwrite(r"C:\Users\Aditi\Pictures\IP\flower1.jpg", log_transformed)
# Display the original and log-transformed images
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(log_transformed, cv2.COLOR_BGR2RGB))
plt.title('Log-Transformed Image')
plt.show()
"""
    print(code)
    
def onlyall():
    code=r"""
onlySegmentation()
onlyErosionDilation()
onlyRobertPrewitt()
onlySobel()
onlyCanny()
onlySharpening()
onlyGradientLaplacian()
onlyContrasting()
onlyThresholding()
onlyDFT()
onlyConvCorr()
onlyHaar()
onlyColorModel()
onlyHistogram()
onlyPowerLaw()
onlyLog()
"""
    print(code)



def symptomCheckerES():
    code=r"""
name = input("Enter your name: ")
fever = input("Do you have fever? (yes/no) ").lower()
cough = input("Do you have cough? (yes/no) ").lower()
sob = input("Do you have shortness of breath? (yes/no) ").lower()
st = input("Do you have sore throat? (yes/no) ").lower()
mp = input("Do you have muscle pain? (yes/no) ").lower()
hc = input("Do you have headache? (yes/no) ").lower()
diarrhea = input("Do you have diarrhea? (yes/no) ").lower()
conjuctivitis = input("Do you have conjuctivitis? (yes/no) ").lower()
lot = input("Do you have Loss of Taste? (yes/no) ").lower()
cp = input("Do you have Chest pain or Pressure? (yes/no) ").lower()
lsp = input("Do you have Loss of Speech or Movement? (yes/no) ").lower()

flu_symptoms = (fever=="yes" and cough=="yes" and sob=="yes" and st=="yes" and mp=="yes" and hc=="yes")
corona_symptoms = (diarrhea=="yes" and st=="yes" and fever=="yes" and cough=="yes" and conjuctivitis=="yes" and lot=="yes")
common_cold = (fever=="yes" and cough=="yes")

if flu_symptoms:
    print(name + " YOU HAVE FLU...")
    med = input("Aditi!, would you like to look at same medicine for the flu? (yes/no): ").lower()
    if med == "yes":
        print("Disclaimer: Contact a doctor for better guidance.")
        print("There are four FDA-approved antiviral drugs recommended by CDC to treat flu this season: ")
        print("1. Oseltamivir phosphate")
        print("2. Zanamivir")
        print("3. Peramivir")
        print("4. Baloxavir marboxil")
elif corona_symptoms:
    print(name + " YOU HAVE Corona")
    med = input("Aditi!, would you like to look at some remedies for Corona? (yes/no): ").lower()
    if med == "yes":
        print("TAKE VACCINE AND QUARANTINE")
elif common_cold:
    print(name + " YOU HAVE COMMON CODE")
    med = input("Aditi!, would you like to look at some remedies for Corona? (yes/no): ").lower()
    if med == "yes":
        print("Disclaimer: Contact a doctor for better guidance")
        print("Treatment consists of abti-inflammatories and decongestants. Most people d=recover on their own. ")
        print("1. Nonsteroidal abti-inflammatory drug")
        print("2. Analgesic")
        print("3. Antihistamine")
        print("4. Cough medicine")
        print("5. Decongestant")
else:
    print("Unable to identify")


Program: 2 Flu disease checker:
info=[]
name=input("Enter your name: ")
info.append(name)
age=int(input("Enter your age: "))
info.append(age)
print("----------------------------------------------")
a=["Fever", "Headache", "Tiredness", "Vomitting"]
b=["Urinate a lot", "Feels thirsty", "Weight loss", "Blurry vision", "Feels very hungry", "Feels very tired"]
print("----------------------------------------------")
print(a, b)
symp=input("Enter symptoms as above separated by comm ")
lst=symp.split(",")
print(info)
print("Symptoms: ")
for i in lst:
    print(i)
if i.strip() in a:
    print("You May Have Malaria\n...visit a Doctor")
elif i.strip() in b:
    print("You May Have Diabetes\n...Consume less Sugar")
else:
    print("Symptoms does not Match")


"""
    print(code)


def AIBot():
    code=r"""
Open cmd and install pip –
pip install aiml 
pip install python-aiml 

basic_chat.aiml
<aiml version="1.0.1" encoding="UTF-8">
<!-- basic_chat.aiml -->
 
    <category>
        <pattern>HELLO *</pattern>
        <template>
            Well, Hello PCS!
        </template>
    </category>
 
    <category>
        <pattern>WHAT ARE YOU</pattern>
        <template>
            I'm a bot, and I'm silly!
        </template>
    </category>
 
    <category>
        <pattern>WHAT DO YOU DO</pattern>
        <template>
            I'm here to motivate you!
        </template>
    </category>
 
    <category>
        <pattern>WHO AM I</pattern>
        <template>
            You are a Professional Footballer....
        </template>
    </category>
 
</aiml>
 
std-startup.xml
<aiml version="1.0.1" encoding="UTF-8">
<!--  std-startup.xml  -->
<!--  Category is an atomic AIML unit  -->
<category>
<!--  Pattern to match in user input  -->
<!--  If user enters "LOAD AIML B"  -->
<pattern>LOAD AIML B</pattern>
<!--  Template is the response to the pattern  -->
<!--  This learn an aiml file  -->
<template>
<learn>basic_chat.aiml</learn>
<!--  You can add more aiml files here  -->
<!-- <learn>more_aiml.aiml</learn> -->
</template>
</category>
</aiml>
 
AI_Prac2_Bot.py
import aiml
kernel=aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")
while True:
    input_text=input(">Human:")
    response=kernel.respond(input_text)
    print(">Bot: "+response)

"""
    print(code)


def bayesTheorem():
    code=r"""
Program: 1
def bayes_theorem(p_h, p_e_given_h, p_e_given_not_h):
    not_h= 1 - p_h
    p_e= p_e_given_h * p_h + p_e_given_not_h * not_h
    p_h_given_e= (p_e_given_h * p_h)/p_e
    return p_h_given_e
p_h=float(input("Enter probability of hk having cold P(H): "))
p_e_given_h=float(input("Enter probability of hk observed sneezing when he had cold P(E|H): "))
p_e_given_not_h=float(input("Enter probability of hk observed sneezing when he did not have cold P(E|~H): "))
result=bayes_theorem(p_h, p_e_given_h, p_e_given_not_h)
print("Hk probability of having cold given that he sneezes is P(H|E)= ", round(result, 2))

Program: 2
def bayes_theorem(p_h, p_e_given_h, p_e_given_not_h):
    not_h= 1 - p_h
    p_e= p_e_given_h * p_h + p_e_given_not_h * not_h
    p_h_given_e= (p_e_given_h * p_h)/p_e
    return p_h_given_e
p_h=float(input("Enter probability of hk having cold: "))
p_e_given_h=float(input("Enter probability of hk observed sneezing when he had cold: "))
p_e_given_not_h=float(input("Enter probability of hk observed sneezing when he did not have cold: "))
result=bayes_theorem(p_h, p_e_given_h, p_e_given_not_h)
print("Hk probability of having cold given that he sneezes is P(H|E)= ", round(result, 2))

Program: 3
def drug_user(prob_th=0.5, sensitivity=0.97, specificity=0.95, prevelance=0.005, verbose=True):
    p_user=prevelance
    p_non_user=1-prevelance
    p_pos_user=sensitivity
    p_neg_user=1-specificity
    p_pos_non_user=1-specificity
    num=p_pos_user*p_user
    den=p_pos_user*p_user+p_pos_non_user*p_non_user
    prob=num/den
    print("Probability of the test-taker being a drug user is ", round(prob, 1))
    if verbose:
        if prob > prob_th:
            print("The test-taker could be an user")
        else:
            print("The test-taker may not be an user")
        return prob
drug_user()
"""
    print(code)


def conditionalProb():
    code=r"""
def conditional_and_joint_probability(A, B, sample_space):
    prob_A_and_B = len(set(A) & set(B))/len(sample_space)
    prob_B = len(B)/len(sample_space)
    prob_A_given_B = prob_A_and_B/prob_B
    return prob_A_and_B, prob_A_given_B
sample_space = range(1, 11)
A = [2, 4, 6, 8, 10]
B = [1, 2, 3, 4, 5]
print("Set(A): ", A)
print("Set(B): ", B)
prob_A_and_B, prob_A_given_B = conditional_and_joint_probability(A, B, sample_space)
print("Joint probability P(A n B) = ", prob_A_and_B)
print("Conditional probability P(A | B) = ", prob_A_given_B)

"""
    print(code)


def familyTree():
    code=r"""
male(j1).    %brother
male(k).     %father
male(a).     %uncle
male(v).    %grandfather
male(s).		%greatgrandfather

female(a1).      %me
female(a2).     %sister
female(j2).     %cousin
female(sk).     %mother
female(aa).     %aunt
female(sv).     %grandmother 
female(ps).     %greatgrandmother 

parent(k,a1).
parent(sk,a1).
parent(k,a2).
parent(sk,a2).
parent(a,j1).
parent(aa,j1).

mother(X,Y):-parent(X,Y),female(X).
father(X,Y):-parent(X,Y), male(X).
sibling(X,Y):-parent(Z,X), parent(Z,Y), X \= Y.
grandparent(X,Y):-parent(X,Z),parent(Z,Y).
greatgrandparent(X,Y):-parent(X,Z),grandparent(Z,Y).
uncle(X,Y):- male(X), sibling(X,P), parent(P,Y).
aunt(X,Y):- female(X), sibling(X,P), parent(P,Y).
"""
    print(code)


def fuzzyOperations():
    code=r"""
Program: 1
A={"a":0.2, "b":0.3, "c":0.6, "d":0.6}
B={"a":0.9, "b":0.9, "c":0.4, "d":0.5}
print("The first fuzzy set: ", A)
print("The second fuzzy set: ", B)
#Union
result={}
for i in A:
    if(A[i]>B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("\nUnion of sets A and B is(A U B): ", result)
#Intersection
result={}
for i in A:
    if(A[i]<B[i]):
        result[i]=A[i]
    else:
        result[i]=B[i]
print("\nIntersection of sets A and B is(A n B): ", result)
#Complement
result={}
for i in A:
    result[i]=round(1-A[i], 2)
print("\nComplement of set A is(A'): ", result)
for i in B:
    result[i]=round(1-B[i], 2)
print("Complement of set B is(B'): ", result)
#Difference
result={}
for i in A:
    result[i]=round(min(A[i], 1-B[i]), 2)
print("\nDifference of sets A and B is(A - B):", result)

Program: 2
#pip install fuzzywuzzy
 from fuzzywuzzy import fuzz
from fuzzywuzzy import process
 s1 = "I love GeeksforGeeks"
 s2 = "I am loving GeeksforGeeks"
 print("FuzzyWuzzy Ratio: ", fuzz.ratio(s1, s2))
print("FuzzyWuzzy PartialRatio: ", fuzz.partial_ratio(s1, s2))
print("FuzzyWuzzy TokenSortRatio: ", fuzz.token_sort_ratio(s1, s2))
print("FuzzyWuzzy TokenSetRatio: ", fuzz.token_set_ratio(s1, s2))
print("FuzzyWuzzy Weighted Ratio: ", fuzz.WRatio(s1, s2),'\n\n')
# for process library,
query = 'geeks for geeks'
choices = ['geek for geek', 'geek geek', 'g. for geeks']
print("List of ratios: ")
print(process.extract(query, choices), '\n')
print("Best among the above list: ",process.extractOne(query, choices))
"""
    print(code)


def simulateSupervised():
    code=r"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

#Generate random data
np.random.seed(0)
x=2*np.random.rand(100,1)
y=4+3*x+np.random.rand(100,1)

#split data into train and test data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

#Instantiate linear model
model = LinearRegression()

#Train the model
model.fit(x_train, y_train)

#Make predictions
predictions=model.predict(x_test)

#Plot training data
plt.scatter(x_train, y_train, color='blue', label='Training data')
plt.scatter(x_test, y_test, color='red', label='Testing data')
plt.plot(x_test, predictions, color='green', linewidth=3, label='Predictions')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear regression')
plt.legend()
plt.show()
"""
    print(code)


def simulateUnsupervised():
    code=r"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
np.random.seed(0)
x=np.random.randn(100, 2)
plt.scatter(x[:, 0], x[:, 1], s=50)
plt.title("Randomly generated data points")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()

#Applying k-means clustering
kmeans=KMeans(n_clusters=3)
kmeans.fit(x)

#Getting centroids
centroids=kmeans.cluster_centers_
labels=kmeans.labels_

#Visualizing clustered data points
plt.scatter(x[:,0], x[:,1], s=50, cmap='viridis')
plt.scatter(centroids[:,0], centroids[:,1], marker='*', c='red', s=200, label='Centroids')
plt.title("K-means clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.legend()
plt.show()
"""
    print(code)

def clustering():
    code=r"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc

# Load customer data
customer_data = pd.read_csv("Mall_Customers.csv")

# Extract relevant features
data = customer_data[['Annual Income (k$)', 'Spending Score (1-100)']].values

# Perform hierarchical clustering
cluster = AgglomerativeClustering(n_clusters=5)
cluster_labels = cluster.fit_predict(data)

# Plot dendrogram
plt.figure(figsize=(10, 7))
plt.title("Customer Dendrogram")
shc.dendrogram(shc.linkage(data, method='ward'))

# Plot clustered data
plt.figure(figsize=(10, 7))
plt.scatter(data[:, 0], data[:, 1], c=cluster_labels, cmap='rainbow')
plt.show()
"""
    print(code)

def svm():
    code=r"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC, SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Titanic dataset
titanic = pd.read_csv('train.csv')

# Preprocessing
titanic.drop(['Name', 'Ticket'], axis=1, inplace=True)
titanic['Cabin'].fillna(titanic['Cabin'].value_counts().idxmax(), inplace=True)
titanic['Embarked'].fillna(titanic['Embarked'].value_counts().idxmax(), inplace=True)
titanic['Age'].fillna(titanic['Age'].mean(), inplace=True)
titanic_cat = titanic.select_dtypes(object).apply(LabelEncoder().fit_transform)
titanic_num = titanic.select_dtypes(np.number).drop('PassengerId', axis=1)
titanic_final = pd.concat([titanic_cat, titanic_num], axis=1)

# Train-test split
X = titanic_final.drop('Survived', axis=1)
Y = titanic_final['Survived']
split_idx = int(0.80 * len(X))
X_train, Y_train = X[:split_idx], Y[:split_idx]
X_test, Y_test = X[split_idx:], Y[split_idx:]

# Model training and evaluation
models = [LogisticRegression(), KNeighborsClassifier(), GaussianNB(), LinearSVC(), SVC(kernel='rbf'),
          DecisionTreeClassifier(), RandomForestClassifier()]
for model in models:
    model_fit = model.fit(X_train, Y_train)
    Y_pred = model_fit.predict(X_test)
    accuracy = accuracy_score(Y_pred, Y_test) * 100
    print(f"{model.__class__.__name__} is {accuracy:.2f}% accurate")
"""
    print(code)


def intelligentClothesAgent():
    code=r"""
class ClothesAgent:
    def __init__(self):
        self.weather = None
    
    def get_weather(self):
        self.weather = input("Enter the weather (Sunny, Rainy, Windy, Snowy): ").lower()
    
    def suggest_clothes(self):
        suggestions = {
            "sunny": "light clothes, sunglasses, and sunscreen",
            "rainy": "an umbrella, raincoat, and waterproof shoes",
            "windy": "layers and a jacket",
            "snowy": "a heavy coat, gloves, and boots"
        }
        if self.weather in suggestions:
            print(f"It is {self.weather} outside. You should wear {suggestions[self.weather]}.")
        else:
            print("Sorry, I don't understand the weather conditions. Please enter sunny, rainy, windy, or snowy.")

def main():
    agent = ClothesAgent()
    agent.get_weather()
    agent.suggest_clothes()

if __name__ == "__main__":
    main()
"""
    print(code)



def simulateLanParser():
    code=r"""
import string
def sentence_segment(text):
    return [sentence.strip() for sentence in text.split('.') + text.split('!') + text.split('?') if sentence.strip()]

def remove_punctuation(input_string):
    return ''.join(char for char in input_string if char not in string.punctuation)

def convert_to_lower(s):
    return s.lower()

def tokenize(s):
    return s.split()

text = "Hello, NLP world!! In this example, we are going to do the basics of Text processing which will be used later."

sentences = sentence_segment(text)
punc_removed_text = remove_punctuation(text)
lower_text = convert_to_lower(punc_removed_text)
tokenized_text = tokenize(lower_text)

print(sentences)
print("\n")
print(tokenized_text)
print("\n")

# Tokenization using str.split()
tokens_split = text.split()
print(tokens_split)
print("\n")

sentence = "We're going to John's house today."
tokens_sentence = sentence.split()
print(tokens_sentence)
"""
    print(code)


def feedforward():
    code=r"""
import numpy as np
def relu(n):
    if n<0:
        return 0
    else:
        return n
inp=np.array([[-1,2],[2,2],[3,3]])
weights=[np.array([3,3]),np.array([1,5]),np.array([3,3]),np.array([1,5]),np.array([2,-1])]
for x in inp :
    node0=relu((x*weights[0]).sum())
    node1=relu((x*weights[1]).sum())
    node2=relu(([node0,node1]*weights[2]).sum())
    node3=relu(([node0,node1]*weights[3]).sum())
    op=relu(([node2,node3]*weights[4]).sum())
    print(x,op)
"""
    print(code)
