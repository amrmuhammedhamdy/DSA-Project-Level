# app/compressor.py
from lxml import etree
import gzip

def compress(input_path, output_path):
    """
    Compress an XML or JSON file into a .gz file using gzip.
    """
    try:
        with open(input_path, "rb") as f_in, gzip.open(output_path, "wb") as f_out:
            f_out.writelines(f_in)
        print(f"Compressed file saved to {output_path}")
    except Exception as e:
        print(f"Failed to compress file: {e}")

