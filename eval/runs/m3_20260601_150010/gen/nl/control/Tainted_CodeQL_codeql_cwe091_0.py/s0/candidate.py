from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)


@app.route('/xslt', methods=['GET', 'POST'])
def xslt_endpoint():
    try:
        # Get parameters from request (support both GET and POST)
        xml_str = request.args.get('xml') or request.form.get('xml')
        xpath_query = request.args.get('xslt') or request.form.get('xslt')

        if not xml_str:
            return jsonify({'error': 'Missing xml parameter'}), 400
        if not xpath_query:
            return jsonify({'error': 'Missing xslt parameter'}), 400

        # Parse XML
        root = etree.fromstring(xml_str.encode('utf-8'))

        # Apply XPath query
        results = root.xpath(xpath_query)

        # Convert results to a serializable format
        result_list = []
        for result in results:
            if isinstance(result, str):
                result_list.append(result)
            elif isinstance(result, (int, float, bool)):
                result_list.append(result)
            else:
                # Element node - serialize to string
                result_list.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': result_list})

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
