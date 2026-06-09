from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xpath', methods=['GET', 'POST'])
def xpath_query():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')
    xpath = request.args.get('xpath') or request.form.get('xpath')

    if not xml_src or not xpath:
        return jsonify({'error': 'Missing xml_src or xpath parameter'}), 400

    try:
        root = etree.fromstring(xml_src.encode('utf-8'))
        results = root.xpath(xpath)

        output = []
        for result in results:
            if isinstance(result, etree._Element):
                output.append(etree.tostring(result, encoding='unicode'))
            else:
                output.append(str(result))

        return jsonify({'results': output})
    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'XML parsing error: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'XPath query error: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
