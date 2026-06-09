from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/xslt', methods=['GET', 'POST'])
def xslt_endpoint():
    try:
        # Get parameters from request
        xml_data = request.form.get('xml') or request.args.get('xml')
        xpath_query = request.form.get('xslt') or request.args.get('xslt')

        # Validate inputs
        if not xml_data:
            return jsonify({'error': 'Missing xml parameter'}), 400
        if not xpath_query:
            return jsonify({'error': 'Missing xslt parameter'}), 400

        # Parse XML safely
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as e:
            return jsonify({'error': f'Invalid XML: {str(e)}'}), 400

        # Apply XPath query
        try:
            results = root.findall(xpath_query)
        except Exception as e:
            return jsonify({'error': f'Invalid XPath query: {str(e)}'}), 400

        # Format results
        result_list = []
        for elem in results:
            if elem.text:
                result_list.append(elem.text)
            else:
                result_list.append(ET.tostring(elem, encoding='unicode'))

        return jsonify({
            'results': result_list,
            'count': len(result_list)
        })

    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
