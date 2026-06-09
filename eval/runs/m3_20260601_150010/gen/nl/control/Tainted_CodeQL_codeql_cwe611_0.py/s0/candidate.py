from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_src = request.form.get('xml_src')
    if not xml_src:
        data = request.get_json(silent=True) or {}
        xml_src = data.get('xml_src')

    root = ET.fromstring(xml_src)
    return ET.tostring(root, encoding='unicode')

if __name__ == '__main__':
    app.run()
