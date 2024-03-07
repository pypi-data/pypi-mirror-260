import os
import numpy as np
from skimage import io
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def cell_segment(image_path, num_clusters=4):
    image = io.imread(image_path)
    w, h, d = original_shape = tuple(image.shape)
    image_2d = np.reshape(image, (w * h, d))
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(image_2d)
    labels = kmeans.predict(image_2d)
    segmented_image = np.reshape(labels, (w, h))
    return segmented_image

def img_save(segmented_image, save_path, image_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    filename = os.path.basename(image_path)
    save_name = os.path.join(save_path, 'segmented_' + os.path.splitext(filename)[0] + '.png')
    segmented_image_normalized = (segmented_image / np.max(segmented_image) * 255).astype(np.uint8)
    io.imsave(save_name, segmented_image_normalized)

def plot_img(segmented_image):
    plt.imshow(segmented_image, cmap='gray')  # Removed vmin and vmax for automatic scaling
    plt.title('Segmented Image')
    plt.axis('off')
    plt.show()

def cell_folder(input_folder, output_folder, num_clusters=4):
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input_folder, filename)
            segmented_image = cell_segment(image_path, num_clusters)
            img_save(segmented_image, output_folder, image_path)