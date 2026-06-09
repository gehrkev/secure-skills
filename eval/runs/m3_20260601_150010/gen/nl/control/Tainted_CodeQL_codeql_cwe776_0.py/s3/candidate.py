from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/upload', methods=['GET'])
def upload():
    xml_src = request.args.get('xml_src')
    root = ET.fromstring(xml_src)
    return ET.tostring(root, encoding='unicode')

if __name__ == '__main__':
    app.run()
