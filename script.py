from PIL import Image
from tqdm import tqdm
import numpy as np
import rembg
import cv2
import os

def remove_background(input_image):
    try:
        input_array = np.array(input_image)
        output_array = rembg.remove(input_array)
        return output_array
    except Exception as e:
        print("error: ", e)
        return None

def run(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for root, _, files in os.walk(input_folder):
        for file in tqdm(files):
            if file.endswith('.png'):
                img = remove_background(cv2.imread(os.path.join(root, file)))
                cv2.imwrite(os.path.join(output_folder, file), img)

if __name__ == '__main__':
    run('./dp0n', './dpon_processed')