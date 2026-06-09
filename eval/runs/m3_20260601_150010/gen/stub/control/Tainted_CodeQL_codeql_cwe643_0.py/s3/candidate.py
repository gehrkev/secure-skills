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

    root = etree.fromstring(xml_src.encode())
    result = root.xpath(xpath)

    if result:
        if isinstance(result[0], str):
            return result[0]
        return etree.tostring(result[0], encoding='unicode')

    return ""
