from flask import Flask, request
from lxml import etree

app = Flask(__name__)

@app.route('/parse_xml', methods=['GET', 'POST'])
def parse_xml():
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    try:
        root = etree.fromstring(xml_src.encode('utf-8'))
        return etree.tostring(root, encoding='unicode')
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run()
