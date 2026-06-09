from lxml import etree


def parse_xml(file_path):
    """Parse an XML file and return the root element."""
    tree = etree.parse(file_path)
    return tree.getroot()
