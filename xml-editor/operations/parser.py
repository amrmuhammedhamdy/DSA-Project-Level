from lxml import etree

def verify(input_path, output_path=None):
    try:
        etree.parse(input_path)
        print("XML is valid.")
        if output_path:
            with open(input_path, 'r') as src, open(output_path, 'w') as dst:
                dst.write(src.read())
    except etree.XMLSyntaxError as e:
        print("XML is invalid.")
        for err in e.error_log:
            print(f"Line {err.line}: {err.message}")
        if output_path:
            fix_xml_with_recovery(input_path, output_path)
            print(f"Fixed XML saved to {output_path}")

def fix_xml_with_recovery(input_path, output_path):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(input_path, parser)
    fixed = etree.tostring(tree, pretty_print=True, encoding="unicode")
    with open(output_path, "w") as f:
        f.write(fixed)
