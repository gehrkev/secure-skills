from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xpath_query', methods=['GET', 'POST'])
def xpath_query():
    """
    Execute XPath query on XML.
    Parameters:
      - xml_src: XML content as string
      - xpath: XPath expression
    """
    try:
        xml_src = request.args.get('xml_src') or request.form.get('xml_src')
        xpath_expr = request.args.get('xpath') or request.form.get('xpath')

        if not xml_src:
            return jsonify({'error': 'xml_src parameter is required'}), 400
        if not xpath_expr:
            return jsonify({'error': 'xpath parameter is required'}), 400

        parser = etree.XMLParser(remove_blank_text=False, resolve_entities=False)
        try:
            root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        except etree.XMLSyntaxError as e:
            return jsonify({'error': f'Invalid XML: {str(e)}'}), 400

        try:
            results = root.xpath(xpath_expr)
        except etree.XPathError as e:
            return jsonify({'error': f'Invalid XPath: {str(e)}'}), 400

        output = []
        for result in results:
            if isinstance(result, str):
                output.append(result)
            elif isinstance(result, (int, float, bool)):
                output.append(result)
            else:
                output.append(etree.tostring(result, encoding='unicode', method='xml'))

        return jsonify({'results': output}), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
