from lxml import etree

def parse_xml(file_path):
    """Parse an XML file from a given file path and return the root element."""
    tree = etree.parse(file_path)
    return tree.getroot()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        root = parse_xml(sys.argv[1])
        print(f"Root element: {root.tag}")
    else:
        print("Usage: python candidate.py <file_path>")
