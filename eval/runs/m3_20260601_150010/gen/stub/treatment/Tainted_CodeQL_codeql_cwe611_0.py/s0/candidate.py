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
        return {"error": "No xml_src provided"}, 400

    try:
        # Create parser with XXE protection
        parser = lxml.etree.XMLParser(resolve_external_dtd=False)
        tree = lxml.etree.fromstring(xml_src.encode(), parser=parser)
        return lxml.etree.tostring(tree, encoding='unicode')
    except lxml.etree.XMLSyntaxError as e:
        return {"error": f"Invalid XML: {str(e)}"}, 400
