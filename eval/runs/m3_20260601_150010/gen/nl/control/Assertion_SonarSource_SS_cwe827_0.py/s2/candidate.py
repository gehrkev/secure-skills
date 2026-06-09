from lxml import etree

def parse_xml(file_path):
    tree = etree.parse(file_path)
    return tree.getroot()
