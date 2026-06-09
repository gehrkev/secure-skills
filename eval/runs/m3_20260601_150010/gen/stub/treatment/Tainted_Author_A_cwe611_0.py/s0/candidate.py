import lxml.etree

from flask import Flask, request

app = Flask(__name__)


@app.route('/parse_xml')
def parse_xml():
    '''
    Get the data from the request using 'xml_src'.
    Parse it as XML from the string.
    :return: The XML as a string.
    '''
    xml_src = request.args.get('xml_src', '')

    parser = lxml.etree.XMLParser(
        resolve_entities=False,
        no_network=True
    )

    try:
        root = lxml.etree.fromstring(xml_src.encode('utf-8'), parser=parser)
        return lxml.etree.tostring(root, pretty_print=True).decode('utf-8')
    except (lxml.etree.XMLSyntaxError, ValueError):
        return ""
