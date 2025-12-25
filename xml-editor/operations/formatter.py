# app/formatter.py
from lxml import etree

def format_xml(input_path, output_path=None):
    """
    Prettify (format) the XML file:
    - Adds proper indentation
    - Keeps it readable
    - Saves to output_path if provided, otherwise overwrites input
    """

    try:
        # Parse XML
        tree = etree.parse(input_path)

        # Convert tree back to string with pretty print
        pretty_xml = etree.tostring(tree, pretty_print=True, encoding="unicode")

        # Determine where to save
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(pretty_xml)
            print(f"Formatted XML saved to {output_path}")
        else:
            # Overwrite input file if no output provided
            with open(input_path, "w", encoding="utf-8") as f:
                f.write(pretty_xml)
            print(f"Formatted XML overwritten: {input_path}")

    except etree.XMLSyntaxError as e:
        print("Failed to format XML: Syntax error found.")
        for err in e.error_log:
            print(f"Line {err.line}: {err.message}")
