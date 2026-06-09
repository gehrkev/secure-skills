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
    xpath = request.args.get('xpath')

    if not xml_src or not xpath:
        return Response('Missing parameters', status=400)

    try:
        # Disable external entity resolution to prevent XXE attacks
        parser = etree.XMLParser(resolve_entities=False)
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)

        # Execute the XPath query
        results = root.xpath(xpath)

        # Format and return results
        if results:
            if isinstance(results[0], str):
                return Response(results[0])
            else:
                return Response(etree.tostring(results[0], encoding='unicode'), mimetype='application/xml')
        else:
            return Response('No results', status=404)

    except etree.XMLSyntaxError:
        return Response('Invalid XML', status=400)
    except Exception as e:
        return Response(str(e), status=500)
