from flask import Flask, request, jsonify
from lxml import etree
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/query', methods=['POST', 'GET'])
def query_xml():
    try:
        xml_src = request.args.get('xml_src') or request.form.get('xml_src')
        xpath = request.args.get('xpath') or request.form.get('xpath')

        if not xml_src:
            return jsonify({'error': 'Missing xml_src parameter'}), 400
        if not xpath:
            return jsonify({'error': 'Missing xpath parameter'}), 400

        if not isinstance(xpath, str):
            return jsonify({'error': 'xpath must be a string'}), 400

        try:
            root = etree.fromstring(xml_src.encode('utf-8'))
        except etree.XMLSyntaxError as e:
            return jsonify({'error': f'Invalid XML: {str(e)}'}), 400

        try:
            results = root.xpath(xpath)
        except etree.XPathError as e:
            return jsonify({'error': f'Invalid XPath: {str(e)}'}), 400

        output = []
        for result in results:
            if isinstance(result, etree._Element):
                output.append(etree.tostring(result, encoding='unicode'))
            else:
                output.append(result)

        return jsonify({'results': output}), 200

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False)
