from flask import Flask, request, jsonify
from lxml import etree
import io

app = Flask(__name__)

@app.route('/xslt', methods=['POST'])
def xslt():
    try:
        xml_data = request.form.get('xml')
        xpath_query = request.form.get('xslt')

        if not xml_data:
            return jsonify({'error': 'Missing xml parameter'}), 400
        if not xpath_query:
            return jsonify({'error': 'Missing xslt parameter'}), 400

        parser = etree.XMLParser(
            resolve_entities=False,
            remove_blank_text=True,
            remove_comments=True,
            remove_pis=True
        )

        xml_tree = etree.parse(io.StringIO(xml_data), parser=parser)
        root = xml_tree.getroot()

        results = root.xpath(xpath_query)

        output = []
        for result in results:
            if isinstance(result, str):
                output.append(result)
            elif isinstance(result, (int, float, bool)):
                output.append(result)
            else:
                output.append(etree.tostring(result, encoding='unicode'))

        return jsonify({'results': output}), 200

    except etree.XMLSyntaxError as e:
        return jsonify({'error': f'Invalid XML: {str(e)}'}), 400
    except etree.XPathEvalError as e:
        return jsonify({'error': f'Invalid XPath query: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)
