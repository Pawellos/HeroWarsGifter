import cv2
import os
import numpy as np 

# Function to crop the first column for player and the last column for total score.
def crop_columns_fractional(image_path):
    # Define the trim ratios (as a proportion of the image height/width)
    top_trim_ratio = 0.318    # Placeholder value for top trim
    bottom_trim_ratio = 0.19  # Placeholder value for bottom trim
    players_width_ratio = 0.2 # Placeholder value for the "Players" column width
    total_width_ratio = 0.1  # Placeholder value for the "Total" column width
    left_trim_ratio = 0.195      # Placeholder value for left trim
    right_trim_ratio = 0.07     # Placeholder value for right trim

    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"The image at {image_path} was not found.")
    
    # Calculate the trim sizes for height and width
    top_trim = int(img.shape[0] * top_trim_ratio)
    bottom_trim = img.shape[0] - int(img.shape[0] * bottom_trim_ratio)
    left_trim = int(img.shape[1] * left_trim_ratio)
    right_trim = img.shape[1] - int(img.shape[1] * right_trim_ratio)
    
    # Crop the image vertically and horizontally
    img_trimmed = img[top_trim:bottom_trim, left_trim:right_trim]
    
    # Estimate the width of the "Players" column
    players_column_width = int(img_trimmed.shape[1] * players_width_ratio)
    
    # Estimate the width of the "Total" column
    total_column_width = int(img_trimmed.shape[1] * total_width_ratio)
    
    # Crop the "Players" column from the left
    players_column_img = img_trimmed[:, :players_column_width]
    
    # Crop the "Total" column from the right
    total_column_img = img_trimmed[:, -total_column_width:]
    
    # Concatenate the "Players" and "Total" columns side by side
    concatenated_img = cv2.hconcat([players_column_img, total_column_img])
    
    return concatenated_img

def save_cropped_concatenated_images(images, base_name, folder):
    paths = []
    for i, img in enumerate(images):
        path = "{folder}/{base_name}_cropped_concatenated_{index}.png".format(
            folder=folder, base_name=base_name, index=i
        )
        cv2.imwrite(path, img)
        paths.append(path)
    return paths

def concatenate_images_vertically(image_paths):
    # Load all images and store their heights
    images = [cv2.imread(path) for path in image_paths if os.path.exists(path)]
    
    # Check if the images list is empty
    if not images:
        print(f"No images to concatenate for paths: {image_paths}")
        return None
    
    total_height = sum(image.shape[0] for image in images)
    
    # Find the max width to ensure all images can be concatenated vertically
    max_width = max(image.shape[1] for image in images)
    
    # Create a new image with total height and max width
    concatenated_image = np.zeros((total_height, max_width, 3), dtype=np.uint8)

    # Current y coordinate where the next image is to be placed
    current_y = 0
    for image in images:
        # Get the current image height
        height = image.shape[0]
        width = image.shape[1]
        
        # Place the image into the concatenated image
        concatenated_image[current_y:current_y+height, :width] = image
        current_y += height
    
    return concatenated_image

def process_images_in_directory(directory):
    image_paths = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.png', '.jpg', '.jpeg')) and not file.startswith('Week')]
    cropped_concatenated_images = [crop_columns_fractional(path) for path in image_paths]
    return cropped_concatenated_images

base_directory = os.getcwd() 
projects = ['Activity', 'Titanite']
weeks = ['Week1', 'Week2', 'Week3', 'Week4']

for project in projects:
    for week in weeks:
        week_directory = os.path.join(base_directory, project, week)
        cropped_concatenated_images = process_images_in_directory(week_directory)
        
        if not cropped_concatenated_images:
            print(f"No images processed in {week_directory}")
            continue

        image_folder = os.path.join(base_directory, project, week)
        cropped_concatenated_image_paths = save_cropped_concatenated_images(cropped_concatenated_images, week, image_folder)
        
        concatenated_vertical_image = concatenate_images_vertically(cropped_concatenated_image_paths)
        if concatenated_vertical_image is not None:
            final_concatenated_vertical_path = os.path.join(image_folder, f"{week}_concatenated_vertical.png")
            cv2.imwrite(final_concatenated_vertical_path, concatenated_vertical_image)
        else:
            print(f"Failed to create concatenated image for {week_directory}")