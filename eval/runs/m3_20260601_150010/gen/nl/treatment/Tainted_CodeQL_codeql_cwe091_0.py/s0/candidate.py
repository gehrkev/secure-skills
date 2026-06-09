from flask import Flask, request, jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/xslt', methods=['GET', 'POST'])
def xslt_endpoint():
    try:
        # Get parameters from request (POST preferred, GET as fallback)
        xml_content = request.form.get('xml') or request.args.get('xml')
        xpath_query = request.form.get('xslt') or request.args.get('xslt')

        if not xml_content or not xpath_query:
            return jsonify({'error': 'Missing xml or xslt parameter'}), 400

        # Parse XML safely (disable external entity processing to prevent XXE)
        parser = etree.XMLParser(
            resolve_entities=False,
            no_network=True,
            remove_blank_text=True
        )
        xml_doc = etree.fromstring(xml_content.encode('utf-8'), parser=parser)

        # Apply XPath query
        results = xml_doc.xpath(xpath_query)

        # Convert results to JSON-serializable format
        output = []
        for result in results:
            if isinstance(result, (str, int, float, bool)):
                output.append(result)
            else:
                # Element node
                output.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': output}), 200

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except etree.XPathError as e:
        return jsonify({'error': f'Invalid XPath query: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing request: {str(e)}'}), 500

if __name__ == '__main__':
    app.run()
