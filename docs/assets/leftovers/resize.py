from PIL import Image
import os

def shrink_pngs_and_save(directory, output_directory, shrink_factor):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            input_filepath = os.path.join(directory, filename)
            output_filepath = os.path.join(output_directory, filename)  # Save in the current directory
            with Image.open(input_filepath) as img:
                new_size = (int(img.width / shrink_factor), int(img.height / shrink_factor))
                resized_img = img.resize(new_size)
                resized_img.save(output_filepath)

# Usage example
input_directory_path = './full-size'  # Path to the 'full-size' folder
output_directory_path = '.'  # Current directory
shrink_factor = 4  # Replace with your desired shrink factor
shrink_pngs_and_save(input_directory_path, output_directory_path, shrink_factor)

