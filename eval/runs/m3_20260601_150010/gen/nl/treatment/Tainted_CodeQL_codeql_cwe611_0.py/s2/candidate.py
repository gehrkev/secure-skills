from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    try:
        # Get xml_src parameter from request (form data or JSON)
        xml_src = request.form.get('xml_src')
        if not xml_src and request.is_json:
            xml_src = request.json.get('xml_src')

        if not xml_src:
            return jsonify({'error': 'xml_src parameter is required'}), 400

        # Parse XML with external entity expansion disabled
        # ElementTree disables external entity processing by default in Python 3.7+
        # This prevents XXE (XML External Entity) attacks
        root = ET.fromstring(xml_src)

        # Convert parsed XML back to string
        parsed_xml_str = ET.tostring(root, encoding='unicode')

        return jsonify({'parsed_xml': parsed_xml_str})

    except ParseError as e:
        return jsonify({'error': f'XML parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()
