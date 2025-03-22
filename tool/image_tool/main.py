import sys
import serial
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QImage, QBitmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw
import numpy as np

# Function to resize the image and convert it to RGB565
def resize_and_convert_to_rgb565(image_path, size=(240, 240)):
    # Open the image using Pillow
    img = Image.open(image_path)
    
    # Resize the image to 240x240
    img = img.resize(size)

    # Convert the image to RGB mode
    img_rgb = img.convert("RGB")

    # Convert the image pixels to RGB565 format
    width, height = img_rgb.size
    rgb565_data = []

    for y in range(height):
        for x in range(width):
            r, g, b = img_rgb.getpixel((x, y))

            # Convert RGB to RGB565
            rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)

            # Store the two bytes of the RGB565 data
            high_byte = (rgb565 >> 8) & 0xFF
            low_byte = rgb565 & 0xFF

            # Append the bytes to the data array
            rgb565_data.append(high_byte)
            rgb565_data.append(low_byte)

    # Convert the list to a byte array (uint8)
    return bytes(rgb565_data)

# Function to send data via UART
def send_data_via_uart(data, port, baudrate):
    # Open the serial port
    with serial.Serial(port, baudrate, timeout=1) as ser:
        # Send the image data over UART
        ser.write(data)
import serial
import time

def save_array(data,var_name="data", line_length=16):
    hex_values = [f'0x{b:02X}' for b in data]
    lines = [', '.join(hex_values[i:i+line_length]) for i in range(0, len(hex_values), line_length)]
    return f'unsigned char {var_name}[] = {{\n    ' + ',\n    '.join(lines) + '\n};\n\n' \
        f'unsigned int {var_name}_size = {len(data)};'

def send_data_divided(data, port, baudrate):
    chunk_size = len(data) // 1000

    with serial.Serial(port, baudrate, timeout=1) as ser:
        for i in range(1000):
            start = i * chunk_size
            end = start + chunk_size if i < 999 else len(data)
            chunk = data[start:end]

            ser.write(chunk)
            print(f"Sent chunk {i+1}")
            time.sleep(0.01)

# Function to create a circular mask on the image
def apply_circular_mask(image_path, size=(240, 240)):
    img = Image.open(image_path)
    img = img.resize(size)  # Resize to 240x240

    # Create a mask with a circle
    mask = Image.new('L', (size[0], size[1]), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    # Apply the circular mask to the image
    img.putalpha(mask)  # Apply the mask to the image

    return img

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the window
        self.setWindowTitle('ESP')
        self.setGeometry(100, 100, 300, 300)

        # Layout setup
        self.layout = QVBoxLayout()

        # Label to display the image
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        # Button to open file dialog
        self.btn_open = QPushButton('Choose Image', self)
        self.btn_open.clicked.connect(self.choose_image)
        self.layout.addWidget(self.btn_open)
        # Store image path
        self.image_path = None

        # Set the layout for the window
        self.setLayout(self.layout)

    def choose_image(self):
        # Open a file dialog to select an image
        image_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)')
        
        # If a file is chosen, display it
        if image_path:
            self.image_path = image_path
            self.display_image(image_path)

    def display_image(self, image_path):
        # Apply the circular mask to the image
        img = apply_circular_mask(image_path)
        
        # Convert the image to QPixmap for PyQt5
        img = img.convert("RGBA")
        data = img.tobytes("raw", "RGBA")
        qim = QImage(data, img.width, img.height, img.width * 4, QImage.Format_RGBA8888)

        # Convert to QPixmap
        pixmap = QPixmap.fromImage(qim)

        # Scale the pixmap if necessary
        pixmap = pixmap.scaled(self.image_label.size(), aspectRatioMode=1)  # Keep aspect ratio

        # Set the pixmap to the label
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)  # Align the image to the center
        time.sleep(2)
        self.send_image()

    def send_image(self):
        # Check if an image is loaded
        if self.image_path:
            # Resize the image and convert to RGB565
            image_data = resize_and_convert_to_rgb565(self.image_path)
            # save_array(image_data)
            with open("data.c", "w") as source_file:
                source_file.write(f'#include "data.h"\n\n')
                source_file.write(save_array(image_data, "imag.c"))
            # Send the image data via UART
            # send_data_via_uart(image_data,"COM4",921600)
            send_data_divided(image_data,"COM4",921600)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec_())
