import os
import time
import tempfile
import uuid
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import subprocess
import platform
import win32print
import locale
import ghostscript


# Function to print PDF file
def print_pdf(pdf_path):
    try:
        if platform.system() == "Windows":
            # Windows uses the `start` command to print
            # subprocess.run(["start", "/p", pdf_path], shell=True, check=True)
            args = [
                "-dPrinted", "-dBATCH", "-dNOSAFER", "-dNOPAUSE", "-dNOPROMPT"
                "-q",
                "-dNumCopies#1",
                "-sDEVICE#mswinpr2",
                f'-sOutputFile#"%printer%{win32print.GetDefaultPrinter()}"',
                f'"{pdf_path}"'
            ]

            encoding = locale.getpreferredencoding()
            args = [a.encode(encoding) for a in args]
            ghostscript.Ghostscript(*args)
        else:
            raise NotImplementedError("This script is intended for Windows OS.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to print PDF: {e}")

# Function to convert image to PDF and save it
def convert_image_to_pdf(image_path, x, y, width, height):
    try:
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

# Event handler for new files
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def on_created(self, event):
        if event.src_path.lower().endswith('.jpg') or event.src_path.lower().endswith('.jpeg'):
            print(f"Detected new file: {event.src_path}")
            convert_image_to_pdf(event.src_path, self.x, self.y, self.width, self.height)

# Function to ensure the image directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    # Default image directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_image_dir = os.path.join(script_dir, 'images')
    ensure_directory_exists(default_image_dir)

    # Get user inputs
    folder_path = input(f"Enter the folder path to watch for new images (default: {default_image_dir}): ") or default_image_dir
    x = int(input("Enter the x position (points): ") or 0)
    y = int(input("Enter the y position (points): ") or 0)
    width = int(input("Enter the width (points): ") or 200)
    height = int(input("Enter the height (points): ") or 200)

    # Create event handler
    event_handler = NewFileHandler(x, y, width, height)

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
