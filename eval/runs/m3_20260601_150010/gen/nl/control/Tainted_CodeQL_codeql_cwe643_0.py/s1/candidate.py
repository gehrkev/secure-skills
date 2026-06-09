from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xpath', methods=['GET', 'POST'])
def xpath_query():
    try:
        # Get parameters from query string
        xml_src = request.args.get('xml_src')
        xpath = request.args.get('xpath')

        # Also check JSON body for POST requests
        if not xml_src or not xpath:
            if request.is_json:
                data = request.get_json()
                xml_src = xml_src or data.get('xml_src')
                xpath = xpath or data.get('xpath')

        if not xml_src or not xpath:
            return jsonify({'error': 'Missing xml_src or xpath parameter'}), 400

        # Parse XML
        root = etree.fromstring(xml_src.encode('utf-8'))

        # Execute XPath query
        results = root.xpath(xpath)

        # Convert results to serializable format
        output = []
        for result in results:
            if isinstance(result, (str, bool, int, float)):
                output.append(result)
            else:
                # It's an element, convert to string
                output.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': output})

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'XML parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
