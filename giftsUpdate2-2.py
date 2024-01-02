import cv2
import os
import numpy as np
from PIL import Image
import pytesseract
import xlsxwriter
import re

def extract_text_line_by_line(image_path):
    # Load the image
    img = cv2.imread(image_path)
 
    # Specify OCR configurations for numeric and text extraction
    config_numeric = r'--psm 6 -c tessedit_char_whitelist=0123456789'
    config_text = r'--psm 4'

    # Calculate column widths based on the new proportions
    first_column_width = (2 * img.shape[1]) // 3  # 2/3 width for names
    last_column_width = img.shape[1] // 3  # 1/3 width for scores

    # Crop columns accordingly
    first_column_img = img[:, :first_column_width]
    last_column_img = img[:, -last_column_width:]

    # Extract text using OCR for each column with the appropriate configuration
    names_text = pytesseract.image_to_string(first_column_img, config=config_text)
    scores_text = pytesseract.image_to_string(last_column_img, config=config_numeric)

    return names_text.splitlines(), scores_text.splitlines()


def process_week_images(project, week, workbook):
    week_directory = os.path.join(base_directory, project, week)
    week_name = f"{project}_{week}"  # Unique name combining project and week
    image_file_name = f"{week}_concatenated_vertical.png"
    image_path = os.path.join(week_directory, image_file_name)
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return

    names, scores = extract_text_line_by_line(image_path)

    names = [item for item in names if item.strip() != ""]
    scores = [item for item in scores if item.strip() != ""]

    gifts_activity = set(zip(names, scores))
    sorted_gifts_activity = sorted(gifts_activity)

    worksheet = workbook.add_worksheet(week_name)

    for it, (key, value) in enumerate(sorted_gifts_activity):
        worksheet.write(it, 0, key)
        worksheet.write(it, 1, int(value))

base_directory = os.getcwd() 
projects = ['Activity', 'Titanite']
weeks = ['Week1', 'Week2', 'Week3', 'Week4']

excel_path = os.path.join(base_directory, 'gifts.xlsx')
workbook = xlsxwriter.Workbook(excel_path)


for project in projects:
    for week in weeks:
        process_week_images(project, week, workbook)

workbook.close()
print(f"Excel file created at {excel_path}")
