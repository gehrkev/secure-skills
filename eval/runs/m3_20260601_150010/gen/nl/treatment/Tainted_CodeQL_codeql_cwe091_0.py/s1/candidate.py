from flask import Flask, request, jsonify
from defusedxml import ElementTree as ET

app = Flask(__name__)

@app.route('/xslt', methods=['POST'])
def xslt_endpoint():
    try:
        xml_data = request.form.get('xml')
        xpath_query = request.form.get('xslt')

        if not xml_data:
            return jsonify({'error': 'Missing xml parameter'}), 400
        if not xpath_query:
            return jsonify({'error': 'Missing xslt parameter'}), 400

        root = ET.fromstring(xml_data)
        results = root.findall(xpath_query)

        result_list = []
        for elem in results:
            result_list.append(ET.tostring(elem, encoding='unicode'))

        return jsonify({'results': result_list}), 200

    except ET.ParseError as e:
        return jsonify({'error': f'XML parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()
