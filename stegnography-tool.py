import os
from tkinter import Tk, Frame, Label, Text, Button, filedialog, messagebox
from PIL import Image

def calculate_max_characters(image_path):
    """
    Calculate the maximum number of characters that can be encoded in the image.
    
    Args:
        image_path (str): Path to the input image.
        
    Returns:
        int: Maximum number of characters.
        
    Raises:
        FileNotFoundError: If the input image file does not exist.
    """
    try:
        img = Image.open(image_path).convert('RGBA')  # Ensure image is in RGBA mode
    except FileNotFoundError:
        raise FileNotFoundError("Input image file not found.")
    
    width, height = img.size
    
    # Calculate the maximum number of bits available for encoding
    max_bits = width * height * 3
    
    # Each character is represented by 8 bits (ASCII encoding)
    max_characters = max_bits // 8
    
    return max_characters

def encode_message_in_image():
    """
    Encode a message into an image using LSB steganography.
    """
    input_image_path = filedialog.askopenfilename(title="Select Input Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not input_image_path:
        return
    
    max_characters = calculate_max_characters(input_image_path)
    
    message = entry_message.get("1.0", "end-1c")
    if len(message) > max_characters:
        messagebox.showerror("Error", f"The message exceeds the maximum number of characters ({max_characters}).")
        return
    
    # Default directory for saving encoded images
    default_directory = os.path.join(os.path.expanduser('~'), 'Downloads')
    output_image_path = filedialog.asksaveasfilename(title="Save Encoded Image", defaultextension=".png", initialdir=default_directory, filetypes=[("PNG Files", "*.png")])
    if not output_image_path:
        return
    
    try:
        encode_message_in_image_helper(input_image_path, message, output_image_path)
        messagebox.showinfo("Success", "Message encoded and saved.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def encode_message_in_image_helper(image_path, message, output_path):
    """
    Helper function to encode a message into an image using LSB steganography.
    
    Args:
        image_path (str): Path to the input image.
        message (str): Message to be encoded into the image.
        output_path (str): Path for the encoded image to be saved.
        
    Raises:
        FileNotFoundError: If the input image file does not exist.
    """
    img = Image.open(image_path).convert('RGBA')  # Ensure image is in RGBA mode
    encoded_img = img.copy()
    width, height = img.size
    index = 0
    
    # Convert message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '0000000000000000'  # Delimiter to mark end of message
    
    for row in range(height):
        for col in range(width):
            if index < len(binary_message):
                pixel = list(img.getpixel((col, row)))
                for n in range(3):  # Iterate over RGB channels (excluding alpha)
                    if index < len(binary_message):
                        pixel[n] = pixel[n] & ~1 | int(binary_message[index])
                        index += 1
                encoded_img.putpixel((col, row), tuple(pixel))
            else:
                break
    
    encoded_img.save(output_path)

def decode_message_from_image():
    """
    Decode a message from an image using LSB steganography.
    """
    input_image_path = filedialog.askopenfilename(title="Select Encoded Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not input_image_path:
        return
    
    try:
        decoded_message = decode_message_from_image_helper(input_image_path)
        if decoded_message:
            messagebox.showinfo("Decoded Message", decoded_message)
        else:
            messagebox.showwarning("No Message Found", "No hidden message found in the image.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def decode_message_from_image_helper(image_path):
    """
    Helper function to decode a message from an image using LSB steganography.
    
    Args:
        image_path (str): Path to the encoded image.
        
    Returns:
        str: Decoded message from the image.
        
    Raises:
        FileNotFoundError: If the encoded image file does not exist.
    """
    img = Image.open(image_path).convert('RGBA')  # Ensure image is in RGBA mode
    width, height = img.size
    binary_message = ""
    
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for n in range(3):  # Iterate over RGB channels (excluding alpha)
                binary_message += str(pixel[n] & 1)
                
    # Convert binary message to string
    bytes_list = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ""
    for byte in bytes_list:
        if byte == '00000000':  # Delimiter to mark end of message
            break
        message += chr(int(byte, 2))
    
    return message

def create_gui():
    """
    Create the graphical user interface.
    """
    root = Tk()
    root.title("Steganography Tool")
    root.geometry("400x300")
    root.configure(bg="#1E1E1E")
    
    frame_encode = Frame(root, bg="#1E1E1E")
    frame_encode.pack(pady=10)
    
    label_message = Label(frame_encode, text="Enter Message:", fg="#FFD700", bg="#1E1E1E", font=("Arial", 12, "bold"))
    label_message.grid(row=0, column=0, padx=5, pady=5)
    global entry_message
    entry_message = Text(frame_encode, height=5, width=30, bg="#2E2E2E", fg="#FFFFFF", font=("Arial", 10))
    entry_message.grid(row=0, column=1, padx=5, pady=5)
    
    button_encode = Button(root, text="Encode Message", command=encode_message_in_image, bg="#FFD700", fg="#1E1E1E", font=("Arial", 12, "bold"), relief="flat")
    button_encode.pack(pady=5)
    
    button_decode = Button(root, text="Decode Message", command=decode_message_from_image, bg="#FFD700", fg="#1E1E1E", font=("Arial", 12, "bold"), relief="flat")
    button_decode.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

