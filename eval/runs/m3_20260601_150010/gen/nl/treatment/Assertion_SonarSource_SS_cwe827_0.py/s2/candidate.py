from lxml import etree
import os


def parse_xml_file(file_path):
    """
    Parse an XML file from a given file path and return the root element.

    Args:
        file_path: Path to the XML file to parse

    Returns:
        The root element of the parsed XML document

    Raises:
        FileNotFoundError: If the file does not exist
        etree.XMLSyntaxError: If the XML is malformed
    """
    # Validate the file path exists and is a file
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a parser with security settings to prevent XXE and XML expansion attacks
    parser = etree.XMLParser(
        resolve_entities=False,  # Disable external entity resolution (CWE-611)
        no_network=True,         # Prevent network access during parsing
        load_external_dtd=False  # Don't load external DTDs (CWE-776)
    )

    # Parse the XML file
    tree = etree.parse(file_path, parser)

    # Return the root element
    return tree.getroot()
