from lxml import etree
from pathlib import Path


def parse_xml(file_path):
    file_path = Path(file_path).resolve()

    if not file_path.exists() or not file_path.is_file():
        raise ValueError(f"Invalid file path: {file_path}")

    parser = etree.XMLParser(
        resolve_entities=False,
        no_network=True
    )

    tree = etree.parse(str(file_path), parser)
    return tree.getroot()
