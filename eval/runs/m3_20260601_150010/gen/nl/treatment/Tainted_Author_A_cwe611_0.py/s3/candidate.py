from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return jsonify({'error': 'Missing xml_src parameter'}), 400

    try:
        # Parse XML with XXE protection by disabling external entity resolution
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)

        # Convert parsed XML back to string
        parsed_xml = etree.tostring(root, encoding='unicode', pretty_print=True)

        return jsonify({'parsed_xml': parsed_xml}), 200
    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error parsing XML: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
