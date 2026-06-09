from flask import Flask, request
from xml.etree import ElementTree as ET

app = Flask(__name__)

@app.route('/parse-xml', methods=['GET'])
def parse_xml():
    xml_src = request.args.get('xml_src', '')

    if not xml_src:
        return "No XML data provided", 400

    try:
        root = ET.fromstring(xml_src)
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError:
        return "Invalid XML", 400

if __name__ == '__main__':
    app.run()
