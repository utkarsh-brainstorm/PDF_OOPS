#!/usr/bin/env python3
import os
import io
import sys
import time
import random
import tempfile
import re
import subprocess
from pathlib import Path

import img2pdf
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image, UnidentifiedImageError

# ==========================================
# 🚀🔥 IMG2PDF: Nerd Edition v6.9
# ==========================================

def print_banner():
    print("🎉🧠 Welcome to the God-Tier CLI:")
    print("╔════════════════════════════════════════════════╗")
    print("║    🚀🔥  IMG2PDF: Nerd Edition v6.9  💾📚    ║")
    print("╚════════════════════════════════════════════════╝")
    print("📸📥 Taking your chaos of images and birthing a majestic PDF\n")

def loading_bar(task: str, delay=0.2):
    emojis = ["🔧", "🔄", "⏳", "🧪", "🛠️", "🚀"]
    print(f"{random.choice(emojis)} {task}", end="", flush=True)
    for _ in range(6):
        print("✨", end="", flush=True)
        time.sleep(delay)
    print(" ✅")

def roast(msg):
    print(f"💥 ERROR: {msg}")
    quips = [
        "👎 That's not how this works, Einstein.",
        "😩 You had *one job*. And you botched it.",
        "🤡 Even a potato would've figured this out.",
        "🧼 Go wash your hands, then try again like an adult.",
        "🚫 Invalid input detected. Somewhere, a computer is crying.",
        "🔫 You just shot the script in the foot. Bravo."
    ]
    print(random.choice(quips))
    sys.exit(1)

def full_page_layout_fun(image_bytes, image_info, page_size):
    try:
        # Debug information
        print(f"Debug - Page size type: {type(page_size)}, value: {page_size}")
        print(f"Debug - Image info type: {type(image_info)}, value: {image_info}")

        # Handle the case where image_info is an integer (single value)
        if isinstance(image_info, int):
            # Assume it's a square image or use the value as width
            width_px = height_px = image_info
        else:
            # Handle as normal tuple/list
            try:
                width_px, height_px = image_info[0], image_info[1]
            except (IndexError, TypeError):
                # Default to a reasonable size if we can't extract dimensions
                width_px, height_px = 595, 842

        # Convert pixels to points (1 pt = 1/72 inch)
        width_pt = float(width_px)  # No division as img2pdf likely expects pixels
        height_pt = float(height_px)

        # Ensure minimum dimensions
        min_dim = 3.0
        width_pt = max(width_pt, min_dim)
        height_pt = max(height_pt, min_dim)

        # Handle page size - default to A4 if not provided correctly
        if isinstance(page_size, (int, float)):
            page_width = page_height = float(page_size)
        elif isinstance(page_size, (tuple, list)) and len(page_size) >= 2:
            page_width, page_height = float(page_size[0]), float(page_size[1])
        else:
            # Default to A4 size in points (595 x 842 points)
            page_width, page_height = 595.0, 842.0

        # Debug dimensions
        print(f"Debug - Using dimensions: width={width_pt}pt, height={height_pt}pt")
        print(f"Debug - Page size: width={page_width}pt, height={page_height}pt")

        # Calculate layout - let's just return the raw dimensions
        # This creates a PDF page that matches the image size exactly
        return (0, 0, width_pt, height_pt)
    except Exception as e:
        print(f"Layout debug - Exception details: {type(e).__name__}: {e}")
        roast(f"Layout function failed: {e}")

def img2pdf_compress(input_pdf_path, output_pdf_path):
    try:
        reader = PdfReader(str(input_pdf_path))
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.add_metadata({})
        with open(output_pdf_path, "wb") as f:
            writer.write(f)
    except Exception as e:
        roast(f"Compression ritual failed. Details: {e}")

def convert_images_to_pdf(_):
    print_banner()

    # Ask user for folder path directly via input()
    folder_path = input("🗂️  Paste the full path to your image folder: ").strip().strip('"')

    try:
        folder = Path(folder_path).resolve(strict=True)
        if not folder.is_dir():
            roast(f"'{folder}' is not a valid folder. Did you try to upload your feelings instead of images?")
    except FileNotFoundError:
        roast("That folder doesn't exist. Did you just imagine it?")
    except Exception as e:
        roast(f"Something went nuclear trying to access the folder: {e}")

    output_pdf = folder / "compiled_notes.pdf"

    # Ask for JPEG quality
    while True:
        try:
            quality = int(input("🎯 On a scale of 0–100, how Erotic your pdf must be for your purpose? : "))
            if 0 <= quality <= 100:
                break
            else:
                print("🚫 Bro, I said between 0 and 100. Not Jupiter.")
        except ValueError:
            print("🧠 That's not a number. You good? Try again.")

    # Ask user for scaling mode
    while True:
        try:
            scaling_mode = int(input("🧩 Image layout — Type 0 for RELATIVE size, 1 for CONTINUOUS width: "))
            if scaling_mode in [0, 1]:
                break
            else:
                print("❌ Only 0 or 1. You're not designing a space rocket here.")
        except ValueError:
            print("💀 Enter 0 or 1, not your hopes and dreams.")

    # Collect images
    image_exts = [".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"]
    images = sorted(
        [f for f in folder.iterdir() if f.suffix.lower() in image_exts],
        key=lambda x: x.name,
        reverse=False
    )

    if not images:
        roast("Found zero valid image files. What are you feeding me, dreams?")

    loading_bar(f"Found {len(images)} image(s) — converting them into pixel perfection")

    image_streams = []
    image_dims = []
    max_width = 0  # Track the widest image

    for img_path in images:
        try:
            with Image.open(img_path) as img:
                img = img.convert("RGB")
                # Store image dimensions
                img_width, img_height = img.size
                image_dims.append((img_width, img_height))

                # Track the max width
                max_width = max(max_width, img_width)

                # Convert to bytes
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=quality)
                image_streams.append(buffer.getvalue())
                print(f"✓ Processed {img_path.name}: {img_width}×{img_height}")
        except UnidentifiedImageError:
            print(f"🤮 {img_path.name} is not even a real image. I'm disgusted.")
        except Exception as e:
            roast(f"Couldn't process {img_path.name}: {e}")

    if not image_streams:
        roast("All your images failed. Are you trolling me?")

    # For continuous width mode, ask for target width
    target_width = max_width
    if scaling_mode == 1:
        print(f"📏 Maximum image width detected: {max_width}px")
        width_input = input(f"Enter desired width in pixels (n/N to use maximum width of {max_width}px): ").strip()

        if width_input.lower() != 'n':
            try:
                custom_width = int(width_input)
                if custom_width <= 0:
                    print(f"🚫 Width must be positive. Using maximum width of {max_width}px instead.")
                else:
                    target_width = custom_width
                    print(f"✓ Using custom width: {target_width}px")
            except ValueError:
                print(f"🚫 Invalid input. Using maximum width of {max_width}px instead.")

    loading_bar("Binding your data sins into a beautiful PDF scroll 📜📎")

    if scaling_mode == 0:
        # OPTION 0: Relative size mode - use img2pdf directly
        try:
            with open(output_pdf, "wb") as f:
                f.write(img2pdf.convert(image_streams, auto_orient=True))
            print(f"✅ Relative size PDF created at: {output_pdf}")
        except Exception as e:
            print(f"Conversion error: {e}")
            roast(f"Couldn't save the PDF. Disk full? Permissions? Demons? Details: {e}")
    else:
        # OPTION 1: CONTINUOUS WIDTH - all images have same width
        try:
            print(f"Creating continuous width PDF with width: {target_width}px")

            # Create temporary directory for processing
            temp_dir = folder / "temp_img2pdf"
            temp_dir.mkdir(exist_ok=True)

            # Resize all images to the same width
            resized_images = []

            for i, (img_bytes, dims) in enumerate(zip(image_streams, image_dims)):
                orig_width, orig_height = dims

                # Calculate new height preserving aspect ratio
                new_height = int(orig_height * (target_width / orig_width))

                print(f"Resizing image {i+1}: {orig_width}x{orig_height} → {target_width}x{new_height}")

                # Create a temporary file for this image
                temp_img_path = temp_dir / f"resized_{i}.jpg"

                # Resize and save the image
                img = Image.open(io.BytesIO(img_bytes))
                img = img.resize((target_width, new_height), Image.LANCZOS)
                img.save(temp_img_path, format="JPEG", quality=quality)

                # Add to list for conversion
                resized_images.append(str(temp_img_path))

            # Convert all resized images to PDF
            with open(output_pdf, "wb") as f:
                f.write(img2pdf.convert(resized_images))

            # Clean up temporary files
            for img_path in resized_images:
                try:
                    Path(img_path).unlink()
                except:
                    pass

            # Remove temp directory
            try:
                temp_dir.rmdir()
            except:
                pass

            print(f"✅ Continuous width PDF created at: {output_pdf}")

        except Exception as e:
            print(f"Conversion error: {e}")
            roast(f"Couldn't save the PDF. Disk full? Permissions? Demons? Details: {e}")

    # Ask for compression
    compress = input("💢 Want to SQUISH this PDF down like a college budget? (y/n): ").strip().lower()
    if compress == 'y':
        compressed_pdf = folder / "compiled_notes_compressed.pdf"
        loading_bar("Crunching PDF with dark magic & caffeine 💀☕")
        img2pdf_compress(output_pdf, compressed_pdf)
        print(f"🥷 Final compressed version ready at: {compressed_pdf}")
    else:
        print("🧘 Keeping the PDF full-fat. You're either brave or reckless.")

    print("\n💡 Pro Tip: This CLI just made 99% of converters look like cavemen.\n")


