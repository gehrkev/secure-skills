from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET'])
def parse_xml():
    xml_src = request.args.get('xml_src', '')

    if not xml_src:
        return 'No XML source provided', 400

    try:
        # Use defusedxml if available for XXE protection, fallback to standard parser
        try:
            from defusedxml import ElementTree as DefusedET
            root = DefusedET.fromstring(xml_src)
        except ImportError:
            root = ET.fromstring(xml_src)

        # Return parsed XML as string
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError as e:
        return f'XML parsing error: {str(e)}', 400

if __name__ == '__main__':
    app.run()
