# Photo Printing Script

This project provides a Python script that captures a photo from a camera, saves it, and prints the image in a specified position on an A4 paper. This is particularly useful for printing photos on pre-printed templates, such as newspaper-style layouts.

## Features

- Capture a photo using a webcam.
- Save the captured photo to a specified folder.
- Print the photo in a user-defined position on an A4 paper.
- Configurable printing position and orientation.

## Requirements

- Python 3.x
- OpenCV
- Pillow
- ReportLab

## Installation

1. Clone the repository:

```
    git clone https://github.com/chudisoft/photo-printing-script.git
    cd photo-printing-script
```

2. Create a virtual environment for Python packages:

```
    python -m venv venv
```
 or
```
    python3 -m venv venv
```

3. Activate the Virtual Environment:

    **For macOS/Linux:**
```
    source venv/bin/activate
```

**For Windows:**
```
    .\venv\Scripts\activate
```

4. Install the required Python packages:

```
    pip install -r requirements.txt
```

## Usage

1. **Capture and Save Photo:**

    The script captures a photo from the webcam and saves it to a specified folder.

```
    save_folder = "path_to_your_folder"
    photo_path = capture_photo(save_folder)
```

2. **Print Photo on Pre-Printed Template:**

    Define the position on the A4 paper where the photo should be printed.

```
    position = (x, y)  # Replace with actual coordinates in points
    orientation = 'portrait'  # or 'landscape'
    output_path = "output.pdf"

    create_printable_pdf(photo_path, output_path, position, orientation)
```

3. **Print the PDF:**

    Use the `lp` command (on Linux) to send the PDF to the printer.

```
    print_pdf(output_path)
```

## Example

To run the script with a specific folder and position:

```
    python print_photo.py
```

# PDF Coordinate System for Image Placement

In a PDF file, the coordinate system starts from the bottom-left corner, meaning:

- **X position** is measured from the left edge of the page.
- **Y position** is measured from the bottom edge of the page.

### A4 Page Dimensions

- **Width:** 595 points
- **Height:** 842 points

### Positioning the Image

To place the image at the very top of the page, set the `y` value close to 842 points, minus the height of the image. 

**Calculation for Y Value:**

If you want the top edge of the image to start exactly at the top of the page, you can calculate the `y` value as follows:

```
    y = 842 - image_height
```

This ensures that the top edge of the image aligns with the top edge of the page.

### Example:

If your image height is 200 points, then:

```
    y = 842 - 200 = 642
```

So, setting y = 642 will place the image such that its top edge aligns with the top of the page.

### Adjusting for Margins

If you want to add a margin from the top, reduce the y value slightly. For example, to add a 10-point margin:

```
    y = 842 - 200 - 10 = 632
```

### Recap

- y = 0: Image bottom edge aligns with the bottom of the page.
- y = 842: Image bottom edge aligns with the top of the page (image is off-page).
- y = 842 - image_height: Image top edge aligns with the top of the page.

Set your y value accordingly based on the image size and desired position.
