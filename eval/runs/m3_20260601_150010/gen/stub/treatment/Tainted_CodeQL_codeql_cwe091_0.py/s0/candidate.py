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
        # Get XML from request
        xml_input = request.args.get('xml') or request.form.get('xml')
        if not xml_input:
            return {'error': 'Missing xml parameter'}, 400

        # Get XPath from request
        xpath_input = request.args.get('xslt') or request.form.get('xslt')
        if not xpath_input:
            return {'error': 'Missing xslt parameter'}, 400

        # Create secure XML parser to prevent XXE attacks
        parser = etree.XMLParser(
            resolve_entities=False,
            no_network=True,
            remove_pis=True,
            load_dtd=False
        )

        # Parse the XML
        root = etree.fromstring(xml_input.encode('utf-8'), parser=parser)

        # Execute XPath query
        results = root.xpath(xpath_input)

        # Convert results to serializable format
        result_list = []
        for result in results:
            if isinstance(result, (str, bool, int, float)):
                result_list.append(result)
            else:
                result_list.append(etree.tostring(result, encoding='unicode'))

        return {'results': result_list}

    except etree.XMLSyntaxError:
        return {'error': 'Invalid XML'}, 400
    except Exception:
        return {'error': 'Query failed'}, 500
