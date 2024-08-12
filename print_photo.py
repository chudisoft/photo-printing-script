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
        return
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(save_folder, f"photo_{timestamp}.jpg")
    cv2.imwrite(filename, frame)
    print(f"Photo saved to {filename}")
    cap.release()
    cv2.destroyAllWindows()
    return filename

def create_printable_pdf(image_path, output_path, position):
    # Open the image
    img = Image.open(image_path)

    # Create a canvas
    c = canvas.Canvas(output_path, pagesize=A4)
    x, y = position

    # Get image dimensions
    img_width, img_height = img.size

    # Draw the image at the specified position
    c.drawImage(image_path, x, y, width=img_width, height=img_height)

    # Save the PDF
    c.showPage()
    c.save()
    print(f"Printable PDF saved to {output_path}")

def create_printable_pdfOld(image_path, output_path, position, orientation):
    img = Image.open(image_path)
    c = canvas.Canvas(output_path, pagesize=A4)
    if orientation == 'portrait':
        img_width, img_height = img.size
        a4_width, a4_height = A4
    else:
        img_width, img_height = img.size
        a4_height, a4_width = A4
    x, y = position
    c.drawImage(image_path, x, y, width=img_width, height=img_height)
    c.showPage()
    c.save()
    print(f"Printable PDF saved to {output_path}")

def print_pdf(pdf_path):
    subprocess.run(["lp", pdf_path])

# User-defined parameters
save_folder = input("Enter the folder path to save the photo: ")
# Define the position (x, y) in points (1 point = 1/72 inch)
# Adjust these values based on the template positioning
x = int(input("Enter the x position: ")) # inch from the left
y = int(input("Enter the y position: "))  # Start from y points above the bottom
position = (x, y)
# orientation = input("Enter the orientation ('portrait' or 'landscape'): ")
output_path = input("Enter the path for the output PDF: ")

# Workflow
photo_path = capture_photo(save_folder)
create_printable_pdf(photo_path, output_path, position)
# create_printable_pdf(photo_path, output_path, position, orientation)
print_pdf(output_path)
