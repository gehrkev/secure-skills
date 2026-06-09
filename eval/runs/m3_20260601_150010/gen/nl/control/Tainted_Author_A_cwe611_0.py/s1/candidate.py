from flask import Flask, request
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.values.get('xml_src')

    if not xml_src:
        return "Error: xml_src parameter not provided", 400

    try:
        root = etree.fromstring(xml_src.encode('utf-8'))
        result = etree.tostring(root, encoding='unicode')
        return result
    except etree.XMLSyntaxError as e:
        return f"Error parsing XML: {str(e)}", 400

if __name__ == '__main__':
    app.run()
