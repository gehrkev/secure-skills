from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    try:
        xml_src = request.args.get('xml_src') or request.form.get('xml_src')

        if not xml_src:
            return jsonify({'error': 'xml_src parameter is required'}), 400

        parser = etree.XMLParser(resolve_entities=False, remove_blank_text=True)
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        result = etree.tostring(root, encoding='unicode', pretty_print=True)

        return result, 200, {'Content-Type': 'text/xml'}

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()
