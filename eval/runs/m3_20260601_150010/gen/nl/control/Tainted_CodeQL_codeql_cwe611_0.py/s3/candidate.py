from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_src = None

    # Try form data first
    if request.form:
        xml_src = request.form.get('xml_src')

    # Try JSON
    if not xml_src and request.is_json:
        data = request.get_json() or {}
        xml_src = data.get('xml_src')

    if not xml_src:
        return {'error': 'xml_src parameter is required'}, 400

    try:
        root = ET.fromstring(xml_src)
        parsed_xml = ET.tostring(root, encoding='unicode')
        return parsed_xml
    except ET.ParseError as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)
