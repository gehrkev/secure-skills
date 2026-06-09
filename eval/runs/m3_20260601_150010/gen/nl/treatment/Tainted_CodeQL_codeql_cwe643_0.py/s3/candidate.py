from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xpath', methods=['GET', 'POST'])
def xpath_query():
    try:
        # Get parameters from query string or form data
        xml_src = request.args.get('xml_src') or request.form.get('xml_src')
        xpath = request.args.get('xpath') or request.form.get('xpath')

        # Validate that both parameters are provided
        if not xml_src or not xpath:
            return jsonify({'error': 'Missing xml_src or xpath parameter'}), 400

        # Parse XML securely - disable external entity processing to prevent XXE
        parser = etree.XMLParser(
            remove_blank_text=True,
            resolve_entities=False,
            remove_comments=True
        )

        try:
            root = etree.fromstring(xml_src.encode('utf-8'), parser)
        except etree.XMLSyntaxError as e:
            return jsonify({'error': f'Invalid XML: {str(e)}'}), 400

        # Execute XPath query
        try:
            results = root.xpath(xpath)
        except etree.XPathError as e:
            return jsonify({'error': f'Invalid XPath: {str(e)}'}), 400

        # Convert results to JSON-serializable format
        output = []
        for result in results:
            if isinstance(result, (str, int, float, bool)):
                output.append(result)
            else:
                # For XML elements, convert to string representation
                output.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': output})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)