# ==========================================
# 🔥 PDF BEAST 🔥 - The Ultimate PDF Slayer
# ==========================================

def get_pdf_path():
    """Get the PDF path from the user."""
    while True:
        pdf_path = input("📂 Drop your PDF path here like it's hot: ").strip()

        # Handle paths with quotes (both single and double quotes)
        if (pdf_path.startswith('"') and pdf_path.endswith('"')) or (pdf_path.startswith("'") and pdf_path.endswith("'")):
            pdf_path = pdf_path[1:-1]

        # Handle escaped spaces in paths
        pdf_path = pdf_path.replace("\\ ", " ")

        if not os.path.isfile(pdf_path):
            print("❌ Yo dumbass, that file doesn't even EXIST. Check your path or go cry.")
            continue

        if not pdf_path.lower().endswith('.pdf'):
            print("🚫 This ain't a PDF, genius. Feed me the real shit.")
            continue

        print(f"✅ File found: {pdf_path} – Locked, loaded, and ready to dominate. 🔥")
        return pdf_path

def get_pdf_resolution(pdf_path):
    """Get resolution info from PDF."""
    max_width = 0
    max_height = 0
    max_dpi = 0
    has_images = False

    try:
        # Try PyMuPDF first
        try:
            import fitz  # PyMuPDF
            pdf_document = fitz.open(pdf_path)

            for page_number in range(len(pdf_document)):
                page = pdf_document.load_page(page_number)

                # Get page dimensions in points (1/72 inch)
                rect = page.rect
                width_pt, height_pt = rect.width, rect.height

                # Get images on the page
                image_list = page.get_images(full=True)
                for img_index, img_info in enumerate(image_list):
                    xref = img_info[0]
                    base_image = pdf_document.extract_image(xref)
                    image_width = base_image["width"]
                    image_height = base_image["height"]

                    has_images = True
                    max_width = max(max_width, image_width)
                    max_height = max(max_height, image_height)

                # Update max dimensions based on page size too
                max_width = max(max_width, int(width_pt))
                max_height = max(max_height, int(height_pt))

            pdf_document.close()

            # If we have images, estimate DPI based on page size
            if has_images and max_width > 0 and max_height > 0:
                # Estimate DPI: most PDFs are created at 72 DPI
                estimated_dpi = max(max_width / (width_pt / 72), max_height / (height_pt / 72))
                max_dpi = max(max_dpi, int(estimated_dpi))

        except ImportError:
            # Fallback to PyPDF2
            reader = PdfReader(pdf_path)

            for i, page in enumerate(reader.pages):
                # Get page dimensions in points (1/72 inch)
                media_box = page.mediabox
                width_pt = float(media_box.width)
                height_pt = float(media_box.height)

                # Update max dimensions based on page size
                max_width = max(max_width, int(width_pt))
                max_height = max(max_height, int(height_pt))

                # Try to check if page has images
                if '/Resources' in page and '/XObject' in page['/Resources']:
                    xObject = page['/Resources']['/XObject'].get_object()

                    for obj in xObject:
                        if xObject[obj]['/Subtype'] == '/Image':
                            has_images = True
                            img_width = int(xObject[obj]['/Width'])
                            img_height = int(xObject[obj]['/Height'])

                            max_width = max(max_width, img_width)
                            max_height = max(max_height, img_height)

            # Estimate DPI if we have images
            if has_images and max_width > 0 and max_height > 0:
                # Rough estimation based on typical PDF point to pixel conversion
                max_dpi = int(max(max_width / (width_pt / 72), max_height / (height_pt / 72)))

        if not has_images:
            # If no images found, use typical PDF resolution of 72 DPI
            max_dpi = 72

        return {
            "width": max_width,
            "height": max_height,
            "dpi": max_dpi,
            "has_images": has_images
        }

    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return {
            "width": 0,
            "height": 0,
            "dpi": 0,
            "has_images": False
        }

