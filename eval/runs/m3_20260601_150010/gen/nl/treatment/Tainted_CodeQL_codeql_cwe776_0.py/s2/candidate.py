from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/upload', methods=['GET'])
def upload():
    xml_src = request.args.get('xml_src', '')

    try:
        root = ET.fromstring(xml_src)
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError:
        return 'Invalid XML', 400

if __name__ == '__main__':
    app.run()
