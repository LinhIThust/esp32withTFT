import sys
import serial
from PIL import Image
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
def send_data_via_uart(data, port='/dev/ttyUSB0', baudrate=115200):
    # Open the serial port
    with serial.Serial(port, baudrate, timeout=1) as ser:
        # Send the image data over UART
        ser.write(data)

# Main function to resize, convert, and send the image
def main(image_path, uart_port='/dev/ttyUSB0', baudrate=115200):
    # Resize the image and convert to RGB565
    image_data = resize_and_convert_to_rgb565(image_path)

    # Send the image data via UART
    send_data_via_uart(image_data, port=uart_port, baudrate=baudrate)

if __name__ == "__main__":
    # Specify the path to the image
    image_path = "su_map.png"  # Replace with your image path
    
    # Specify the UART port (for Windows, use something like 'COM3')
    uart_port = 'COM4'  # Modify for your system
    baudrate = 921600

    # Run the main function
    main(image_path, uart_port, baudrate)
