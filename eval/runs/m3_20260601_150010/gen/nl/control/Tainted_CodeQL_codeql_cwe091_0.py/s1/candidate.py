from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xslt', methods=['GET', 'POST'])
def xslt_endpoint():
    xml_data = request.args.get('xml') or request.form.get('xml')
    xpath_query = request.args.get('xslt') or request.form.get('xslt')

    if not xml_data or not xpath_query:
        return jsonify({'error': 'Missing xml or xslt parameters'}), 400

    try:
        root = etree.fromstring(xml_data.encode('utf-8'))
        results = root.xpath(xpath_query)

        output = []
        for result in results:
            if isinstance(result, (str, bool, int, float)):
                output.append(result)
            else:
                output.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': output})

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
