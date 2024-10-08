import os
import time
import tempfile
import uuid
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import subprocess
import platform
import win32print
import ghostscript
from datetime import datetime, timedelta

# Dictionary to store the last printed time of files
printed_files = {}

# Function to print PDF file
def print_pdf(pdf_path):
    try:
        if platform.system() == "Windows":
            # Setup the Ghostscript command arguments for printing
            args = [
                b"gs",  # Command for Ghostscript as bytes
                b"-dPrinted", b"-dBATCH", b"-dNOSAFER", b"-dNOPAUSE", b"-dNOPROMPT",
                b"-q",
                b"-sDEVICE=mswinpr2",  # Device for Windows Printer
                f'-sOutputFile=%printer%{win32print.GetDefaultPrinter()}'.encode(),  # Output to the default printer as bytes
                pdf_path.encode()  # Path to the PDF file as bytes
            ]

            # Run Ghostscript command
            ghostscript.Ghostscript(*args)
        else:
            raise NotImplementedError("This script is intended for Windows OS.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to print PDF: {e}")

# Function to convert image to PDF and save it
def convert_image_to_pdf(image_path, x, y, width, height):
    try:
        # Ensure the file exists before proceeding
        if not os.path.exists(image_path):
            print(f"File does not exist: {image_path}")
            return

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Generate a unique filename for the output PDF
            output_filename = f"{uuid.uuid4()}.pdf"
            output_path = os.path.join(tmpdirname, output_filename)

            # Create the PDF
            c = canvas.Canvas(output_path, pagesize=A4)
            c.drawImage(image_path, x, y, width, height)
            c.save()

            print(f"Printable PDF created at {output_path}")

            # Attempt to print the PDF
            print_pdf(output_path)
    except Exception as e:
        print(f"Error processing file {image_path}: {e}")

# Event handler for file events
class FileHandler(FileSystemEventHandler):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # def on_created(self, event):
    #     self.process(event)

    def on_modified(self, event):
        self.process(event)

    # def on_moved(self, event):
    #     # The file was renamed (e.g., .tmp to .jpg)
    #     self.process(event)

    def process(self, event):
        if event.is_directory:
            return

        file_path = event.src_path.lower()
        time.sleep(1)
        if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
            print(f"Detected new or modified file: {file_path}")

            print(printed_files)
            # Check if the file was printed in the last 10 seconds
            if file_path in printed_files:
                last_print_time = printed_files[file_path]
                if datetime.now() - last_print_time < timedelta(seconds=10):
                    print(f"File {file_path} was printed less than 10 seconds ago. Skipping...")
                    return
            
            # Update the last printed time
            printed_files[file_path] = datetime.now()

            # Convert the image to PDF and print it
            convert_image_to_pdf(file_path, self.x, self.y, self.width, self.height)

# Function to ensure the image directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    # Default image directory
    # Load configuration from JSON file

    script_dir = os.path.dirname(os.path.abspath(__file__))
    # default_image_dir = os.path.join(script_dir, 'images')
    config_path = os.path.join(script_dir, 'config.json')

    with open(config_path, 'r') as f:
        config = json.load(f)

    folder_path = config.get("folder_path")
    x = config.get("x", 0)
    y = config.get("y", 0)
    width = config.get("width", 200)
    height = config.get("height", 200)

    ensure_directory_exists(folder_path)

    # Get user inputs
    # folder_path = input(f"Enter the folder path to watch for new images (default: {default_image_dir}): ") or default_image_dir
    # x = int(input("Enter the x position (points): ") or 0)
    # y = int(input("Enter the y position (points): ") or 0)
    # width = int(input("Enter the width (points): ") or 200)
    # height = int(input("Enter the height (points): ") or 200)

    # Create event handler
    event_handler = FileHandler(x, y, width, height)

    # Set up observer
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=False)

    # Start observing
    observer.start()
    try:
        print("Script is now waiting for new images to be added to the folder.")
        print("Press Ctrl+C to stop the script.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
