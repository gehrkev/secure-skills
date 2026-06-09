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
    data = request.get_json()
    xml_src = data.get('xml_src')

    if not xml_src:
        return {'error': 'xml_src not provided'}, 400

    # Create a secure parser with XXE and entity expansion protections
    parser = lxml.etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        remove_blank_text=False
    )

    try:
        root = lxml.etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        result = lxml.etree.tostring(root, encoding='unicode')
        return result, 200
    except lxml.etree.XMLSyntaxError as e:
        return {'error': str(e)}, 400
