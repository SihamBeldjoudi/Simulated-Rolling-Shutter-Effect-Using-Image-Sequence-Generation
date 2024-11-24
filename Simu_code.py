import os
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Configuration

output_folder = "images_mouvement"  # Folder to store the generated images
num_images = 512                    # Number of images to generate
interval = 1                         # Interval of 1 second between each image
nbre_total_images = 512              # Total number of images generated
nbre_images_utilisees = 512           # Number of images to use in final composition (using all here)

# Create the output folder if it doesn't already exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Animation parameters (image size and movement)
image_size = (100, 100)               # Image size in pixels (100x100)
start_position = np.array([10, 50])   # Starting position of the object
end_position = np.array([90, 50])     # Final position of the object

# Calculate the movement step for each image (how much the object moves per image)
movement_step = (end_position - start_position) / num_images

# Generating the images
for i in range(num_images):
    # Calculate the current position of the object
    current_position = start_position + i * movement_step

    # Create the image
    fig, a = plt.subplots(figsize=(1, 1), dpi=image_size[0])  # Create a figure with the given DPI and size
    a.set_xlim(0, image_size[0])  # Set x-axis limits
    a.set_ylim(0, image_size[1])  # Set y-axis limits
    a.axis("off")  # Turn off the axis to only show the object

    # Draw the object (a circle in this case)
    circle = plt.Circle(current_position, 5, color='blue')  # Draw a blue circle at the current position
    a.add_patch(circle)  # Add the circle to the plot

    # Save the image
    image_path = os.path.join(output_folder, f"image_{i+1:03d}.png")  # Path to save the image
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0)  # Save the figure without extra padding
    plt.close(fig)  # Close the figure to free up memory

    # Wait for 1 second before capturing the next image
    time.sleep(interval)

# Print confirmation message after generating all images
print(f"All images have been saved in the '{output_folder}' folder.")

# Target size for images (to ensure uniform dimensions and avoid dimension errors)
target_size = (512, 512)

# Function to load and resize an image to a numpy array
def image_array(filepath):
    image = Image.open(filepath).convert("RGB")  # Open image and convert to RGB
    image = image.resize(target_size)            # Resize image to 512x512
    return np.array(image)                       # Return image as a numpy array

# List of image file paths
images = [f"{output_folder}/image_{i+1:03d}.png" for i in range(nbre_images_utilisees)]

# Empty matrix to hold the final composite image (512x512x3 for RGB channels)
Matrice_zeros = np.zeros((512, 512, 3), dtype=np.uint8)

# Calculations for compositing
N = 512                       # Total number of rows in the final image
per = 1                       # Number of periods (1 full cycle in this case)
n_lignes_periode = N / per    # Number of rows per period (512 in this case)
n_lignes_blocs = n_lignes_periode / nbre_images_utilisees  # Rows each image contributes

# Placing each image segment into the final matrix
for a in range(per):                 # Loop over each period
    for i in range(nbre_images_utilisees):   # Loop over each image
        # Load and resize the current image as a numpy array
        image_array_i = image_array(images[i])
        
        # Calculate the start and end indices for this image's segment in the final matrix
        debut = int(i * n_lignes_blocs + a * n_lignes_periode)   # Start index for this image segment
        fin = int((i + 1) * n_lignes_blocs + a * n_lignes_periode) # End index for this image segment
        
        # Copy the calculated rows from the current image into the final matrix
        Matrice_zeros[debut:fin, :] = image_array_i[debut:fin, :]

# Displaying information about the composition process
print('Number of images: ', nbre_images_utilisees)
print('Number of rows per block: ', n_lignes_blocs)
print('Number of periods: ', per)
print('Number of rows per period: ', n_lignes_periode)

# Display the final composite image matrix
plt.imshow(Matrice_zeros)
plt.axis('on')
plt.show()