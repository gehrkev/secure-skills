from lxml import etree

def parse_xml_file(file_path):
    parser = etree.XMLParser(resolve_entities=False, no_network=True)
    tree = etree.parse(file_path, parser)
    return tree.getroot()
