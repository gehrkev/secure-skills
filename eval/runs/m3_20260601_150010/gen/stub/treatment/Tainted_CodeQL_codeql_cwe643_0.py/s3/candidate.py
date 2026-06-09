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
    xml_src = request.args.get('xml_src')
    xpath_expr = request.args.get('xpath')

    if not xml_src or not xpath_expr:
        return "Missing parameters", 400

    # Disable external entity expansion to prevent XXE attacks
    parser = etree.XMLParser(resolve_entities=False)

    try:
        root = etree.fromstring(xml_src.encode(), parser=parser)
    except etree.XMLSyntaxError:
        return "Invalid XML", 400

    try:
        result = root.xpath(xpath_expr)
    except etree.XPathError:
        return "Invalid XPath", 400

    if not result:
        return "No results", 404

    # Convert result to string
    if isinstance(result, list) and result:
        item = result[0]
        if hasattr(item, 'tag'):
            return etree.tostring(item, encoding='unicode')
        else:
            return str(item)

    return str(result)
