from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xpath', methods=['GET', 'POST'])
def execute_xpath():
    # Get parameters - check query params first, then form data, then JSON
    xml_src = request.args.get('xml_src')
    xpath_query = request.args.get('xpath')

    if not xml_src or not xpath_query:
        if request.is_json:
            data = request.get_json()
            xml_src = xml_src or data.get('xml_src')
            xpath_query = xpath_query or data.get('xpath')
        elif request.form:
            xml_src = xml_src or request.form.get('xml_src')
            xpath_query = xpath_query or request.form.get('xpath')

    if not xml_src or not xpath_query:
        return jsonify({'error': 'Missing xml_src or xpath parameter'}), 400

    try:
        # Parse XML
        root = etree.fromstring(xml_src.encode('utf-8'))

        # Execute XPath query
        results = root.xpath(xpath_query)

        # Convert results to JSON-serializable format
        serialized_results = []
        for result in results:
            if isinstance(result, str):
                serialized_results.append(result)
            elif isinstance(result, bool):
                serialized_results.append(result)
            elif isinstance(result, (int, float)):
                serialized_results.append(result)
            else:
                # For element nodes, serialize to string
                serialized_results.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': serialized_results})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
