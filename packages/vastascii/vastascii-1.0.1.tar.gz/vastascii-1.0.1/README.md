# ASCII Art Library

The ASCII Art Library is a Python library that allows you to convert images to ASCII art and display them in a Tkinter window or in the terminal.

## Installation

You can install the library via pip:

```bash
pip install vastascii
```

## Usage

To use the library, simply import the `main` function and provide the URL of the image you want to convert to ASCII art. You can also specify the display type as either "tkinter" (to display in a Tkinter window) or "terminal" (to print in the terminal). If no display type is provided, it defaults to Tkinter window.

Example usage in a Python script:

```python
from vastascii import show_ascii

image_url = input("Enter the URL of the image: ")
display_type = input("Enter display type ('external' or 'internal'): ")
show_ascii(image_url, display_type)
```

## How it Works

1. The library downloads the image from the provided URL.
2. It converts the image to grayscale.
3. Based on the intensity of each pixel in the grayscale image, it assigns ASCII characters to represent different levels of intensity.
4. It displays the resulting ASCII art either in a Tkinter window or in the terminal.

Enjoy converting your images to ASCII art with ease!
