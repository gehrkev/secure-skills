from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return 'Missing xml_src parameter', 400

    try:
        root = ET.fromstring(xml_src)
        return ET.tostring(root, encoding='unicode')
    except ET.ParseError as e:
        return f'Invalid XML: {e}', 400

if __name__ == '__main__':
    app.run(debug=True)
