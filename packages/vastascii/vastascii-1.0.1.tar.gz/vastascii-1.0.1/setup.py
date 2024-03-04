from setuptools import setup, find_packages

setup(
    name='vastascii',
    version='1.0.1',
    description='Convert images to ASCII art and display them in a Tkinter window or in the terminal',
    author='SiliconY',
    author_email='yangsilicon9@gmail.com',
    readme="README.md",
    packages=find_packages(),
    install_requires=['requests', 'Pillow'],
)
