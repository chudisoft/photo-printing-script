import cv2
import os
import time
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import subprocess

def capture_photo(save_folder):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return None
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return None
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(save_folder, f"photo_{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Photo saved to {filename}")
    cap.release()
    cv2.destroyAllWindows()
    return filename

def create_printable_pdf(image_path, output_path, position, size):
    # Open the image
    img = Image.open(image_path)

    # Create a canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    x, y = position
    width, height = size

    # Draw the image at the specified position with the specified size
    c.drawImage(image_path, x, y, width=width, height=height)

    # Save the PDF
    c.showPage()
    c.save()
    print(f"Printable PDF saved to {output_path}")

def print_pdf(pdf_path):
    # Replace this with a method that works with your PDF reader
    try:
        subprocess.run(['cmd', '/c', pdf_path], shell=True)
        print(f"Printing {pdf_path}...")
    except Exception as e:
        print(f"Error printing PDF: {e}")

def get_validated_input(prompt, validation_fn, error_message):
    while True:
        try:
            value = validation_fn(input(prompt))
            return value
        except ValueError:
            print(error_message)

# Recurring operation until the user quits
while True:
    # User-defined parameters
    save_folder = get_validated_input(
        "Enter the folder path to save the photo: ",
        lambda x: x if os.path.isdir(x) else ValueError("Invalid path"),
        "Please enter a valid directory path."
    )

    x = get_validated_input(
        "Enter the x position (points): ",
        lambda x: int(x) if int(x) >= 0 else ValueError("Must be a non-negative integer"),
        "Please enter a non-negative integer for the x position."
    )

    y = get_validated_input(
        "Enter the y position (points): ",
        lambda y: int(y) if int(y) >= 0 else ValueError("Must be a non-negative integer"),
        "Please enter a non-negative integer for the y position."
    )

    width = get_validated_input(
        "Enter the width (points): ",
        lambda w: int(w) if int(w) > 0 else ValueError("Must be a positive integer"),
        "Please enter a positive integer for the width."
    )

    height = get_validated_input(
        "Enter the height (points): ",
        lambda h: int(h) if int(h) > 0 else ValueError("Must be a positive integer"),
        "Please enter a positive integer for the height."
    )

    output_file_name = get_validated_input(
        "Enter the file name for the output PDF (e.g., output.pdf): ",
        lambda x: x if x.endswith(".pdf") else ValueError("Must end with .pdf"),
        "Please enter a valid file name ending with .pdf."
    )

    output_path = os.path.join(save_folder, output_file_name)

    # Workflow
    photo_path = capture_photo(save_folder)
    if photo_path:
        create_printable_pdf(photo_path, output_path, (x, y), (width, height))
        print_pdf(output_path)

    # Check if the user wants to quit
    should_quit = input("Do you want to quit? Type 'yes' to quit, or press Enter to continue: ").strip().lower()
    if should_quit == 'yes':
        print("Exiting...")
        break
