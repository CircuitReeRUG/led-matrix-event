# This shit doesn't really work

import numpy as np
from PIL import Image

def np_arr_to_bytearray(np_arr):
    # Convert numpy array to bytearray
    return bytearray(np.packbits(np_arr))

def image_to_binary_array(png_path, size=(8, 8), threshold=240):
    # Load image
    image = Image.open(png_path)
    # Convert image to  and invert
    
    gray_image = image.convert('L')
    
    # Resize image to 8x8 pixels
    resized_image = gray_image.resize(size, Image.LANCZOS)
    
    # Convert resized image to numpy array
    data = np.array(resized_image)

    # Create a binary array based on a threshold
    # Pixels darker than the threshold are considered colored (1), others are 0
    binary_array = data < threshold
    
    return np_arr_to_bytearray(binary_array)

binary_array = image_to_binary_array('circuitree_waving.png')
print(binary_array)