def compress_pdf(pdf_path):
    """Compress PDF with user-defined parameters."""
    print("\n💪 Crunching your bloated PDF... time to put it on a data diet 🥦📉")

    # Record start time
    start_time = time.time()

    # First, get original PDF resolution
    print("📏 Analyzing PDF resolution...")
    resolution_info = get_pdf_resolution(pdf_path)

    if resolution_info["has_images"]:
        print(f"📊 PDF SPECS:")
        print(f"   ▸ Max resolution: {resolution_info['width']} × {resolution_info['height']} pixels")
        print(f"   ▸ Estimated DPI: {resolution_info['dpi']}")
        print(f"   ▸ Contains images: Yes")
    else:
        print(f"📊 PDF SPECS:")
        print(f"   ▸ Page dimensions: {resolution_info['width']} × {resolution_info['height']} points")
        print(f"   ▸ Standard DPI: {resolution_info['dpi']} (text-based PDF)")
        print(f"   ▸ Contains images: No")

    # Get original file size
    original_size = os.path.getsize(pdf_path)

    # Suggest compression width based on current resolution
    suggested_width = min(1200, resolution_info['width'])
    if resolution_info['width'] > 0:
        print(f"\n💡 COMPRESSION SUGGESTION:")
        print(f"   For good quality: {suggested_width} width (maintains readability)")
        print(f"   For small file: {int(suggested_width/2)} width (may reduce quality)")
        print(f"   Keep quality above 85 for text readability.")

    # Get compression parameters
    width = int(input(f"\nEnter the desired width in pixels [{suggested_width}]: ") or suggested_width)
    quality = int(input("Enter the JPEG quality (1-100) [85]: ") or 85)
    if quality < 1 or quality > 100:
        quality = 85  # Default if invalid input
        print(f"Invalid quality value. Using default quality: {quality}")

    # Output file path
    output_dir = os.path.dirname(pdf_path)
    base_name = os.path.basename(pdf_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_dir, f"{name_without_ext}_compressed.pdf")

    try:
        # First, let's try a different approach for text-based PDFs using pdf2image + PIL
        print("Converting PDF to images and compressing...")
        # Create temporary directory for image conversion
        temp_dir = tempfile.mkdtemp()

        # Get images for each page
        images = []
        try:
            try:
                import fitz  # PyMuPDF
                pdf_document = fitz.open(pdf_path)

                for page_number in range(len(pdf_document)):
                    print(f"Processing page {page_number+1}/{len(pdf_document)}")
                    page = pdf_document.load_page(page_number)
                    pix = page.get_pixmap(alpha=False)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                    # Calculate height maintaining aspect ratio
                    aspect_ratio = img.height / img.width
                    height = int(width * aspect_ratio)

                    # Resize and compress
                    img = img.resize((width, height), Image.LANCZOS)

                    # Save to the temp directory
                    temp_img_path = os.path.join(temp_dir, f"page_{page_number+1}.jpg")
                    img.save(temp_img_path, format='JPEG', quality=quality)
                    images.append(temp_img_path)

                pdf_document.close()

            except ImportError:
                try:
                    from pdf2image import convert_from_path
                    print("Using pdf2image for conversion...")

                    # Convert PDF to images
                    pdf_images = convert_from_path(pdf_path, dpi=300)

                    for i, img in enumerate(pdf_images):
                        print(f"Processing page {i+1}/{len(pdf_images)}")
                        # Calculate height maintaining aspect ratio
                        aspect_ratio = img.height / img.width
                        height = int(width * aspect_ratio)

                        # Resize and compress
                        img = img.resize((width, height), Image.LANCZOS)

                        # Save to the temp directory
                        temp_img_path = os.path.join(temp_dir, f"page_{i+1}.jpg")
                        img.save(temp_img_path, format='JPEG', quality=quality)
                        images.append(temp_img_path)

                except ImportError:
                    print("Both PyMuPDF and pdf2image not installed. Trying alternative method.")
                    raise

            # Create a new PDF with compressed images
            writer = PdfWriter()

            # Add each compressed image as a page
            for img_path in images:
                img = Image.open(img_path)
                pdf_bytes = io.BytesIO()
                img.save(pdf_bytes, format='PDF')
                pdf_bytes.seek(0)

                # Add the compressed page to the output PDF
                compressed_reader = PdfReader(pdf_bytes)
                writer.add_page(compressed_reader.pages[0])

            # Save the compressed PDF
            with open(output_path, 'wb') as f_out:
                writer.write(f_out)

            # Clean up temp files
            for img_path in images:
                if os.path.exists(img_path):
                    os.remove(img_path)
            os.rmdir(temp_dir)

            print(f"🍑 Boom! Compressed PDF saved as: {output_path}")

            # Calculate summary
            new_size = os.path.getsize(output_path)
            elapsed_time = time.time() - start_time

            # Summary
            reduction = (1 - (new_size / original_size)) * 100 if original_size > 0 else 0
            print("\n✅ IMAGE-BASED COMPRESSION SUMMARY:")
            print(f"  • Original file size: {original_size / 1024:.1f} KB")
            print(f"  • New file size: {new_size / 1024:.1f} KB")
            print(f"  • Size reduction: {reduction:.1f}%")
            print(f"  • Processing time: {elapsed_time:.1f} seconds")
            print(f"  • Quality setting: {quality}/100")
            print(f"  • Width setting: {width}px")

            return output_path

        except Exception as inner_e:
            print(f"Image-based compression failed: {inner_e}")
            print("Trying alternative compression method...")

            # Fallback to original method for image-based PDFs
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            print(f"Compressing {len(reader.pages)} pages...")

            # Process each page
            for i, page in enumerate(reader.pages):
                print(f"Processing page {i+1}/{len(reader.pages)}")

                try:
                    # Check if the page has images
                    if '/Resources' in page and '/XObject' in page['/Resources']:
                        xObject = page['/Resources']['/XObject'].get_object()
                        has_images = False

                        for obj in xObject:
                            if xObject[obj]['/Subtype'] == '/Image':
                                has_images = True
                                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                                data = xObject[obj].get_data()
                                if '/ColorSpace' in xObject[obj]:
                                    mode = "RGB"
                                else:
                                    mode = "P"

                                img = Image.open(io.BytesIO(data))

                                # Calculate height maintaining aspect ratio
                                aspect_ratio = img.height / img.width
                                height = int(width * aspect_ratio)

                                # Resize and compress
                                img = img.resize((width, height), Image.LANCZOS)

                                # Convert to bytes
                                img_bytes = io.BytesIO()
                                img.save(img_bytes, format='JPEG', quality=quality)
                                img_bytes.seek(0)

                                # Create a new PDF with the compressed image
                                img = Image.open(img_bytes)
                                pdf_bytes = io.BytesIO()
                                img.save(pdf_bytes, format='PDF')
                                pdf_bytes.seek(0)

                                # Add the compressed page to the output PDF
                                compressed_reader = PdfReader(pdf_bytes)
                                writer.add_page(compressed_reader.pages[0])
                                break

                        if not has_images:
                            # Just add the page without modification if no images found
                            writer.add_page(page)
                    else:
                        # No resources or XObject, just add the page
                        writer.add_page(page)
                except Exception as page_error:
                    print(f"Error processing page {i+1}: {page_error}")
                    # Add original page as fallback
                    writer.add_page(page)

            # Save the compressed PDF
            with open(output_path, 'wb') as f_out:
                writer.write(f_out)

            print(f"🍑 Boom! Compressed PDF saved as: {output_path}")

            # Calculate summary
            new_size = os.path.getsize(output_path)
            elapsed_time = time.time() - start_time

            # Summary
            reduction = (1 - (new_size / original_size)) * 100 if original_size > 0 else 0
            print("\n✅ IMAGE-BASED COMPRESSION SUMMARY:")
            print(f"  • Original file size: {original_size / 1024:.1f} KB")
            print(f"  • New file size: {new_size / 1024:.1f} KB")
            print(f"  • Size reduction: {reduction:.1f}%")
            print(f"  • Processing time: {elapsed_time:.1f} seconds")
            print(f"  • Quality setting: {quality}/100")
            print(f"  • Width setting: {width}px")

            return output_path

    except Exception as e:
        print(f"💩 Shit hit the fan while compressing: {e}")
        return None

