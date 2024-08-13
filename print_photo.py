import cv2
import os
import time
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import random
import string
import platform

def capture_photo(save_folder, filename):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    filepath = os.path.join(save_folder, filename)
    cv2.imwrite(filepath, frame)
    print(f"Photo saved to {filepath}")
    cap.release()
    cv2.destroyAllWindows()
    return filepath

def create_printable_pdf(image_path, output_path, position, size):
    img = Image.open(image_path)
    c = canvas.Canvas(output_path, pagesize=A4)
    x, y = position
    width, height = size
    c.drawImage(image_path, x, y, width=width, height=height)
    c.showPage()
    c.save()
    print(f"Printable PDF saved to {output_path}")

def print_pdf(pdf_path):
    try:
        if platform.system() == "Windows":
            os.startfile(pdf_path, "print")
        elif platform.system() == "Linux":
            subprocess.run(["lp", pdf_path])
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["lp", pdf_path])
        else:
            print("Printing is not supported on this OS.")
    except Exception as e:
        print(f"Failed to print PDF: {e}")

def get_random_filename(extension=".jpg"):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"photo_{timestamp}_{random_str}{extension}"

def get_user_input(prompt, default_value):
    user_input = input(f"{prompt} (default: {default_value}): ")
    return user_input.strip() if user_input else default_value

# Default values
default_folder = os.getcwd()
default_filename = get_random_filename()

while True:
    save_folder = get_user_input("Enter the folder path to save the photo", default_folder)
    filename = get_user_input("Enter the photo filename", default_filename)
    output_filename = get_user_input("Enter the file name for the output PDF (e.g., output.pdf)", "output.pdf")

    x = int(get_user_input("Enter the x position (points)", "0"))
    y = int(get_user_input("Enter the y position (points)", "0"))
    width = int(get_user_input("Enter the width (points)", "200"))
    height = int(get_user_input("Enter the height (points)", "200"))

    position = (x, y)
    size = (width, height)

    photo_path = capture_photo(save_folder, filename)
    output_path = os.path.join(save_folder, output_filename)
    create_printable_pdf(photo_path, output_path, position, size)
    print_pdf(output_path)

    cont = input("Do you want to take another photo and print? (y/n): ").strip().lower()
    if cont != 'y':
        break
