from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xslt', methods=['GET', 'POST'])
def xslt():
    # Retrieve XML and XPath query from request parameters
    xml_content = request.args.get('xml') or request.form.get('xml')
    xpath_query = request.args.get('xslt') or request.form.get('xslt')

    # Validate that both parameters are provided
    if not xml_content or not xpath_query:
        return jsonify({'error': 'Missing xml or xslt parameters'}), 400

    try:
        # Parse the XML
        root = etree.fromstring(xml_content.encode('utf-8'))

        # Apply the XPath query
        results = root.xpath(xpath_query)

        # Convert results to serializable format
        formatted_results = []
        for result in results:
            if isinstance(result, (str, bool, int, float)):
                formatted_results.append(result)
            else:
                # For XML elements, serialize to string
                formatted_results.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': formatted_results})

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'XML parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'XPath evaluation error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
