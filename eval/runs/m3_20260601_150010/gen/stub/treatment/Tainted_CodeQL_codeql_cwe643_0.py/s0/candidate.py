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
    xml_src = request.args.get('xml_src', '')
    xpath = request.args.get('xpath', '')

    if not xml_src or not xpath:
        return Response('Missing parameters', status=400)

    try:
        # Create parser with XXE protection - disable external entity resolution and DTD parsing
        parser = etree.XMLParser(
            resolve_entities=False,
            dtd_validation=False,
            remove_blank_text=True
        )

        # Parse XML safely
        root = etree.fromstring(xml_src.encode('utf-8'), parser=parser)

        # Execute XPath query
        result = root.xpath(xpath)

        # Format results
        output = []
        for item in result:
            if isinstance(item, str):
                output.append(item)
            else:
                output.append(etree.tostring(item, encoding='unicode'))

        return Response('\n'.join(output), mimetype='text/plain')

    except etree.XMLSyntaxError:
        return Response('Invalid XML', status=400)
    except Exception:
        return Response('Error processing request', status=500)
