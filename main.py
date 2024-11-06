from PIL import Image

def add_leading_zeros(binary_number, expected_length):
    """Pads a binary string with leading zeros to reach the expected length."""
    return binary_number.zfill(expected_length)

def rgb_to_binary(r, g, b):
    """Converts RGB values to 8-bit binary strings."""
    return (add_leading_zeros(bin(r)[2:], 8),
            add_leading_zeros(bin(g)[2:], 8),
            add_leading_zeros(bin(b)[2:], 8))

def get_binary_pixel_values(img):
    """Converts all pixels of an image to a single binary string."""
    width, height = img.size
    binary_pixels = ''
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
            binary_pixels += r_binary + g_binary + b_binary
    return binary_pixels

def change_binary_values(img_visible, hidden_pixels, width_hidden, height_hidden):
    """Encodes binary data of the hidden image into the least significant bits of the visible image."""
    img_visible_copy = img_visible.copy()
    width_visible, height_visible = img_visible.size
    idx = 0

    for x in range(width_visible):
        for y in range(height_visible):
            if x == 0 and y == 0:
                # Store hidden image dimensions in the first pixel
                dimensions_binary = add_leading_zeros(bin(width_hidden)[2:], 12) + add_leading_zeros(bin(height_hidden)[2:], 12)
                img_visible_copy.putpixel((x, y), (
                    int(dimensions_binary[0:8], 2),
                    int(dimensions_binary[8:16], 2),
                    int(dimensions_binary[16:24], 2)
                ))
                continue
            
            r, g, b = img_visible.getpixel((x, y))
            r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
            
            if idx + 12 <= len(hidden_pixels):
                r_binary = r_binary[:4] + hidden_pixels[idx:idx+4]
                g_binary = g_binary[:4] + hidden_pixels[idx+4:idx+8]
                b_binary = b_binary[:4] + hidden_pixels[idx+8:idx+12]
                idx += 12

                img_visible_copy.putpixel((x, y), (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2)))
                if idx >= len(hidden_pixels):
                    return img_visible_copy
    return img_visible_copy

def extract_hidden_pixels(img_visible, pixel_count):
    """Extracts binary data hidden in the least significant bits of pixels."""
    width_visible, height_visible = img_visible.size
    hidden_pixels = ''
    idx = 0

    for x in range(width_visible):
        for y in range(height_visible):
            if x == 0 and y == 0:
                continue

            r, g, b = img_visible.getpixel((x, y))
            r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
            hidden_pixels += r_binary[4:] + g_binary[4:] + b_binary[4:]
            
            if idx >= pixel_count * 24:
                return hidden_pixels[:pixel_count * 24]
            idx += 1
    return hidden_pixels

def reconstruct_image(binary_pixels, width, height):
    """Creates an image from binary pixel data."""
    image = Image.new("RGB", (width, height))
    idx = 0
    for x in range(width):
        for y in range(height):
            r = int(binary_pixels[idx:idx+8], 2)
            g = int(binary_pixels[idx+8:idx+16], 2)
            b = int(binary_pixels[idx+16:idx+24], 2)
            image.putpixel((x, y), (r, g, b))
            idx += 24
    return image

def encode_and_decode():
    """Encodes one image into another, saves it, then decodes it back and saves the hidden image."""
    # Paths for input and output images
    img_visible_path = "./images/chicken.jpg"  # مسیر تصویر مرئی
    img_hidden_path = "./images/art.jpg"    # مسیر تصویر مخفی
    encoded_output_path = "encoded_image.png"  # مسیر خروجی تصویر کدگذاری شده
    decoded_output_path = "decoded_image.png"  # مسیر خروجی تصویر بازیابی شده

    # Load images
    img_visible = Image.open(img_visible_path)
    img_hidden = Image.open(img_hidden_path)
    
    # Encode the hidden image into the visible image
    hidden_pixels = get_binary_pixel_values(img_hidden)
    width_hidden, height_hidden = img_hidden.size
    encoded_image = change_binary_values(img_visible, hidden_pixels, width_hidden, height_hidden)
    encoded_image.save(encoded_output_path)
    print(f"Encoded image saved to {encoded_output_path}")

    # Decode the hidden image from the encoded image
    encoded_image = Image.open(encoded_output_path)
    r, g, b = encoded_image.getpixel((0, 0))
    r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
    dimensions_binary = r_binary + g_binary + b_binary

    width_hidden = int(dimensions_binary[:12], 2)
    height_hidden = int(dimensions_binary[12:], 2)
    pixel_count = width_hidden * height_hidden

    hidden_pixels = extract_hidden_pixels(encoded_image, pixel_count)
    decoded_image = reconstruct_image(hidden_pixels, width_hidden, height_hidden)
    decoded_image.save(decoded_output_path)
    print(f"Decoded image saved to {decoded_output_path}")

# Run the combined encode and decode process
encode_and_decode()
requirements =