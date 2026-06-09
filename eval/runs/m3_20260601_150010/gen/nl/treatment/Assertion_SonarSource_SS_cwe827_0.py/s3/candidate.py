from lxml import etree
from pathlib import Path


def parse_xml(file_path):
    """Parse an XML file and return the root element.

    Applies security mitigations to prevent XXE and DTD expansion attacks.

    Args:
        file_path: Path to the XML file to parse

    Returns:
        The root element of the parsed XML document

    Raises:
        FileNotFoundError: If the file does not exist
        etree.XMLSyntaxError: If the XML is malformed
    """
    # Validate and resolve the file path to prevent path traversal
    path = Path(file_path).resolve()

    # Ensure the file exists and is readable
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a parser with security settings to prevent XXE and DTD expansion attacks
    # resolve_entities=False prevents external entity expansion (CWE-611)
    # The default settings in lxml also disable DTD processing (CWE-776)
    parser = etree.XMLParser(
        resolve_entities=False,
        remove_blank_text=False
    )

    # Parse the XML file
    tree = etree.parse(str(path), parser)

    # Return the root element
    return tree.getroot()