def compress_pdf_text(pdf_path):
    """Compress PDF while preserving text content for searchability and copy operations.
    This function only compresses images while leaving all text untouched."""
    print("\n📝 Smart PDF compression - keeps text intact, shrinks only the images 📸↓")

    # Record start time
    start_time = time.time()

    # First, get original PDF resolution
    print("📏 Analyzing PDF resolution...")
    resolution_info = get_pdf_resolution(pdf_path)

    if resolution_info["has_images"]:
        print(f"📊 PDF SPECS:")
        print(f"   ▸ Max resolution: {resolution_info['width']} × {resolution_info['height']} pixels")
        print(f"   ▸ Estimated DPI: {resolution_info['dpi']}")
        print(f"   ▸ Contains images: Yes")
    else:
        print(f"📊 PDF SPECS:")
        print(f"   ▸ Page dimensions: {resolution_info['width']} × {resolution_info['height']} points")
        print(f"   ▸ Standard DPI: {resolution_info['dpi']} (text-based PDF)")
        print(f"   ▸ Contains images: No")
        print("⚠️ No images found in PDF. Compression will have minimal effect.")

    # Output file path
    output_dir = os.path.dirname(pdf_path)
    base_name = os.path.basename(pdf_path)
    name_without_ext = os.path.splitext(base_name)[0]
    output_path = os.path.join(output_dir, f"{name_without_ext}_compressed_text.pdf")

    print("\n💡 IMAGE COMPRESSION LEVELS:")
    print("1. 💎 LIGHT - Minimal compression, excellent image quality")
    print("2. 📊 MEDIUM - Good balance of quality and file size")
    print("3. 📱 HEAVY - Maximum compression, smaller files for sharing")

    level = input("Choose compression level (1-3) [2]: ").strip() or "2"

    # Get original file size for comparison
    original_size = os.path.getsize(pdf_path)
    print(f"📄 Original PDF size: {original_size / 1024:.1f} KB")

    # Convert level to compression parameters for images only
    if level == "1":  # Light
        image_quality = 90
        image_resize_threshold = 1800  # Only resize very large images
        print("⚙️ Using LIGHT image compression (text untouched)...")
    elif level == "3":  # Heavy
        image_quality = 40  # More aggressive compression
        image_resize_threshold = 800  # More aggressive resizing
        print("⚙️ Using HEAVY image compression (text untouched)...")
    else:  # Medium (default)
        image_quality = 65  # More aggressive than before
        image_resize_threshold = 1200  # More aggressive resizing
        print("⚙️ Using MEDIUM image compression (text untouched)...")

    temp_output_path = None

    try:
        # Most reliable approach: Use PyMuPDF to directly target images only
        try:
            import fitz  # PyMuPDF
            print("🔍 Scanning for images to compress...")

            # Open the PDF
            pdf_document = fitz.open(pdf_path)

            # Track image compression stats
            total_images = 0
            compressed_images = 0
            original_image_bytes = 0
            new_image_bytes = 0

            # Process each page
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                print(f"Processing page {page_num+1}/{len(pdf_document)}")

                # Find all images on the page
                image_list = page.get_images(full=True)

                if len(image_list) > 0:
                    print(f"  Found {len(image_list)} image(s) on page {page_num+1}")

                # Process each image
                for img_index, xref in enumerate(image_list):
                    xref_obj = xref[0]  # XREF number
                    try:
                        base_image = pdf_document.extract_image(xref_obj)

                        if base_image:
                            total_images += 1
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]
                            original_img_size = len(image_bytes)
                            original_image_bytes += original_img_size

                            # Skip tiny images - not worth compressing
                            if base_image.get("width", 0) < 50 or base_image.get("height", 0) < 50 or original_img_size < 5000:
                                print(f"  Skipping small image ({base_image.get('width', 0)}×{base_image.get('height', 0)}, {original_img_size/1024:.1f} KB)")
                                continue

                            print(f"  Image {img_index+1}: {base_image.get('width', 0)}×{base_image.get('height', 0)} pixels, {original_img_size/1024:.1f} KB")

                            # Load image for processing
                            img = Image.open(io.BytesIO(image_bytes))

                            # Check if image needs resizing (but preserve aspect ratio)
                            needs_resize = (img.width > image_resize_threshold or img.height > image_resize_threshold)

                            if needs_resize:
                                # Calculate new dimensions
                                aspect_ratio = img.height / img.width
                                if img.width > img.height:
                                    new_width = min(img.width, image_resize_threshold)
                                    new_height = int(new_width * aspect_ratio)
                                else:
                                    new_height = min(img.height, image_resize_threshold)
                                    new_width = int(new_height / aspect_ratio)

                                print(f"  Resizing from {img.width}×{img.height} to {new_width}×{new_height}")
                                # Use high-quality LANCZOS resampling
                                img = img.resize((new_width, new_height), Image.LANCZOS)

                            # Compress image based on type
                            img_bytes = io.BytesIO()

                            # More aggressive compression for all image types
                            if image_ext.lower() in ["jpg", "jpeg"]:
                                # For JPEGs, apply quality reduction and optimization
                                img.save(img_bytes, format="JPEG", quality=image_quality, optimize=True)
                            elif image_ext.lower() == "png":
                                # For PNGs, handle transparency
                                has_alpha = img.mode == 'RGBA' or 'transparency' in img.info
                                if has_alpha:
                                    # Preserve transparency for PNGs that need it but with compression
                                    img.save(img_bytes, format="PNG", optimize=True, compress_level=9)
                                else:
                                    # Convert non-transparent PNGs to JPEG for better compression
                                    img = img.convert('RGB')
                                    img.save(img_bytes, format="JPEG", quality=image_quality, optimize=True)
                            else:
                                # Other formats, convert to JPEG with quality setting
                                if img.mode == 'RGBA':
                                    img = img.convert('RGB')
                                img.save(img_bytes, format="JPEG", quality=image_quality, optimize=True)

                            # Check if we achieved compression
                            img_bytes.seek(0)
                            new_bytes = img_bytes.getvalue()
                            new_size = len(new_bytes)
                            new_image_bytes += new_size

                            savings = original_img_size - new_size
                            savings_percent = (savings / original_img_size) * 100 if original_img_size > 0 else 0

                            # Only replace if we actually reduced size
                            if new_size < original_img_size:
                                print(f"  ✅ Compressed image by {savings_percent:.1f}% ({original_img_size/1024:.1f}KB → {new_size/1024:.1f}KB)")
                                page.replace_image(xref_obj, stream=new_bytes)
                                compressed_images += 1
                            else:
                                print(f"  ⚠️ No size reduction, keeping original")

                    except Exception as img_err:
                        print(f"  ⚠️ Error processing image: {img_err}")

            # Only proceed if we have actually compressed some images
            if compressed_images > 0:
                # Create temporary file
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                    temp_output_path = tmp.name

                # Save the PDF with compressed images but untouched text
                try:
                    # Try with garbage collection but handle older versions
                    pdf_document.save(temp_output_path,
                                    deflate=True,     # Use deflate compression for streams
                                    clean=True,       # Clean/sanitize content
                                    garbage=3,        # Garbage collection level
                                    pretty=False)     # No pretty printing (saves space)
                except TypeError:
                    # Fallback for older PyMuPDF versions without garbage parameter
                    pdf_document.save(temp_output_path,
                                    deflate=True,     # Use deflate compression for streams
                                    clean=True,       # Clean/sanitize content
                                    pretty=False)     # No pretty printing (saves space)

                pdf_document.close()

                # Check if we've actually reduced the file size
                if os.path.exists(temp_output_path):
                    temp_size = os.path.getsize(temp_output_path)

                    if temp_size < original_size:
                        # Success! Move to final location
                        import shutil
                        shutil.move(temp_output_path, output_path)
                        temp_output_path = None  # Mark as moved

                        new_size = os.path.getsize(output_path)
                        reduction = (1 - (new_size / original_size)) * 100

                        # Report results
                        print("\n✅ PDF compression summary:")
                        print(f"  • Found {total_images} images, compressed {compressed_images}")
                        print(f"  • Original file size: {original_size / 1024:.1f} KB")
                        print(f"  • New file size: {new_size / 1024:.1f} KB")
                        print(f"  • Size reduction: {reduction:.1f}%")
                        print(f"  • Image bytes saved: {(original_image_bytes - new_image_bytes) / 1024:.1f} KB")
                        print(f"  • Text content: 100% preserved and searchable")
                        print(f"  • Processing time: {time.time() - start_time:.1f} seconds")
                        print(f"\n🧠 Smart PDF saved as: {output_path}")

                        return output_path
                    else:
                        # No size reduction - discard and try another approach
                        print(f"⚠️ Compressed file not smaller than original ({temp_size/1024:.1f}KB > {original_size/1024:.1f}KB)")
                        os.unlink(temp_output_path)
                        temp_output_path = None
            else:
                print("⚠️ No images were successfully compressed. Trying alternative method.")

        except ImportError:
            print("PyMuPDF not available. Falling back to alternative method.")
        except Exception as pymupdf_error:
            print(f"Error with PyMuPDF method: {pymupdf_error}")

        # Try using qpdf for image-only compression (if available)
        try:
            print("🔄 Trying qpdf for lossless optimization...")

            # Create a temp file path for output
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                temp_output_path = tmp.name

            # Check if qpdf is available
            try:
                # Try qpdf command to check if it's available
                check_qpdf = subprocess.run(["qpdf", "--version"],
                                           capture_output=True,
                                           text=True)
                qpdf_available = check_qpdf.returncode == 0
            except FileNotFoundError:
                qpdf_available = False

            if qpdf_available:
                # Use qpdf to optimize the PDF structure
                print("Using qpdf for lossless optimization...")
                qpdf_cmd = ["qpdf", "--linearize", "--compress-streams=y", "--recompress-flate",
                           "--object-streams=generate", pdf_path, temp_output_path]

                result = subprocess.run(qpdf_cmd, capture_output=True, text=True)
                qpdf_success = result.returncode == 0

                if qpdf_success and os.path.exists(temp_output_path):
                    # Check if we've actually reduced the file size
                    temp_size = os.path.getsize(temp_output_path)

                    if temp_size < original_size:
                        # Success! Move to final location
                        import shutil
                        shutil.move(temp_output_path, output_path)
                        temp_output_path = None  # Mark as moved

                        new_size = os.path.getsize(output_path)
                        reduction = (1 - (new_size / original_size)) * 100

                        print(f"✅ Lossless optimization successful!")
                        print(f"  • Original size: {original_size / 1024:.1f} KB")
                        print(f"  • New size: {new_size / 1024:.1f} KB")
                        print(f"  • Reduction: {reduction:.1f}%")
                        print(f"  • Text: 100% preserved and searchable")
                        print(f"  • Processing time: {time.time() - start_time:.1f} seconds")
                        print(f"\n🧠 Optimized PDF saved as: {output_path}")

                        return output_path
                    else:
                        print("⚠️ qpdf output not smaller than original")
                        os.unlink(temp_output_path)
                        temp_output_path = None
            else:
                print("qpdf not found, trying Ghostscript...")

        except Exception as qpdf_error:
            print(f"Error with qpdf method: {qpdf_error}")

        # Fallback: Try GhostScript for image-only compression
        try:
            print("🔄 Trying Ghostscript for targeted image compression...")

            # Check if ghostscript is available before proceeding
            gs_available = False
            gs_command = None

            # Try both 'gs' and 'gswin64c.exe' to see which one exists
            try:
                check_gs = subprocess.run(["gs", "--version"],
                                         capture_output=True,
                                         text=True)
                if check_gs.returncode == 0:
                    gs_available = True
                    gs_command = "gs"
            except FileNotFoundError:
                try:
                    check_gs = subprocess.run(["gswin64c.exe", "--version"],
                                             capture_output=True,
                                             text=True)
                    if check_gs.returncode == 0:
                        gs_available = True
                        gs_command = "gswin64c.exe"
                except FileNotFoundError:
                    pass

            if not gs_available:
                print("⚠️ Ghostscript not found on your system. Skipping this method.")
                raise FileNotFoundError("Ghostscript not installed or not in PATH")

            # Create a temp file path for output
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                temp_output_path = tmp.name

            # Use GhostScript parameters that preserve text but compress images
            if level == "1":  # Light
                gs_params = [
                    "-dPDFSETTINGS=/prepress",
                    "-dColorConversionStrategy=/LeaveColorUnchanged",
                    "-dDownsampleColorImages=true",
                    "-dDownsampleGrayImages=true",
                    "-dDownsampleMonoImages=false",
                    "-dColorImageResolution=150",
                    "-dGrayImageResolution=150",
                    f"-dJPEGQuality={image_quality}"
                ]
            elif level == "3":  # Heavy
                gs_params = [
                    "-dPDFSETTINGS=/ebook",
                    "-dDownsampleColorImages=true",
                    "-dDownsampleGrayImages=true",
                    "-dDownsampleMonoImages=false",
                    "-dColorImageResolution=72",
                    "-dGrayImageResolution=72",
                    f"-dJPEGQuality={image_quality}"
                ]
            else:  # Medium
                gs_params = [
                    "-dPDFSETTINGS=/printer",
                    "-dDownsampleColorImages=true",
                    "-dDownsampleGrayImages=true",
                    "-dDownsampleMonoImages=false",
                    "-dColorImageResolution=120",
                    "-dGrayImageResolution=120",
                    f"-dJPEGQuality={image_quality}"
                ]

            # Special params to ensure text is completely preserved
            text_preserving_params = [
                "-dAutoFilterColorImages=false",
                "-dAutoFilterGrayImages=false",
                "-dCompressFonts=false",      # Don't modify fonts
                "-dEmbedAllFonts=true",       # Keep all fonts embedded
                "-dSubsetFonts=false",        # Don't subset fonts (keeps all characters)
                "-dPreserveAnnots=true",      # Keep annotations
                "-dPreserveMarkedContent=true", # Keep marked content
                "-dPreserveOCProperties=true"  # Keep OCR properties
            ]

            # Common parameters
            common_params = [
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=pdfwrite",
                "-dDetectDuplicateImages=true",
                "-dOptimize=true"
            ]

            # Run GhostScript with all parameters
            gs_command_line = [gs_command] + common_params + gs_params + text_preserving_params + [
                f"-sOutputFile={temp_output_path}", pdf_path
            ]

            print(f"Running Ghostscript with command: {gs_command}")
            result = subprocess.run(gs_command_line, capture_output=True, text=True)
            gs_success = result.returncode == 0

            if gs_success and os.path.exists(temp_output_path):
                # Check if we've actually reduced the file size
                temp_size = os.path.getsize(temp_output_path)

                if temp_size < original_size:
                    # Success! Move to final location
                    import shutil
                    shutil.move(temp_output_path, output_path)
                    temp_output_path = None  # Mark as moved

                    new_size = os.path.getsize(output_path)
                    reduction = (1 - (new_size / original_size)) * 100

                    print(f"✅ Compression successful!")
                    print(f"  • Original size: {original_size / 1024:.1f} KB")
                    print(f"  • New size: {new_size / 1024:.1f} KB")
                    print(f"  • Reduction: {reduction:.1f}%")
                    print(f"  • Text: 100% preserved and searchable")
                    print(f"  • Processing time: {time.time() - start_time:.1f} seconds")
                    print(f"\n🧠 PDF with compressed images saved as: {output_path}")

                    return output_path
                else:
                    print(f"⚠️ GhostScript output larger than original, discarding result")
                    os.unlink(temp_output_path)
                    temp_output_path = None
            else:
                print(f"⚠️ GhostScript processing failed: {result.stderr}")

        except FileNotFoundError:
            print("⚠️ Ghostscript not available on this system")
        except Exception as gs_error:
            print(f"Error with GhostScript method: {gs_error}")

        # Last resort: try PyPDF2 with image optimization
        try:
            print("🔄 Trying PyPDF2 with image optimization...")

            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                temp_output_path = tmp.name

            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            # Process each page
            for i, page in enumerate(reader.pages):
                writer.add_page(page)

            # Write to temp file
            with open(temp_output_path, 'wb') as f_out:
                writer.write(f_out)

            # Check if we've actually reduced the file size
            temp_size = os.path.getsize(temp_output_path)

            if temp_size < original_size:
                # Success! Move to final location
                import shutil
                shutil.move(temp_output_path, output_path)
                temp_output_path = None  # Mark as moved

                new_size = os.path.getsize(output_path)
                reduction = (1 - (new_size / original_size)) * 100

                print(f"✅ Basic optimization successful!")
                print(f"  • Original size: {original_size / 1024:.1f} KB")
                print(f"  • New size: {new_size / 1024:.1f} KB")
                print(f"  • Reduction: {reduction:.1f}%")
                print(f"  • Processing time: {time.time() - start_time:.1f} seconds")
                print(f"\n🧠 Optimized PDF saved as: {output_path}")

                return output_path
            else:
                print(f"⚠️ PyPDF2 output not smaller than original")
                os.unlink(temp_output_path)
                temp_output_path = None

        except Exception as pypdf_error:
            print(f"Error with PyPDF2 method: {pypdf_error}")

        # If all compression methods failed to reduce size, just copy the original
        print("\n⚠️ No compression method could reduce file size.")
        print("🔍 This may happen if:")
        print("  • The PDF is already well-optimized")
        print("  • Images are already compressed efficiently")
        print("  • The PDF contains mostly text content")

        elapsed_time = time.time() - start_time
        print(f"\n💡 Process completed in {elapsed_time:.1f} seconds")
        print("\n📄 Creating an uncompressed copy.")
        import shutil
        shutil.copy2(pdf_path, output_path)
        print(f"📄 Original file copied to: {output_path}")
        return output_path

    except Exception as e:
        print(f"🤕 Text-preserving compression failed: {e}")
        # Clean up any temporary files
        try:
            if temp_output_path and os.path.exists(temp_output_path):
                os.unlink(temp_output_path)
        except:
            pass
        return None

