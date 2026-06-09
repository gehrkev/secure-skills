from lxml import etree
from pathlib import Path


def parse_xml_file(file_path):
    """
    Parse an XML file from a given file path and return the root element.

    Args:
        file_path: Path to the XML file

    Returns:
        The root element of the parsed XML file
    """
    file_path = Path(file_path).resolve()

    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True
    )

    tree = etree.parse(str(file_path), parser)

    return tree.getroot()
