from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_src = request.form.get('xml_src')
    if not xml_src:
        json_data = request.get_json(silent=True) or {}
        xml_src = json_data.get('xml_src')

    if not xml_src:
        return "No xml_src provided", 400

    try:
        root = ET.fromstring(xml_src)
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError as e:
        return f"Error parsing XML: {e}", 400

if __name__ == '__main__':
    app.run(debug=True)
