from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xslt', methods=['POST'])
def xslt_endpoint():
    try:
        xml_data = request.args.get('xml') or request.form.get('xml')
        xpath_query = request.args.get('xslt') or request.form.get('xslt')

        if not xml_data or not xpath_query:
            return jsonify({'error': 'Missing required parameters: xml and xslt'}), 400

        # Parse XML with XXE protection by disabling entity resolution
        parser = etree.XMLParser(resolve_entities=False)
        root = etree.fromstring(xml_data.encode('utf-8'), parser=parser)

        # Apply XPath query
        results = root.xpath(xpath_query)

        # Convert results to appropriate format
        result_list = []
        for result in results:
            if isinstance(result, str):
                result_list.append(result)
            else:
                result_list.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': result_list})

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except etree.XPathEvalError as e:
        return jsonify({'error': f'Invalid XPath query: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=False)
