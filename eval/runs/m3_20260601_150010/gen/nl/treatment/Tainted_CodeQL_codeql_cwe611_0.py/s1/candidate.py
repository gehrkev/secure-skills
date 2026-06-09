from flask import Flask, request
from defusedxml import ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_src = request.form.get('xml_src', '')

    if not xml_src:
        return 'No xml_src provided', 400

    try:
        root = ET.fromstring(xml_src)
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError as e:
        return f'XML parse error: {str(e)}', 400

if __name__ == '__main__':
    app.run(debug=True)
