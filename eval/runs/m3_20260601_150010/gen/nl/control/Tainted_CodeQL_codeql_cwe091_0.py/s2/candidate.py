from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xslt', methods=['GET', 'POST'])
def xslt():
    xml = request.args.get('xml') or request.form.get('xml')
    xpath_query = request.args.get('xslt') or request.form.get('xslt')

    if not xml or not xpath_query:
        return jsonify({'error': 'Missing xml or xslt parameter'}), 400

    try:
        root = etree.fromstring(xml.encode('utf-8'))
        results = root.xpath(xpath_query)

        result_list = []
        for result in results:
            if isinstance(result, str):
                result_list.append(result)
            else:
                result_list.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': result_list})

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'XML parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'XPath query error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
