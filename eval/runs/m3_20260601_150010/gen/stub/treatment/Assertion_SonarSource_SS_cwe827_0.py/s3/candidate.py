from lxml import etree


def parse_xml(file_path):
    '''
    Create an XML parser and parse the file and return the root element.
    @param file_path: The path to the XML file to be parsed.
    @return: The root element of the XML file.
    '''
    # Create a secure parser that prevents XXE attacks
    # by disabling external entity resolution
    parser = etree.XMLParser(resolve_entities=False)

    # Parse the XML file and return the root element
    tree = etree.parse(file_path, parser)
    return tree.getroot()
