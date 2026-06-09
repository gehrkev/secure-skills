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
        try:
            xml_src = request.get_json().get('xml_src')
        except:
            pass
    if not xml_src:
        xml_src = request.args.get('xml_src')

    if not xml_src:
        return ""

    xml = lxml.etree.fromstring(xml_src.encode('utf-8'))
    return lxml.etree.tostring(xml, encoding='unicode')
