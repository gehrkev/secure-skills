from flask import Flask, request
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.values.get('xml_src')

    if not xml_src:
        return "No xml_src parameter provided", 400

    try:
        root = etree.fromstring(xml_src.encode())
        result = etree.tostring(root, pretty_print=True).decode()
        return result
    except etree.XMLSyntaxError as e:
        return f"XML parsing error: {str(e)}", 400

if __name__ == '__main__':
    app.run()