def split_pdf(pdf_path):
    """Split PDF based on user input ranges."""
    print("\n--- PDF Splitting ---")

    # Record start time
    start_time = time.time()

    # Get original file size
    original_size = os.path.getsize(pdf_path)

    try:
        # Read the original PDF
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"📚 This bad boy has {total_pages} pages – time to split it like a toxic relationship 🪓")

        # Get page range from user
        range_input = input(f"Enter page range (e.g., '1-5' for a range, '1,3,5' for specific pages, or just '7' for a single page): ")

        # Output directory
        output_dir = os.path.dirname(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        # Process the input
        if '-' in range_input and ',' not in range_input:  # Range like 1-5
            start, end = map(int, range_input.split('-'))
            if start < 1 or end > total_pages or start > end:
                print(f"Invalid range. Must be between 1 and {total_pages}.")
                return

            # Create PDF with the specified range
            writer = PdfWriter()
            for i in range(start-1, end):
                writer.add_page(reader.pages[i])

            output_path = os.path.join(output_dir, f"{base_name}_pages_{start}-{end}.pdf")
            with open(output_path, 'wb') as f_out:
                writer.write(f_out)

            # Calculate summary
            new_size = os.path.getsize(output_path)
            elapsed_time = time.time() - start_time

            print("\n✅ PDF SPLITTING SUMMARY:")
            print(f"  • Original PDF: {total_pages} pages, {original_size / 1024:.1f} KB")
            print(f"  • Extracted: {end-start+1} pages ({start}-{end})")
            print(f"  • New file size: {new_size / 1024:.1f} KB")
            print(f"  • Processing time: {elapsed_time:.1f} seconds")
            print(f"📤 Page range {start}-{end} ripped out and saved as: {output_path}")

        elif ',' in range_input:  # Specific pages like 1,3,5
            page_numbers = [int(p.strip()) for p in range_input.split(',')]

            # Validate page numbers
            if any(p < 1 or p > total_pages for p in page_numbers):
                print(f"Invalid page number. Must be between 1 and {total_pages}.")
                return

            # Create PDF with the specified pages
            writer = PdfWriter()
            for page_num in page_numbers:
                writer.add_page(reader.pages[page_num-1])

            output_path = os.path.join(output_dir, f"{base_name}_pages_{'_'.join(map(str, page_numbers))}.pdf")
            with open(output_path, 'wb') as f_out:
                writer.write(f_out)

            # Calculate summary
            new_size = os.path.getsize(output_path)
            elapsed_time = time.time() - start_time

            print("\n✅ PDF SPLITTING SUMMARY:")
            print(f"  • Original PDF: {total_pages} pages, {original_size / 1024:.1f} KB")
            print(f"  • Extracted: {len(page_numbers)} pages ({', '.join(map(str, page_numbers))})")
            print(f"  • New file size: {new_size / 1024:.1f} KB")
            print(f"  • Processing time: {elapsed_time:.1f} seconds")
            print(f"📤 Selected pages {', '.join(map(str, page_numbers))} ripped out and saved as: {output_path}")

        else:  # Single page
            try:
                page_num = int(range_input)
                if page_num < 1 or page_num > total_pages:
                    print(f"Invalid page number. Must be between 1 and {total_pages}.")
                    return

                # Create PDF with the single page
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num-1])

                output_path = os.path.join(output_dir, f"{base_name}_page_{page_num}.pdf")
                with open(output_path, 'wb') as f_out:
                    writer.write(f_out)

                # Calculate summary
                new_size = os.path.getsize(output_path)
                elapsed_time = time.time() - start_time

                print("\n✅ PDF SPLITTING SUMMARY:")
                print(f"  • Original PDF: {total_pages} pages, {original_size / 1024:.1f} KB")
                print(f"  • Extracted: 1 page (page {page_num})")
                print(f"  • New file size: {new_size / 1024:.1f} KB")
                print(f"  • Processing time: {elapsed_time:.1f} seconds")
                print(f"📤 Page {page_num} ripped out and saved as: {output_path}")

            except ValueError:
                print("Invalid input. Please follow the format instructions.")
                return
    except Exception as e:
        print(f"🤡 Failed to split: {e} – maybe don't feed me garbage next time.")
        return None

