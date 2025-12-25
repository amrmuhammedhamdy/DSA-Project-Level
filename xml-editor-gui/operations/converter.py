# app/converter.py
import json
from lxml import etree

def xml_to_json(input_path, output_path=None):
    """
    Convert an XML file to JSON.
    Saves to output_path if provided, otherwise prints JSON.
    """

    def etree_to_dict(t):
        """
        Recursively convert an ElementTree to a dict.
        """
        d = {t.tag: {} if t.attrib else None}

        # Process children
        children = list(t)
        if children:
            dd = {}
            for child in children:
                child_dict = etree_to_dict(child)
                for k, v in child_dict.items():
                    # Handle multiple children with same tag
                    if k in dd:
                        if not isinstance(dd[k], list):
                            dd[k] = [dd[k]]
                        dd[k].append(v)
                    else:
                        dd[k] = v
            d = {t.tag: dd}
        else:
            # Leaf node
            d = {t.tag: t.text}

        return d

    try:
        tree = etree.parse(input_path)
        root = tree.getroot()

        data_dict = etree_to_dict(root)
        json_data = json.dumps(data_dict, indent=2)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_data)
            print(f"Converted JSON saved to {output_path}")
        else:
            print(json_data)

    except etree.XMLSyntaxError as e:
        print("Failed to convert XML to JSON: Syntax error found.")
        for err in e.error_log:
            print(f"Line {err.line}: {err.message}")
