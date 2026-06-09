from flask import Flask, request, jsonify
from lxml import etree
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.route('/xpath', methods=['POST', 'GET'])
def xpath_query():
    try:
        # Get parameters from request (check both query and form)
        xml_src = request.args.get('xml_src') or request.form.get('xml_src')
        xpath = request.args.get('xpath') or request.form.get('xpath')

        # Validate inputs
        if not xml_src:
            return jsonify({'error': 'Missing xml_src parameter'}), 400
        if not xpath:
            return jsonify({'error': 'Missing xpath parameter'}), 400

        # Parse XML safely with XXE protection and external entity resolution disabled
        parser = etree.XMLParser(
            resolve_entities=False,
            remove_blank_text=True,
            no_network=True
        )

        try:
            root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        except etree.XMLSyntaxError as e:
            logger.warning(f"Invalid XML provided: {str(e)}")
            return jsonify({'error': 'Invalid XML syntax'}), 400

        # Execute XPath query
        try:
            results = root.xpath(xpath)
        except etree.XPathError as e:
            logger.warning(f"Invalid XPath query: {str(e)}")
            return jsonify({'error': 'Invalid XPath query'}), 400

        # Convert results to JSON-serializable format
        output = []
        for result in results:
            if isinstance(result, str):
                output.append(result)
            elif isinstance(result, (int, float, bool)):
                output.append(result)
            elif isinstance(result, bytes):
                output.append(result.decode('utf-8'))
            elif hasattr(result, 'text') and result.text:
                output.append(result.text)
            else:
                try:
                    output.append(etree.tostring(result, encoding='unicode', method='xml'))
                except:
                    output.append(str(result))

        return jsonify({'results': output}), 200

    except Exception as e:
        logger.error(f"Unexpected error in xpath_query: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=False)
