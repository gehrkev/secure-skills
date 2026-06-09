from flask import Flask, request
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml')
def parse_xml():
    xml_src = request.args.get('xml_src')

    if not xml_src:
        return "No xml_src parameter provided", 400

    try:
        root = etree.fromstring(xml_src.encode('utf-8'))
        result = etree.tostring(root, encoding='unicode')
        return result
    except Exception as e:
        return f"Error parsing XML: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)
