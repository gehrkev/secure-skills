from flask import Flask, request

app = Flask(__name__)

try:
    from defusedxml import ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return 'Error: xml_src parameter is required', 400

    try:
        root = ET.fromstring(xml_src)
        import xml.etree.ElementTree as standard_ET
        result = standard_ET.tostring(root, encoding='unicode')
        return result, 200, {'Content-Type': 'application/xml'}
    except ET.ParseError as e:
        return f'Error: Invalid XML - {str(e)}', 400

if __name__ == '__main__':
    app.run()
