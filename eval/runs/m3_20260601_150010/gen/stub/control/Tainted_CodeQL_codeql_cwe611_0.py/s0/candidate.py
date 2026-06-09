from flask import Flask, request
import lxml.etree

app = Flask(__name__)

@app.post("/parse_xml")
def parse_xml():
    '''
    Get the data from the request using 'xml_src'.
    Parse it as XML from the string.
    :return: The XML as a string.
    '''
    xml_src = request.form.get('xml_src') or request.args.get('xml_src')

    if not xml_src:
        data = request.get_json(silent=True)
        if data:
            xml_src = data.get('xml_src')

    if isinstance(xml_src, str):
        xml_src = xml_src.encode()

    tree = lxml.etree.fromstring(xml_src)
    return lxml.etree.tostring(tree, encoding='unicode')
