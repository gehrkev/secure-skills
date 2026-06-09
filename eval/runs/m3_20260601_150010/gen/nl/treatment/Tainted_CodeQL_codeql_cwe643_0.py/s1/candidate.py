from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xpath', methods=['GET', 'POST'])
def execute_xpath():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')
    xpath_query = request.args.get('xpath') or request.form.get('xpath')

    if not xml_src:
        return jsonify({'error': 'xml_src parameter is required'}), 400
    if not xpath_query:
        return jsonify({'error': 'xpath parameter is required'}), 400

    try:
        parser = etree.XMLParser(
            resolve_entities=False,
            remove_blank_text=True,
            dtd_validation=False
        )
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)
    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except Exception:
        return jsonify({'error': 'Failed to parse XML'}), 400

    try:
        results = root.xpath(xpath_query)
    except etree.XPathError as e:
        return jsonify({'error': f'Invalid XPath query: {str(e)}'}), 400
    except Exception:
        return jsonify({'error': 'XPath query execution failed'}), 400

    serialized = []
    for result in results:
        if isinstance(result, (str, int, float, bool)):
            serialized.append(result)
        else:
            serialized.append(etree.tostring(result, encoding='unicode'))

    return jsonify({'results': serialized, 'count': len(serialized)})

if __name__ == '__main__':
    app.run(debug=False)
