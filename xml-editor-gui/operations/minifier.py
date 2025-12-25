# app/compressor.py
from lxml import etree

def minify(input_path, output_path=None):
    """
    Minify an XML file:
    - Removes all unnecessary whitespace and newlines
    - Saves to output_path if provided, otherwise overwrites input
    """

    try:
        parser = etree.XMLParser(remove_blank_text=True)  # removes extra whitespace nodes
        tree = etree.parse(input_path, parser)

        # Convert tree to string without pretty print
        minified_xml = etree.tostring(tree, encoding="unicode", pretty_print=False)

        # Save to output or overwrite input
        target = output_path if output_path else input_path
        with open(target, "w", encoding="utf-8") as f:
            f.write(minified_xml)

        print(f"Minified XML saved to {target}")

    except etree.XMLSyntaxError as e:
        print("Failed to minify XML: Syntax error found.")
        for err in e.error_log:
            print(f"Line {err.line}: {err.message}")
