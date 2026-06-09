from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

app = Flask(__name__)

@app.route('/parse_xml', methods=['POST'])
def parse_xml():
    try:
        xml_src = request.form.get('xml_src')

        if not xml_src:
            return jsonify({'error': 'xml_src parameter is required'}), 400

        # Disable external entity expansion to prevent XXE attacks
        parser = ET.XMLParser()
        parser.parser.SetParamEntityParsing(ET.XML_PARAM_ENTITY_PARSING_NEVER)

        root = ET.fromstring(xml_src, parser=parser)
        parsed_xml_string = ET.tostring(root, encoding='unicode')

        return parsed_xml_string, 200, {'Content-Type': 'text/plain; charset=utf-8'}

    except ParseError as e:
        return jsonify({'error': f'XML parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
