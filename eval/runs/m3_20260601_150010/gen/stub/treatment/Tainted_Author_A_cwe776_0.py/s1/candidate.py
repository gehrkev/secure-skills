import xml.etree.ElementTree as ET
from flask import Flask, request

app = Flask(__name__)

@app.route('/xml_upload')
def XMLUpload():
    '''
    Get the data from the request using 'xml_src'.
    Parse it as XML from the string.
    :return: The XML as a string.
    '''
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')

    if not xml_src:
        return ""

    try:
        try:
            parser = ET.XMLParser(resolve_entities=False)
        except TypeError:
            parser = ET.XMLParser()

        root = ET.fromstring(xml_src, parser=parser)
        return ET.tostring(root, encoding='unicode')
    except ET.ParseError:
        return ""
