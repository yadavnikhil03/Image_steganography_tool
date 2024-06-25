# Image Steganography Tool

This Python-based GUI tool enables you to encode and decode secret messages within image files using LSB (Least Significant Bit) steganography.

## Features

- **Encoding:** Embeds text messages into selected image files using LSB steganography.
- **Decoding:** Retrieves hidden messages from encoded image files.
- **Capacity Calculation:** Automatically calculates the maximum number of characters that can be encoded into a chosen image.
- **User Interface:** Provides a simple and intuitive graphical interface for ease of use.

## Requirements

- Python 3.x
- tkinter (included in standard Python installation) 
- Pillow (PIL fork for handling images) `pip install Pillow`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/image-steganography-tool.git
   cd image-steganography-tool

# Usage
1. Encoding a Message:
- Launch the application by running  `python steganography.py`.
- Click on Encode Message.
- Select an image file (.png, .jpg, .jpeg) where you want to hide the message.
- Enter your secret message in the provided text box.
- Click Save to choose the location and filename for the encoded image or this may save in Download Folder by Default.

3. Decoding a Message:
- Launch the application by running `python steganography.py`.
- Click on Decode Message.
- Select the encoded image file (.png, .jpg, .jpeg) from which you want to extract the hidden message.
- The decoded message will be displayed in a message box.

# Acknowledgments
The tool utilizes the Pillow library for image processing.
Inspired by the concept of LSB steganography for hiding information within digital media.