def extract_images(pdf_path):
    """Extract images from PDF pages."""
    print("\n🧽 Time to suck the soul (and the JPEGs) out of this PDF... 🧛‍♂️")

    # Record start time
    start_time = time.time()

    try:
        # Read the original PDF
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        print(f"📚 This bad boy has {total_pages} pages.")

        # Get page range from user
        range_input = input(f"Enter page range (e.g., '1-5' for a range, '1,3,5' for specific pages, or just '7' for a single page): ")

        # Get quality preference
        print("\n🔥 QUALITY OPTIONS 🔥")
        print("1. 💎 ORIGINAL AF - Exact same quality as in PDF (chonky files, maximum detail)")
        print("2. 🔮 LOSSLESS PNG - Super high-quality with zero compression (big files)")
        print("3. 🖼️ OPTIMIZED JPG - Balanced quality and file size (smaller files)")
        quality_choice = input("Choose your quality setting (1-3): ").strip()

        dpi = 300  # Default DPI

        if quality_choice == "1":
            # Original quality - use higher DPI and PNG
            img_format = "PNG"
            file_ext = "png"
            dpi = 600  # Higher DPI for better quality
            quality = None
            print("💎 Using ORIGINAL quality - prepare for some thicc files")
        elif quality_choice == "2":
            # Lossless PNG
            img_format = "PNG"
            file_ext = "png"
            quality = None
            print("🔮 Using LOSSLESS PNG - still big but slightly optimized")
        else:
            # JPEG with quality setting
            img_format = "JPEG"
            file_ext = "jpg"
            quality = int(input("Enter JPEG quality (1-100, 100 for highest quality): ").strip() or "95")
            quality = max(1, min(100, quality))  # Ensure it's between 1-100
            print(f"🖼️ Using OPTIMIZED JPEG with quality level: {quality}")

        # Output directory
        output_dir = os.path.dirname(pdf_path)
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]

        page_indices = []

        # Process the input
        if '-' in range_input and ',' not in range_input:  # Range like 1-5
            start, end = map(int, range_input.split('-'))
            if start < 1 or end > total_pages or start > end:
                print(f"Invalid range. Must be between 1 and {total_pages}.")
                return
            page_indices = list(range(start-1, end))

        elif ',' in range_input:  # Specific pages like 1,3,5
            page_numbers = [int(p.strip()) for p in range_input.split(',')]

            # Validate page numbers
            if any(p < 1 or p > total_pages for p in page_numbers):
                print(f"Invalid page number. Must be between 1 and {total_pages}.")
                return
            page_indices = [p-1 for p in page_numbers]

        else:  # Single page
            try:
                page_num = int(range_input)
                if page_num < 1 or page_num > total_pages:
                    print(f"Invalid page number. Must be between 1 and {total_pages}.")
                    return
                page_indices = [page_num-1]

            except ValueError:
                print("Invalid input. Please follow the format instructions.")
                return

        # Extract and save images
        print(f"Extracting {len(page_indices)} pages as {img_format} images...")

        images_count = 0
        for i, page_idx in enumerate(page_indices):
            print(f"Processing page {page_idx+1}")

            # Create a temporary PDF with just this page
            temp_writer = PdfWriter()
            temp_writer.add_page(reader.pages[page_idx])

            # Save to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                temp_writer.write(tmp)
                tmp_path = tmp.name

            # Convert to image using appropriate method based on quality choice
            try:
                if quality_choice == "1":
                    # Try to use PyMuPDF first for original quality
                    try:
                        import fitz  # PyMuPDF
                        pdf_document = fitz.open(tmp_path)
                        page = pdf_document.load_page(0)  # Just one page in temp file

                        # Use high resolution for best quality
                        zoom = 4.0  # Higher zoom for better quality
                        mat = fitz.Matrix(zoom, zoom)
                        pix = page.get_pixmap(matrix=mat, alpha=False)

                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        images = [img]
                        pdf_document.close()
                    except ImportError:
                        # Fall back to pdf2image with high DPI
                        from pdf2image import convert_from_path
                        images = convert_from_path(tmp_path, dpi=600)  # High DPI for quality
                else:
                    # Use regular conversion with specified parameters
                    images = convert_pdf_to_images(tmp_path, dpi)

                if images:
                    print(f"📸 Found {len(images)} image(s) on page {page_idx + 1}")

                    # Save each image with appropriate format and settings
                    for j, img in enumerate(images):
                        output_path = os.path.join(output_dir, f"{base_name}_page_{page_idx+1}_{j+1}.{file_ext}")

                        if img_format == "JPEG":
                            # Use optimize=True for better JPEG compression
                            img.save(output_path, img_format, quality=quality, optimize=True)
                        else:
                            # For PNG, use compression level 6 (moderate) for better balance
                            img.save(output_path, img_format, compress_level=6)

                        print(f"🖼️ Extracted & saved: {output_path}")
                        images_count += 1
                else:
                    print("😤 No images found. Just pure text boredom in that file.")

            except Exception as e:
                print(f"🪦 Image extraction face-planted: {e}")

            # Remove temporary file
            os.unlink(tmp_path)

        if images_count > 0:
            elapsed_time = time.time() - start_time

            print("\n✅ IMAGE EXTRACTION SUMMARY:")
            print(f"  • Original PDF: {total_pages} pages")
            print(f"  • Pages processed: {len(page_indices)}")
            print(f"  • Images extracted: {images_count}")
            print(f"  • Format: {img_format}")
            if quality_choice == "3":  # Only for JPEG
                print(f"  • Quality setting: {quality}/100")
            print(f"  • Processing time: {elapsed_time:.1f} seconds")
            print(f"🍓 Mission complete! {images_count} {img_format} image(s) ripped and stored in: {output_dir}")
            return output_dir
        else:
            print("😤 No images found in the selected pages. This PDF is boring AF.")
            return None

    except Exception as e:
        print(f"🪦 Image extraction face-planted: {e}")
        return None

