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
    try:
        xml_src = request.args.get('xml_src')
        xpath = request.args.get('xpath')

        if not xml_src or not xpath:
            return Response('Missing xml_src or xpath parameter', status=400)

        parser = etree.XMLParser(resolve_entities=False)
        tree = etree.fromstring(xml_src.encode('utf-8'), parser=parser)

        result = tree.xpath(xpath)

        if result:
            if isinstance(result[0], str):
                return Response(result[0], mimetype='text/plain')
            else:
                return Response(etree.tostring(result[0], encoding='unicode'), mimetype='application/xml')
        else:
            return Response('No matching elements', status=404)

    except etree.XMLSyntaxError as e:
        return Response(f'Invalid XML: {str(e)}', status=400)
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500)
