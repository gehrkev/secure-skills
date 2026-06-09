from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_src = request.form.get('xml_src')
    if not xml_src and request.is_json:
        xml_src = request.json.get('xml_src')

    root = ET.fromstring(xml_src)
    result = ET.tostring(root, encoding='unicode')

    return result

if __name__ == '__main__':
    app.run()