def convert_pdf_to_images(pdf_path, dpi=300):
    """Convert PDF to images using Pillow and PyMuPDF."""
    try:
        import fitz  # PyMuPDF
        images = []
        pdf_document = fitz.open(pdf_path)

        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            # Use matrix for better quality control
            zoom = dpi / 72  # Standard PDF point is 1/72 inch
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)

        pdf_document.close()
        return images

    except ImportError:
        print("PyMuPDF (fitz) not installed. Using alternative method.")
        try:
            from pdf2image import convert_from_path
            return convert_from_path(pdf_path, dpi=dpi)
        except ImportError:
            print("pdf2image not installed. Please install either PyMuPDF or pdf2image.")
            return []

def merge_pdfs(initial_pdf_path=None):
    """Merge multiple PDFs while preserving content types."""
    print("\n🧩 PDF MERGER - Combine your PDFs like a digital Frankenstein 🧠⚡")

    # Record start time
    start_time = time.time()

    # Check if we already have an initial PDF path
    if initial_pdf_path and os.path.isfile(initial_pdf_path):
        print(f"✅ Main PDF ready to merge: {initial_pdf_path}")
        main_pdf_path = initial_pdf_path
        pdf_paths = [main_pdf_path]
    else:
        # If no initial PDF provided, ask for all PDFs
        print("📝 Enter ALL PDF paths separated by spaces, each in quotes (e.g., \"path1\" \"path2\" \"path3\")")
        print("👇 First PDF will be at the top, followed by others in the order listed")

        pdf_paths_input = input('PDF paths (each in quotes, separated by spaces): ').strip()

        if not pdf_paths_input:
            print("❌ No PDFs specified. Merge operation cancelled.")
            return None

        # Extract quoted paths (handles both single and double quotes)
        matches = re.findall(r'"([^"]+)"|\'([^\']+)\'', pdf_paths_input)
        pdf_paths = [m[0] or m[1] for m in matches]

        # Process the input to get all PDF paths
        for pdf_path in pdf_paths:
            pdf_path = pdf_path.strip()

            # Skip empty paths
            if not pdf_path:
                continue

            # Handle paths with quotes
            if (pdf_path.startswith('"') and pdf_path.endswith('"')) or (pdf_path.startswith("'") and pdf_path.endswith("'")):
                pdf_path = pdf_path[1:-1]

            # Handle escaped spaces
            pdf_path = pdf_path.replace("\\ ", " ")

            if not os.path.isfile(pdf_path):
                print(f"❌ File not found: {pdf_path}")
                continue

            if not pdf_path.lower().endswith('.pdf'):
                print(f"🚫 Not a PDF: {pdf_path}")
                continue

            # Skip duplicates
            if pdf_path in pdf_paths:
                print(f"⚠️ Skipping duplicate PDF: {pdf_path}")
                continue

            pdf_paths.append(pdf_path)
            print(f"✅ PDF ready to merge: {pdf_path}")

        if not pdf_paths:
            print("❌ No valid PDFs found. Merge operation cancelled.")
            return None

        # First PDF becomes the main one
        main_pdf_path = pdf_paths[0]

    # Now, get the PDFs to add (if we have an initial PDF)
    if initial_pdf_path and os.path.isfile(initial_pdf_path):
        # Ask for additional PDFs to merge with the initial PDF
        print("\n📚 Enter PDFs to merge with your main PDF")
        print("📝 Enter paths separated by commas (they'll be added in the order you list them)")
        print("👇 Main PDF will be first, followed by these in order")

        additional_pdfs_input = input("Additional PDF paths: ").strip()

        if not additional_pdfs_input:
            print("❌ No additional PDFs specified. Merge operation cancelled.")
            return None

        # Process additional PDFs
        for path in additional_pdfs_input.split(','):
            pdf_path = path.strip()

            # Skip empty paths
            if not pdf_path:
                continue

            # Handle paths with quotes
            if (pdf_path.startswith('"') and pdf_path.endswith('"')) or (pdf_path.startswith("'") and pdf_path.endswith("'")):
                pdf_path = pdf_path[1:-1]

            # Handle escaped spaces
            pdf_path = pdf_path.replace("\\ ", " ")

            if not os.path.isfile(pdf_path):
                print(f"❌ File not found: {pdf_path}")
                continue

            if not pdf_path.lower().endswith('.pdf'):
                print(f"🚫 Not a PDF: {pdf_path}")
                continue

            # Skip duplicates and the main PDF
            if pdf_path in pdf_paths or os.path.abspath(pdf_path) == os.path.abspath(main_pdf_path):
                print(f"⚠️ Skipping duplicate PDF: {pdf_path}")
                continue

            pdf_paths.append(pdf_path)
            print(f"✅ PDF ready to merge: {pdf_path}")

    if len(pdf_paths) < 2:
        print("❌ Need at least 2 PDFs to merge. Operation cancelled.")
        return None

    # Create the output path
    output_dir = os.path.dirname(main_pdf_path)
    base_name = os.path.splitext(os.path.basename(main_pdf_path))[0]
    output_path = os.path.join(output_dir, f"{base_name}_merged.pdf")

    # Get total file sizes and page counts for summary
    total_original_size = sum(os.path.getsize(pdf) for pdf in pdf_paths)
    total_pages = 0

    try:
        # First, determine if we can use PyMuPDF or need to fall back to PyPDF2
        try:
            import fitz  # PyMuPDF
            print("🔄 Using PyMuPDF for high-quality merging...")

            # Prepare to track all PDFs to be merged
            pdf_info = []

            # Get page counts for all PDFs
            for pdf_path in pdf_paths:
                try:
                    # Get info about this PDF
                    doc = fitz.open(pdf_path)
                    file_size = os.path.getsize(pdf_path)
                    page_count = len(doc)
                    doc.close()

                    # Add to tracking
                    pdf_info.append({"path": pdf_path, "pages": page_count, "size": file_size})
                    total_pages += page_count

                except Exception as e:
                    print(f"⚠️ Error analyzing {pdf_path}: {e}")

            # Now perform the actual merge
            merged_doc = fitz.open()

            # Add each PDF in order
            for i, pdf_path in enumerate(pdf_paths):
                print(f"📄 Adding {pdf_info[i]['pages']} pages from {os.path.basename(pdf_path)}...")
                try:
                    doc = fitz.open(pdf_path)
                    merged_doc.insert_pdf(doc)
                    doc.close()
                except Exception as e:
                    print(f"⚠️ Error merging {pdf_path}: {e}")

            # Save the merged PDF
            print("💾 Saving merged PDF...")
            merged_doc.save(output_path, garbage=4, deflate=True, clean=True)
            merged_doc.close()

        except ImportError:
            # Fall back to PyPDF2
            print("🔄 Using PyPDF2 for merging...")

            # Create a writer object
            writer = PdfWriter()

            # Track PDFs being merged
            pdf_info = []

            # Add pages from each PDF in order
            for pdf_path in pdf_paths:
                try:
                    reader = PdfReader(pdf_path)
                    file_size = os.path.getsize(pdf_path)
                    page_count = len(reader.pages)

                    pdf_info.append({"path": pdf_path, "pages": page_count, "size": file_size})
                    total_pages += page_count

                    print(f"📄 Adding {page_count} pages from {os.path.basename(pdf_path)}...")
                    for page in reader.pages:
                        writer.add_page(page)

                except Exception as e:
                    print(f"⚠️ Error merging {pdf_path}: {e}")

            # Save the merged PDF
            print("💾 Saving merged PDF...")
            with open(output_path, 'wb') as f_out:
                writer.write(f_out)

        # Get the final file size
        new_size = os.path.getsize(output_path)
        elapsed_time = time.time() - start_time

        # Calculate size in appropriate units (KB/MB)
        def format_size(size_in_bytes):
            if size_in_bytes < 1024 * 1024:  # Less than 1MB
                return f"{size_in_bytes / 1024:.1f} KB"
            else:
                return f"{size_in_bytes / (1024 * 1024):.2f} MB"

        original_size_formatted = format_size(total_original_size)
        new_size_formatted = format_size(new_size)

        # Generate summary
        print("\n✅ PDF MERGER SUMMARY:")
        print(f"  • PDFs merged: {len(pdf_info)}")
        print(f"  • Total pages: {total_pages}")
        print(f"  • Original files total size: {original_size_formatted}")
        print(f"  • Merged file size: {new_size_formatted}")
        print(f"  • Processing time: {elapsed_time:.1f} seconds")

        # List all PDFs that were merged
        print("\n📚 FILES MERGED:")
        for i, pdf in enumerate(pdf_info, 1):
            if i == 1:
                print(f"  {i}. 📄 {os.path.basename(pdf['path'])} (TOP - {pdf['pages']} pages)")
            else:
                print(f"  {i}. 📄 {os.path.basename(pdf['path'])} ({pdf['pages']} pages)")

        print(f"\n🧩 Merged PDF saved as: {output_path}")
        return output_path

    except Exception as e:
        print(f"🤕 PDF merging failed: {e}")
        return None

