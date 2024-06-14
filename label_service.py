from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code39
from reportlab.lib.units import inch
import os
import requests
import certifi
import urllib3
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Constants
FONT_SIZE = int(os.getenv("FONT_SIZE", 12))  # Font size for text
SUBSCRIPT_FONT_SIZE = int(FONT_SIZE * 0.75)  # Font size for subscripts
BORDER_HEIGHT = 300  # Height of the border rectangle
MARGIN = 50  # Margin around the border
BARCODE_SCALE = 1.5  # Scale factor for the barcode
BARCODE_WIDTH = 2 * inch * BARCODE_SCALE  # Scaled width of the barcode
BARCODE_HEIGHT = 0.75 * inch * BARCODE_SCALE  # Scaled height of the barcode
BARCODE_POSITION_ADJUST = 70  # Adjustment for the barcode position
IMAGE_SCALE = 0.5  # Scale factor for the image size
IMAGE_POSITION_ADJUST = 100  # Adjustment for the image position
NAME_BOX_WIDTH = 450  # Width of the name box
LOGO_Y_POSITION = 730  # Y position for the company logo

# Suppress only the single InsecureRequestWarning from urllib3 needed for testing purposes
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def wrap_text_manually(text, canvas, max_width):
    """
    Manually wrap text to fit within a specified width on the canvas.
    """
    def split_by_symbols(word):
        split_symbols = ['-', '_']
        for symbol in split_symbols:
            if symbol in word:
                parts = word.split(symbol)
                return [part + symbol for part in parts[:-1]] + [parts[-1]]
        return [word]

    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        split_words = split_by_symbols(word)
        for part in split_words:
            if canvas.stringWidth(current_line + part, "Helvetica", FONT_SIZE) < max_width:
                current_line += part
            else:
                lines.append(current_line)
                current_line = part
        current_line += " "

    if current_line:
        lines.append(current_line.strip())
    
    return lines

def draw_formula(c, formula, x, y):
    """
    Draws a chemical formula with subscripts on the canvas.
    """
    c.setFont("Helvetica", FONT_SIZE)
    x_offset = 0
    for char in formula:
        if char.isdigit():
            c.setFont("Helvetica", SUBSCRIPT_FONT_SIZE)
            c.drawString(x + x_offset, y - (FONT_SIZE * 0.25), char)
            x_offset += c.stringWidth(char, "Helvetica", SUBSCRIPT_FONT_SIZE)
            c.setFont("Helvetica", FONT_SIZE)
        else:
            c.drawString(x + x_offset, y, char)
            x_offset += c.stringWidth(char, "Helvetica", FONT_SIZE)

def create_label(info, output_path):
    page_size = A4  # Fixed to A4 size

    c = canvas.Canvas(output_path, pagesize=page_size)
    width, height = page_size

    # Set font size
    c.setFont("Helvetica", FONT_SIZE)

    # Add company logo to the top
    logo_path = os.path.join(os.path.dirname(__file__), "images", "Logo.png")
    if os.path.exists(logo_path):
        c.drawImage(logo_path, width - MARGIN - 110, LOGO_Y_POSITION, width=100, height=50)  # Adjust position and size as needed

    # Add text with wrapping
    y_position = height - MARGIN - 50
    max_text_width = width - 2 * MARGIN - 20

    fields = [
        ("Catalogue", info[0]),
        ("Name", info[1]),
        ("Formula", info[2]),
        ("Purity", info[3]),
        ("COO", info[4]),
        ("Company", info[5])
    ]

    for label, text in fields:
        if label == "Name":
            # Use manual text wrapping for the Name field
            c.setFont("Helvetica-Bold", FONT_SIZE)
            wrapped_text = wrap_text_manually(f"{text}", c, NAME_BOX_WIDTH)
        elif label == "Formula":
            c.setFont("Helvetica", FONT_SIZE)
            c.drawString(MARGIN + 10, y_position, f"{label}: ")
            draw_formula(c, text, MARGIN + 10 + c.stringWidth(f"{label}: "), y_position)
            y_position -= FONT_SIZE + 5  # Add margin after formula
            wrapped_text = []
        elif label == "Purity":
            # Convert purity to percentage if it's a decimal
            try:
                purity = float(text)
                if 0 <= purity <= 1:
                    text = f"{purity * 100:.0f}%"
                else:
                    text = f"{purity}%"
            except ValueError:
                pass
            wrapped_text = wrap_text_manually(f"{label}: {text}", c, max_text_width)
        else:
            c.setFont("Helvetica", FONT_SIZE)
            wrapped_text = wrap_text_manually(f"{label}: {text}", c, max_text_width)
        
        for line in wrapped_text:
            c.drawString(MARGIN + 10, y_position, line)
            y_position -= FONT_SIZE + 5
        y_position -= 5  # Add extra space between fields

    # Generate barcode
    barcode = code39.Standard39(str(info[0]), barHeight=BARCODE_HEIGHT, stop=1)
    barcode.drawOn(c, MARGIN + 10, y_position - BARCODE_POSITION_ADJUST)  # Adjust position as needed

    # Add logo from URL
    url = info[6]
    try:
        response = requests.get(url, verify=certifi.where())  # Use certifi for SSL verification
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.SSLError as e:
        print(f"SSL error: {e}")
        response = requests.get(url, verify=False)  # Disable SSL verification for testing purposes
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return  # Exit the function if the request failed

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img_path = "temp_image.png"
        img.save(img_path)
        img_width, img_height = img.size
        img_width *= IMAGE_SCALE
        img_height *= IMAGE_SCALE
        c.drawImage(img_path, width - MARGIN - img_width - 10, y_position - IMAGE_POSITION_ADJUST, width=img_width, height=img_height)  # Make picture bigger and adjust position
        os.remove(img_path)

    # Draw the border last, to ensure it's above all other layers
    c.setLineWidth(2)
    c.rect(MARGIN, height - BORDER_HEIGHT - MARGIN, width - 2 * MARGIN, BORDER_HEIGHT)

    c.save()

def generate_filename(label_id):
    cleaned_id = label_id.strip().replace(" ", "-")
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"label_{cleaned_id}_{date_str}.pdf"
