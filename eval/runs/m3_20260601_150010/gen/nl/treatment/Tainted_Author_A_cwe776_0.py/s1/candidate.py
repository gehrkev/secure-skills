from flask import Flask, request
try:
    import defusedxml.ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse-xml', methods=['GET'])
def parse_xml():
    xml_src = request.args.get('xml_src')

    if not xml_src:
        return 'xml_src parameter required', 400

    try:
        root = ET.fromstring(xml_src)
        return ET.tostring(root, encoding='unicode')
    except ET.ParseError:
        return 'Invalid XML', 400

if __name__ == '__main__':
    app.run()
