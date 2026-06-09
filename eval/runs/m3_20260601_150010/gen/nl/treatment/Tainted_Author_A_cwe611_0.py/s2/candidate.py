from flask import Flask, request
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return "No xml_src parameter provided", 400

    try:
        parser = etree.XMLParser(resolve_entities=False, remove_blank_text=True)
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        result = etree.tostring(root, pretty_print=True, encoding='unicode')
        return result
    except etree.XMLSyntaxError as e:
        return f"Invalid XML: {str(e)}", 400
    except Exception as e:
        return f"Error parsing XML: {str(e)}", 500

if __name__ == '__main__':
    app.run()
