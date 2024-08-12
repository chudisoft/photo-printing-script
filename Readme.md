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