from flask import Flask, request
from xml.etree import ElementTree as ET

app = Flask(__name__)

@app.route('/parse-xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return "No xml_src parameter provided", 400

    try:
        root = ET.fromstring(xml_src)
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError as e:
        return f"Invalid XML: {str(e)}", 400

if __name__ == '__main__':
    app.run()
