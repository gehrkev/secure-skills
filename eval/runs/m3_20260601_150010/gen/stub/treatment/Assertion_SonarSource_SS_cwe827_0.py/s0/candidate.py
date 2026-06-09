from lxml import etree


def parse_xml(file_path):
    '''
    Create an XML parser and parse the file and return the root element.
    @param file_path: The path to the XML file to be parsed.
    @return: The root element of the XML file.
    '''
    # Create a secure XML parser to prevent XXE attacks
    # Disable external entity resolution and DTD processing
    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        load_dtd=False,
        remove_blank_text=False
    )

    # Parse the XML file and return the root element
    tree = etree.parse(file_path, parser)
    return tree.getroot()
