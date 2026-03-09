# PDF Beast & IMG2PDF Nerd Edition 🦖🔥

Welcome to **PDF_OOPS**—the absolute ultimate CLI toolkit for dominating your documents! Whether you have a chaotic folder of images that you need to birth into a majestic PDF, or a bloated PDF that needs to be crunched down to size, this tool has you covered.

## 🚀 Quick Start (No Setup Required!)

If you just want to use the toolkit **without** the hassle of setting up Python, installing libraries, or configuring heavy environments:

👉 **[Go to the Releases page](../../releases)** and download the standalone executable for your operating system. Simply download, run, and you are ready to conquer PDFs natively!

---

## ✨ Features & How They Work

PDF_OOPS provides an incredibly interactive and fun Command Line Interface (CLI). Just run the script and let it roast your bad inputs while expertly handling your daily document chores.

### 1. 📸 IMG2PDF: Nerd Edition v6.9 (Image to PDF)
*   **Compile a Folder of Images:** Takes an entire folder of random images (`.jpg`, `.png`, `.webp`, etc.) and intelligently binds them into a single perfect PDF scroll.
*   **Smart Auto-Orientation:** Ensures your images are correctly oriented.
*   **Dynamic Custom Size:** Select the scale of the resulting PDF! You can choose `Relative Size Mode` to preserve precise original formats or `Continuous Width Mode` to unify an entire batch of mismatched images to the exact same width! 
*   **Erotic Quality Control:** Define the output JPEG quality on a scale from 0 to 100 to strike the finest balance.

### 2. 🗜️ PDF Beast (The Ultimate PDF Slayer Mode)
*   **Heavy Compression:** Have an insanely massive, image-heavy PDF? Drop it here. Determine your target pixel width and quality percentage, and watch it smartly squish your document down to a budget size!
*   **Smart Text Preserving Compression:** Got a text-heavy PDF but with bloated graphs/images? Oh yes! Use the Smart Option (Light, Medium, or Heavy compression). It specifically scans your PDF page-by-page, *only compresses the images it finds*, and entirely preserves your native, selectable, searchable text! 

### 🎮 How to Interact with the CLI
1. The script contains all functionality bundled together. Depending on the function you intend to call within the Python script (e.g., `convert_images_to_pdf()` or `compress_pdf_text()`), simply execute it.
2. The interactive prompt will ask you to **Paste the full path to your image folder or PDF**. Drag and drop works perfectly!
3. Answer the highly engaging terminal prompts as requested (e.g., entering numerical values for quality settings, `0 or 1` for scale modes, or `y/n` for squishing the file).
4. Sit back as loading bars light up your console. The new files will be cleanly placed with `_compressed` or `_compressed_text` suffixes right next to your originals!

---

## 🐍 For Developers: Running from Python Source

If you prefer to run the scripts directly via Python, follow these steps to set up the environment.

### 1. Requirements & OS Dependencies
Make sure you have **Python 3.8+** installed on your system.
This script relies on heavily battle-tested formatting and parsing libraries designed for macOS, Linux, and Windows.

### 2. Setup the Environment
Open your terminal and create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required Python dependencies:
```bash
pip install img2pdf PyPDF2 Pillow PyMuPDF pdf2image
```
*Note for `pdf2image`: You might need `poppler` installed on your OS.*
*   Ubuntu/Debian: `sudo apt-get install poppler-utils`
*   macOS: `brew install poppler`
*   Windows: Download Poppler for Windows and add it to your PATH.

### 3. Run the Script
Now you can execute the Python script directly:
```bash
python PDF_OOPS.py
```

---

## 🔮 Future Roadmap

We are constantly aiming for effortless usability! Keep an eye out—**after some time, we will be releasing official PyInstaller One-File executables for Windows and macOS!** 

This will mean true click-and-run, dependency-free processing power across all major platforms. Directly download the `.exe` or Mac application and slay your PDFs instantly!
