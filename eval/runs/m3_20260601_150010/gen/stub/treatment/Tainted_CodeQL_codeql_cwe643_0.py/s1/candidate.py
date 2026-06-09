from lxml import etree

from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/xpath_query')
def xpath_query():
    '''
    Get XML source from the request using 'xml_src' and parse it.
    Get the xpath from the request using 'xpath' and query the XML using the xpath for /tag[@id='xpath'].
    :return: The result of the query.
    '''
    xml_src = request.args.get('xml_src') or request.form.get('xml_src')
    xpath = request.args.get('xpath') or request.form.get('xpath')

    if not xml_src or not xpath:
        return Response("Missing parameters", status=400)

    try:
        parser = etree.XMLParser(resolve_entities=False, no_network=True)
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)
    except (etree.XMLSyntaxError, UnicodeDecodeError):
        return Response("Invalid XML", status=400)

    try:
        result = root.xpath(xpath)
    except etree.XPathError:
        return Response("Invalid XPath", status=400)

    return Response(str(result), content_type='text/plain')
