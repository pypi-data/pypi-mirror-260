import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float, io
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.metrics import peak_signal_noise_ratio
from skimage.util import random_noise

from skimage import io, img_as_float, img_as_ubyte
from PIL import Image
import os
from skimage import io, color

def denoise_images(input_folder, result_folder=None):
    files = os.listdir(input_folder)

    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, file)
            image = io.imread(image_path)
            image = img_as_float(image)

            sigma_est = np.mean(estimate_sigma(image, channel_axis=-1))

            patch_kw = dict(patch_size=5,      # 5x5 patches
                            patch_distance=6,  # 13x13 search area
                            channel_axis=-1)

            denoised_image = denoise_nl_means(image, h=0.6 * sigma_est, sigma=sigma_est,
                                               fast_mode=True, **patch_kw)

            denoised_image_uint8 = img_as_ubyte(denoised_image)

            if result_folder:
                if not os.path.exists(result_folder):
                    os.makedirs(result_folder)
                save_path = os.path.join(result_folder, file)
            else:
                save_path = image_path

            io.imsave(save_path, denoised_image_uint8)

def img_to_gray(input_folder, result_folder=None):
    files = os.listdir(input_folder)

    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_folder, file)
            image = io.imread(image_path)
            gray_image = color.rgb2gray(image)
            gray_image_uint8 = (gray_image * 255).astype('uint8')
            pil_image = Image.fromarray(gray_image_uint8)

            # Determine the result folder
            if result_folder:
                if not os.path.exists(result_folder):
                    os.makedirs(result_folder)
                save_path = os.path.join(result_folder, file)
            else:
                save_path = image_path

            pil_image.save(save_path)
            print(f"{file} converted to grayscale and saved.")