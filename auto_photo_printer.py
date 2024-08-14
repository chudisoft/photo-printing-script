import os
import time
import shutil
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import subprocess

def create_printable_pdf(image_path, output_path, position, size):
    # Open the image
    img = Image.open(image_path)

    # Create a canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    x, y = position
    width, height = size

    # Draw the image at the specified position and size
    c.drawImage(image_path, x, y, width=width, height=height)

    # Save the PDF
    c.showPage()
    c.save()

def print_pdf(pdf_path):
    try:
        subprocess.run(["start", "/wait", pdf_path], shell=True)
    except Exception as e:
        print(f"Failed to print PDF: {e}")

def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def watch_folder(folder_path, position, size):
    print(f"Waiting for new images in {folder_path}...")
    print("Press Ctrl+C to exit.")
    existing_files = set(os.listdir(folder_path))

    while True:
        try:
            time.sleep(1)
            current_files = set(os.listdir(folder_path))
            new_files = current_files - existing_files

            for new_file in new_files:
                if new_file.lower().endswith('.jpg') or new_file.lower().endswith('.jpeg'):
                    file_path = os.path.join(folder_path, new_file)
                    print(f"Detected new file: {file_path}")

                    try:
                        output_pdf_path = os.path.join(os.getenv('TEMP'), "output.pdf")
                        create_printable_pdf(file_path, output_pdf_path, position, size)
                        print(f"Printable PDF created at {output_pdf_path}")
                        print_pdf(output_pdf_path)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

            existing_files = current_files

        except KeyboardInterrupt:
            print("Script terminated by user.")
            break

if __name__ == "__main__":
    # Set default paths and create the images directory if it doesn't exist
    script_dir = os.path.dirname(os.path.realpath(__file__))
    default_folder_path = os.path.join(script_dir, "images")
    ensure_dir_exists(default_folder_path)

    # User input for folder path, coordinates, and image size
    folder_path = input(f"Enter the folder path to watch for new images (default: {default_folder_path}): ") or default_folder_path
    x = int(input("Enter the x position (points) (default: 0): ") or 0)
    y = int(input("Enter the y position (points) (default: 0): ") or 0)
    width = int(input("Enter the width (points) (default: 200): ") or 200)
    height = int(input("Enter the height (points) (default: 200): ") or 200)

    position = (x, y)
    size = (width, height)

    watch_folder(folder_path, position, size)
