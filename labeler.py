import os
from PIL import Image
import csv
import tkinter as tk
from tkinter import simpledialog

# Define the label options
label_options = {
    'A': 'Angry',
    'D': 'Disgust',
    'F': 'Fear',
    'H': 'Happy',
    'S': 'Sad',
    'U': 'Surprise',
    'N': 'Neutral',
    'R': 'Remove'
}

# Path to the image folder and the CSV file
img_folder_path = 'img'  # Folder where the images are stored
results_csv_path = 'labels.csv'  # CSV file to store the labels

# Function to display an image and get the user's label
def label_image(image_path):
    img = Image.open(image_path)
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate the position for the right side
    x_position = screen_width - img.width
    y_position = (screen_height - img.height) // 2
    
    # Set the position to the right side
    root.geometry(f'{img.width}x{img.height}+{x_position}+{y_position}')
    
    img.show()
    
    user_input = simpledialog.askstring("Input", f"Enter label for {os.path.basename(image_path)}:\n" +
                                            "\n".join([f"{k}={v}" for k, v in label_options.items()]))
    img.close()
    root.destroy()  # Close the window
    if user_input and user_input.upper() in label_options:
        return label_options[user_input.upper()]
    else:
        return 'Invalid'

# Main program function to process images and save labels
def label_images(start_at=1):
    image_files = [f for f in os.listdir(img_folder_path) if f.endswith('.png')]
    image_files.sort(key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else float('inf'))
    start_index = start_at - 1  # Convert to zero-based index
    for img_name in image_files[start_index:]:
        label = label_image(os.path.join(img_folder_path, img_name))
        if label != 'Invalid':
            # Remove the ".png" extension from the image name
            img_name_without_extension = os.path.splitext(img_name)[0]
            labeled_images = [(img_name_without_extension, label)]
            save_labels(labeled_images)

# Function to save labels to CSV
def save_labels(labeled_images):
    with open(results_csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(labeled_images)

if __name__ == "__main__":

    # Ask for the starting image number
    root = tk.Tk()
    root.withdraw()
    start_at = simpledialog.askinteger("Input", "Enter the starting image number (default is 1):", minvalue=1, initialvalue=1)
    root.destroy()

    # Run the labeling process starting at the given image number
    if start_at is not None:
        label_images(start_at)
    else:
        label_images()
