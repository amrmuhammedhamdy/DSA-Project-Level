from lxml import etree
import gzip

def decompress(input_path, output_path):
    """
    Decompress a .gz file back to XML/JSON.
    """
    try:
        with gzip.open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
            f_out.write(f_in.read())
        print(f"Decompressed file saved to {output_path}")
    except Exception as e:
        print(f"Failed to decompress file: {e}")