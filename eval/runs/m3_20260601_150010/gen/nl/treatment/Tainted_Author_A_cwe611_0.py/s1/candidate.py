from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return jsonify({'error': 'xml_src parameter is required'}), 400

    try:
        parser = etree.XMLParser(
            resolve_entities=False,
            remove_blank_text=True,
            remove_comments=True,
            strip_cdata=False
        )
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        parsed_xml = etree.tostring(root, encoding='unicode', pretty_print=True)
        return jsonify({'parsed_xml': parsed_xml}), 200
    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
