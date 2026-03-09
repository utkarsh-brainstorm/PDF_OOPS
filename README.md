**🚨 NOTE: Generative AI is used in this project. Heisenberg only planned it and verified the functions, but the most code is written by AI. 🚨**

# PDF_OOPS & IMG2PDF 🦖🔥

**PDF_OOPS** is a god-tier, interactive, multi-functional Command Line Toolkit designed to dominate your PDFs. It houses two massively powerful subsystems: **IMG2PDF** (an ultra-customizable image-to-PDF binder) and **PDF PREDATOR** (the ultimate arsenal to compress, extract, merge, and split existing PDFs). 

Forget writing shell commands; just run the tool, drop your files, and interact with the highly engaging terminal prompts!

---

## 🚀 Quick Start (No Setup Required!)

If you do not want to install Python or set up developer environments, you can use the standalone executable:

1. Go to the **[Releases](../../releases)** page of this repository.
2. Download the `PDF_OOPS` executable file for your operating system (currently available for Linux).
3. If on Linux/macOS, open your terminal, navigate to your download folder, and make it executable: `chmod +x PDF_OOPS`
4. Run the file: `./PDF_OOPS`
5. Drag and drop your folders or files into the terminal window when prompted!

---

## ✨ The Complete Toolkit Feature Guide

When you launch the application, you are presented with the **MAIN MASTER MENU**. You must choose between the two major toolkits:

---

### 📸 TOOLKIT 1: IMG2PDF (Images to PDF Converter)
This tool takes an entire messy folder of images and intelligently binds them into a single, majestic PDF scroll. 

1. **Auto-Discovery & Sorting:** Provide a folder path. The script recursively finds all valid image types (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`), ignores junk files, and sorts them alphanumerically.
2. **Erotic Quality Control:** You define the output JPEG compression quality on a scale of `0–100`.
3. **Advanced Layout Styling:**
   *   **Relative Size Mode (Type `0`):** Embeds every image exactly according to its native pixel dimensions.
   *   **Continuous Width Mode (Type `1`):** Ideal for standardizing chaotic scans. The system detects the widest image in your folder. You can accept this maximum width, or type a custom pixel width. It mathematically applies a high-quality LANCZOS resampling to every single image, perfectly adjusting their heights to preserve aspect ratios, ensuring your final PDF is uniformly wide from top to bottom.
4. **Post-Processing Compression:** After binding, you are given the choice to "squish" the final PDF. It utilizes PyPDF2 to strip out unneeded metadata and optimize data streams for a smaller footprint.

---

### 🔥 TOOLKIT 2: PDF PREDATOR (Modify Existing PDFs)
When you select this toolkit, you are asked to drag and drop an existing `.pdf` file. A comprehensive sub-menu appears containing 5 distinct weapons:

#### 1. 🗜️ Image-Based Compression (Max Shrinkage)
*   **What it does:** Destroys file size when you only care about visuals and do not need selectable text.
*   **How it works:** It analyzes your PDF's native resolution and DPI via PyMuPDF. It suggests a target width. You input your desired pixel width and JPEG quality. It then forcefully converts every single page of the PDF into a flattened image, aggressive resizes it down, and rebuilds those images back into a brand new PDF.

#### 2. 📝 Smart Text-Preserving Compression
*   **What it does:** The holy grail of compression. It makes your massive PDFs smaller while **keeping your native text perfectly 100% selectable, sharp, and searchable.**
*   **How it works:** You select a level: Light, Medium, or Heavy. The engine then utilizes deep dictionary diving via PyMuPDF to iterate over every page. It identifies raw embedded image XObjects, evaluates their size, extracts them, runs aggressive LANCZOS downsampling and format optimization (e.g., converting heavy alpha-transparent PNGs to optimized JPEGs), and writes the modified image streams back into the PDF without touching the text layers.
*   **Fallbacks:** If PyMuPDF is missing or fails, it natively attempts structural lossless optimization via `qpdf`, then attempts targeted prepress Ghostscript compression (`gs`), and finally attempts stream deflation via `PyPDF2`.

#### 3. ✂️ Advanced PDF Splitter
*   **What it does:** Extracts pages flawlessly into a new document.
*   **How it works:** It accepts extremely powerful syntax inputs to slice your PDF exactly how you want:
    *   **Ranges:** Type `1-5` to extract pages 1 through 5.
    *   **Specific Pages:** Type `1,3,7` to pluck only those exact pages and stitch them into a new file.
    *   **Single Page:** Type `4` to rip out just page 4.

#### 4. 🖼️ Extract Images from PDF
*   **What it does:** Rips pages out of the PDF and saves them as raw image files to your hard drive.
*   **How it works:** You input the page range (using the exact same powerful `1-5` or `1,3,7` syntax). You then choose an extraction quality:
    *   **Original AF (Type `1`):** Uses PyMuPDF matrices to render a massive 600 DPI output and saves it as a high-quality PNG.
    *   **Lossless PNG (Type `2`):** Zero compression PNG at standard 300 DPI.
    *   **Optimized JPG (Type `3`):** Prompts you for a 1-100 JPEG quality scale to extract pages into smaller file sizes.

#### 5. 🧩 PDF Merger (Franken-stitch)
*   **What it does:** Seamlessly combines multiple disparate PDF files into one single file.
*   **How it works:** Your previously loaded main PDF takes the top position. The console asks you to input additional PDF paths (drag and drop multiple, separated by commas). It utilizes PyMuPDF (falling back to PyPDF2) to inject the PDFs in the precise order provided, applying garbage collection and deflation compression as it saves the final merged document.

---

## 🐍 For Developers: Running from Python Source

If you prefer to run the code manually or modify it, follow these steps:

### 1. Requirements
*   **Python 3.8+** installed on your system.

### 2. Setup the Environment
Open your terminal in the project folder and run:
```bash
# Optional but recommended: Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the required deep formatting Python dependencies
pip install img2pdf PyPDF2 Pillow PyMuPDF pdf2image
```
*Note on external binaries:*
*   To unlock full `pdf2image` and image extraction fallback potential, ensure `poppler` is installed on your OS (`sudo apt-get install poppler-utils` for Debian/Ubuntu, `brew install poppler` for macOS).
*   For extreme lossless compression fallbacks, having `qpdf` and `ghostscript` installed on your system OS gives the tool even more power.

### 3. Run the Script
```bash
python PDF_OOPS.py
```

---

## 🔮 Future Updates
We are actively working on pushing PyInstaller one-file executable releases for **Windows** and **macOS** as well! This ensures full click-and-run support universally without touching a terminal or handling external dependencies.
