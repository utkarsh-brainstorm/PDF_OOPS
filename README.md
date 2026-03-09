**🚨 NOTE: Generative AI is used in this project. Heisenberg only planned it and verified the functions, but the most code is written by AI. 🚨**

# PDF_OOPS

PDF_OOPS is a tool to combine images into PDFs and make large PDFs smaller in file size.

## Quick Start

To use this tool without setting up Python:
1. Go to the [Releases](../../releases) page.
2. Download the version for your computer.
3. Run the downloaded file.

## Features & Instructions

Run the tool and follow the on-screen prompts. You will be asked to drag and drop your image folder or PDF file.

### 1. Make PDF from Images
Combines a folder of images into one PDF.
* **Relative Size:** Keeps the original size of each image. Type `0`.
* **Continuous Width:** Makes all images the exact same width. Type `1`.
* **Quality:** Choose a number from 0 to 100 to set image quality (100 is best).

### 2. Compress PDF
Makes large PDF files smaller.
* **Basic Compression:** Squishes the whole PDF to make the file size smaller.
* **Smart Text Compression:** Makes images smaller but keeps text sharp and selectable. Choose Light (1), Medium (2), or Heavy (3) compression.

## Running from Source (For Developers)

If you want to run the code yourself using Python:

1. Make sure Python 3.8+ is installed.
2. Open your terminal in the project folder.
3. (Optional) Create a virtual environment: `python -m venv venv` and activate it.
4. Install requirements: `pip install img2pdf PyPDF2 Pillow PyMuPDF pdf2image`
*Note: You may need to install `poppler` on your system for `pdf2image` to work fully.*
5. Run the tool: `python PDF_OOPS.py`

## Future Updates

We will soon release ready-to-use executable files for Windows and macOS, so you can just double-click and use it without any terminal.
