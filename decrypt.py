import os
import ocrmypdf
import tempfile
import argparse
import subprocess

from pdfrw import PdfReader, PdfWriter, PdfReader

from fingerprint import fingerprint


def copy_pdf_id(src, target):
    """
        Copies the PDF is from src to target. Both
        arguments are given as a file path
    """
    src_trailer = PdfReader(src)
    
    target_trailer = PdfReader(target)
    target_trailer.ID = src_trailer.ID

    PdfWriter(target, trailer=target_trailer).write()


parser = argparse.ArgumentParser(description="Decrypts a PDF file")

parser.add_argument("--input", type=str, required=True, help="PDF input file")
parser.add_argument("--output", type=str, required=True, help="PDF output file")
parser.add_argument("--ocr-language", type=str, required=True, help="OCR language")
parser.add_argument("--copy-pdf-id", type=str, required=False, default="y", help="Wether the PDF ID should be preserved")

args = parser.parse_args()
args.copy_pdf_id = args.copy_pdf_id == "y"

tempdir_path = tempfile.mkdtemp()

# Rasterize the PDF to images
process = subprocess.Popen([
    "pdftoppm",
    args.input,
    os.path.join(tempdir_path, "raster"),
    "-png"
])

process.communicate()

# Convert the images to a PDF using tesseract
raster_filenames = sorted(os.listdir(tempdir_path))
raster_filenames = [os.path.join(tempdir_path, fn) for fn in raster_filenames]
raster_filenames = "\n".join(raster_filenames)

# Write the source files to a text file (for the tesseract command)
temp_raster_list = tempfile.NamedTemporaryFile(delete=False)
temp_raster_list.write(str.encode(raster_filenames))
temp_raster_list.flush()

# Rebuild a rasterized PDF file
raster_pdf_path = os.path.join(tempdir_path, "rasterized")

process = subprocess.Popen([
    "tesseract",
    temp_raster_list.name,
    raster_pdf_path,
    "pdf"
])

# Necessary fix to adapt for the tesseract output filename
raster_pdf_path = f"{raster_pdf_path}.pdf"

process.communicate()

# Apply OCR with the given language
ocrmypdf.ocr(
    raster_pdf_path,
    args.output,
    redo_ocr=True,
    language=args.ocr_language)

# Make sure the decrypted PDF has the same ID as the encrypted version
# for compatibility with Hypothes.is annotations
if args.copy_pdf_id:
    copy_pdf_id(args.input, args.output)