def predator_main():
    print("=== 🔥 PDF BEAST 🔥 - The Ultimate PDF Slayer ===")

    # Get PDF path
    pdf_path = get_pdf_path()

    while True:
        # Display menu
        print("\nChoose your weapon:")
        print("1. 🗜️  Compress PDF - Image-based compression (max shrinkage)")
        print("2. 📝  Compress PDF - Text-preserving compression (keeps text selectable)")
        print("3. ✂️  Split PDF - Cut it like it owes you money")
        print("4. 🖼️  Extract Images - Rip those pretty pictures")
        print("5. 🧩  Merge PDFs - Franken-stitch multiple PDFs")
        print("6. 🚪 Return to Main Menu")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            compress_pdf(pdf_path)
        elif choice == "2":
            compress_pdf_text(pdf_path)
        elif choice == "3":
            split_pdf(pdf_path)
        elif choice == "4":
            extract_images(pdf_path)
        elif choice == "5":
            merge_pdfs(pdf_path)  # Pass the initial PDF path
        elif choice == "6":
            print("🏃 Exiting PDF Beast.")
            break
        else:
            print("🤦‍♂️ Are you serious? Choose between 1-6... is that so hard?")


# ==========================================
# 🛑 MAIN MASTER MENU
# ==========================================

if __name__ == "__main__":
    while True:
        print("\n=======================================================")
        print("👑 GOD-TIER PDF TOOLKIT - Choose your weapon")
        print("=======================================================")
        print("1. 📸 IMG2PDF (Images to PDF Converter)")
        print("2. 🔥 PDF PREDATOR (Compress, Split, Extract, Merge)")
        print("3. 🚪 Exit")

        main_choice = input("\nEnter your choice (1-3): ")

        if main_choice == "1":
            convert_images_to_pdf(None)
        elif main_choice == "2":
            predator_main()
        elif main_choice == "3":
            print("👋 Catch you later. Stay nerdy.")
            sys.exit(0)
        else:
            print("🤡 Invalid choice. Even a potato knows to type 1, 2, or 3.")
