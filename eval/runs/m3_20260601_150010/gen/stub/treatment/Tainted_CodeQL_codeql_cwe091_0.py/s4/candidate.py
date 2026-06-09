from lxml import etree
from io import StringIO
from flask import Flask, request

app = Flask(__name__)


@app.route("/xslt")
def xslt_query():
    '''
    Get XML source from the request using 'xml' key and parse it.
    Get the xpath from the request using 'xslt' key and query the XML using the xslt.
    :return: The result of the query.
    '''
    try:
        xml_source = request.args.get('xml')
        xpath_expr = request.args.get('xslt')

        if not xml_source or not xpath_expr:
            return "Missing xml or xslt parameter", 400

        # Parse XML safely - disable DTD processing and external entity expansion
        parser = etree.XMLParser(resolve_entities=False, remove_blank_text=False)
        root = etree.fromstring(xml_source.encode(), parser=parser)

        # Execute XPath query
        result = root.xpath(xpath_expr)

        return str(result)
    except Exception as e:
        return str(e), 400
