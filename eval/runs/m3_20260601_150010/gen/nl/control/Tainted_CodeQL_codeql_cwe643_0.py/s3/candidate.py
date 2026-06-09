from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)


@app.route('/xpath', methods=['GET', 'POST'])
def xpath_query():
    """
    Endpoint that accepts xml_src and xpath parameters,
    parses the XML, executes the XPath query, and returns results.
    """
    # Get parameters from request (support both query string and form data)
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')
    xpath = request.args.get('xpath') or request.form.get('xpath')

    # Validate inputs
    if not xml_src:
        return jsonify({'error': 'xml_src parameter is required'}), 400
    if not xpath:
        return jsonify({'error': 'xpath parameter is required'}), 400

    try:
        # Parse the XML
        root = etree.fromstring(xml_src.encode('utf-8'))

        # Execute the XPath query
        results = root.xpath(xpath)

        # Convert results to a serializable format
        formatted_results = []
        for result in results:
            if isinstance(result, str):
                formatted_results.append(result)
            elif isinstance(result, bool):
                formatted_results.append(result)
            elif isinstance(result, (int, float)):
                formatted_results.append(result)
            else:
                # For elements, return their string representation
                formatted_results.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': formatted_results}), 200

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except etree.XPathError as e:
        return jsonify({'error': f'Invalid XPath: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
