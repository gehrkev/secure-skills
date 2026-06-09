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
        xml_source = request.args.get('xml') or request.form.get('xml')
        xpath_query = request.args.get('xslt') or request.form.get('xslt')

        if not xml_source or not xpath_query:
            return {'error': 'Missing required parameters'}, 400

        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False)
        tree = etree.parse(StringIO(xml_source), parser)
        root = tree.getroot()

        results = root.xpath(xpath_query)

        response_results = []
        for result in results:
            if isinstance(result, (str, bool, int, float)):
                response_results.append(result)
            else:
                response_results.append(etree.tostring(result, encoding='unicode'))

        return {'results': response_results}

    except etree.XMLSyntaxError:
        return {'error': 'Invalid XML'}, 400
    except Exception:
        return {'error': 'Query failed'}, 400
