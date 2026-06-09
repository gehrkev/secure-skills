from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xpath', methods=['GET', 'POST'])
def execute_xpath():
    try:
        # Get parameters from request
        xml_src = request.args.get('xml_src') or request.form.get('xml_src')
        xpath = request.args.get('xpath') or request.form.get('xpath')

        if not xml_src or not xpath:
            return jsonify({'error': 'Missing xml_src or xpath parameter'}), 400

        # Parse XML and execute XPath query
        root = etree.fromstring(xml_src.encode('utf-8'))
        results = root.xpath(xpath)

        # Convert results to JSON-serializable format
        serialized = []
        for result in results:
            if isinstance(result, str):
                serialized.append(result)
            elif isinstance(result, bool):
                serialized.append(result)
            elif isinstance(result, (int, float)):
                serialized.append(result)
            else:
                # Element object
                serialized.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': serialized})

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
