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
    xml_source = request.args.get('xml')
    xpath_expr = request.args.get('xslt')

    try:
        root = etree.fromstring(xml_source.encode('utf-8'))
        result = root.xpath(xpath_expr)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 400
