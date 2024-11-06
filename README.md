# Image Steganography Project

This project hides one image within another using least significant bit (LSB) encoding. The `encode` function conceals a smaller image inside a larger image, while the `decode` function extracts the hidden image. The goal is to create an encoded image that appears visually similar to the larger "host" image but contains all the data needed to retrieve the hidden "secret" image.

## Requirements

- **Python**: 3.x
- **Pillow (PIL)**: Python Imaging Library for handling image operations

## Usage

1. **Encoding**: The `encode()` function takes a large image to hide data within and a smaller image to hide. It returns an encoded image that visually resembles the larger image.

2. **Decoding**: The `decode()` function takes an encoded image (produced by `encode`) and retrieves the original hidden image.

### Code Structure

- **encode()**: Encodes the smaller image in the least significant bits of each pixel in the larger image.
- **decode()**: Decodes the smaller image from the encoded image by reading the least significant bits.
- **Image Size Requirement**: The dimensions of the hidden image must meet specific requirements relative to the host image.

## Image Size Requirement

To ensure successful encoding, the size of the hidden image should be approximately half the dimensions of the host image. This is because the host image uses 12 bits per pixel to store the 24-bit RGB values of each pixel in the hidden image. 

### Calculation for Requirement

The total pixels of the host image must satisfy:

\[
\text{Host Image Pixels} \times 12 \geq \text{Hidden Image Pixels} \times 24
\]

For example:
- If the host image has dimensions `1024 x 1024`, the hidden image should not exceed dimensions around `512 x 512`.

## Example

```python
# Paths to images
host_image_path = "path/to/host_image.png"
hidden_image_path = "path/to/hidden_image.png"

# Encode
encoded_image = encode(Image.open(host_image_path), Image.open(hidden_image_path))
encoded_image.save("encoded_output.png")

# Decode
decoded_image = decode(encoded_image)
decoded_image.save("decoded_output.png")
```
