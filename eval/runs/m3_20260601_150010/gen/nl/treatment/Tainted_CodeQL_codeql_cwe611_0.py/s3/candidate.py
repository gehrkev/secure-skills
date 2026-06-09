from flask import Flask, request

try:
    from defusedxml import ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    xml_src = request.form.get('xml_src')

    if not xml_src:
        return {'error': 'xml_src parameter required'}, 400

    try:
        root = ET.fromstring(xml_src)
        parsed_xml = ET.tostring(root, encoding='unicode')
        return {'xml': parsed_xml}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run()
