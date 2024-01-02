
# Image Processing and OCR Scripts

This repository contains two Python scripts for processing images and extracting text from them using OCR (Optical Character Recognition).

## Prerequisites

- Python 3.x
- OpenCV (`cv2` module)
- NumPy
- PIL (Pillow)
- pytesseract
- xlsxwriter

Make sure you have the above Python modules installed. You can install them using pip:

```bash
pip install opencv-python numpy Pillow pytesseract xlsxwriter
```

You will also need to have [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system.

## Script Descriptions

### 1. Image Processing Script

`giftsUpdate2-1.py` - This script processes a set of images by cropping them to extract specific columns and concatenating them vertically.

#### Functionality

- **Crops** images to extract the "Player" and "Total" columns based on defined width and height ratios.
- **Saves** the cropped images.
- **Concatenates** the images vertically to create a single image per week for each project.

#### Usage

To run the script, navigate to the script's directory and execute:

```bash
python3 giftsUpdate2-1.py
```

This script processes images found in subdirectories structured as follows:

```
base_directory/
├─ Activity/
│  ├─ Week1/
│  ├─ Week2/
│  ├─ Week3/
│  ├─ Week4/
├─ Titanite/
│  ├─ Week1/
│  ├─ Week2/
│  ├─ Week3/
│  ├─ Week4/
```

### 2. OCR Script

`giftsUpdate2-2.py` - This script uses OCR to extract text from the images processed by the `giftsUpdate2-1.py` script and writes the data to an Excel file.

#### Functionality

- **Extracts text** from images using OCR.
- **Writes** the extracted data to an Excel workbook with a sheet for each week and project.

#### Usage

After processing the images with `process_images.py`, run the following command:

```bash
python3 giftsUpdate2-2.py
```

This script looks for the concatenated images produced by the first script in the same directory structure.

## Example Directory Structure

Ensure that your directory structure matches the expected format. For instance:

```
current_directory/
├─ giftsUpdate2-1.py
├─ giftsUpdate2-2.py
├─ Activity/
│  ├─ Week1/
│  ├─ Week2/
│  ├─ Week3/
│  ├─ Week4/
├─ Titanite/
│  ├─ Week1/
│  ├─ Week2/
│  ├─ Week3/
│  ├─ Week4/
```

## Notes

- The scripts should be located outside the `Activity` and `Titanite` directories, ideally in a parent directory.
- The scripts automatically process images in the `Activity` and `Titanite` directories and their corresponding `Week` subdirectories.
- The scripts use the current working directory as the base directory, meaning they should be run from the parent directory where `Activity` and `Titanite` reside.
