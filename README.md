**🚨 NOTE: Generative AI is used in this project. Heisenberg only planned it and verified the functions, but the most code is written by AI. 🚨**

# PDF_OOPS

PDF_OOPS is a tool to combine images into PDFs and make large PDFs smaller in file size.

## Quick Start

To use this tool without setting up Python:
1. Go to the [Releases](../../releases) page.
2. Download the `PDF_OOPS` Linux executable file.
3. Open your terminal, make it executable (`chmod +x PDF_OOPS`), and run it (`./PDF_OOPS`).

## Features & Instructions

Run the tool and it will ask you to drop your folder or file. It has two main tools inside based on what you run:

### 1. Make PDF from Images (IMG2PDF Mode)
Combines a whole folder of images into one PDF. Drop your folder and it will ask you:
* **Quality Setting:** Type a number from 0 to 100 to set how good the images look (100 is best, but biggest file size).
* **Relative Size (Type `0`):** Keeps every image exactly its original size.
* **Continuous Width (Type `1`):** Makes all images exactly the same width. If you choose this, it will ask you to type the exact width you want in pixels.
* **Compress PDF:** After making the PDF, it will ask if you want to squish it to make it even smaller. Type `y` for yes or `n` for no.

### 2. Compress Existing PDF (PDF Beast Mode)
Makes large PDF files smaller. Drop your PDF file and it will do its magic:
* **Basic Compression:** It will ask you for a width in pixels and a quality number (1-100) to squish the whole PDF down.
* **Smart Text Compression:** Makes heavy images smaller but keeps all your text completely untouched and copyable. You just type `1` for Light compression, `2` for Medium, or `3` for Heavy compression.

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
