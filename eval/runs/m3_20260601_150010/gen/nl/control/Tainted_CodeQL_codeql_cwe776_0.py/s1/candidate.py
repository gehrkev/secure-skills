from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/upload', methods=['GET'])
def upload():
    xml_src = request.args.get('xml_src')
    if xml_src is None:
        return "No xml_src parameter provided", 400

    try:
        root = ET.fromstring(xml_src)
        result = ET.tostring(root, encoding='unicode')
        return result
    except ET.ParseError as e:
        return f"Invalid XML: {str(e)}", 400

if __name__ == '__main__':
    app.run()
