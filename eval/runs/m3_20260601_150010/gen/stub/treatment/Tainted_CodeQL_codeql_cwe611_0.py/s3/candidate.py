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
    xml_src = request.form.get('xml_src')

    if not xml_src:
        return {'error': 'xml_src is required'}, 400

    try:
        parser = lxml.etree.XMLParser(resolve_entities=False)
        tree = lxml.etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        return lxml.etree.tostring(tree, encoding='unicode')
    except lxml.etree.XMLSyntaxError:
        return {'error': 'Invalid XML'}, 400
