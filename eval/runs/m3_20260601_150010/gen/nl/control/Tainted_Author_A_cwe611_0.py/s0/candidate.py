from flask import Flask, request
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return "No xml_src parameter provided", 400

    try:
        parsed = etree.fromstring(xml_src.encode() if isinstance(xml_src, str) else xml_src)
        return etree.tostring(parsed, encoding='unicode', pretty_print=True)
    except Exception as e:
        return f"Error parsing XML: {str(e)}", 400

if __name__ == '__main__':
    app.run(debug=True)
