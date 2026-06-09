from flask import Flask, request

try:
    from defusedxml.ElementTree import fromstring as safe_fromstring
except ImportError:
    from xml.etree.ElementTree import fromstring as safe_fromstring

import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse-xml', methods=['GET', 'POST'])
def parse_xml():
    # Retrieve XML data from 'xml_src' request parameter
    xml_data = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_data:
        return 'xml_src parameter is required', 400

    try:
        # Parse XML safely - defusedxml prevents XXE attacks
        root = safe_fromstring(xml_data)
        # Return as string
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError as e:
        return f'Invalid XML: {str(e)}', 400

if __name__ == '__main__':
    app.run()
