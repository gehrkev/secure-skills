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
        xpath_expr = request.args.get('xslt') or request.form.get('xslt')

        if not xml_source or not xpath_expr:
            return {"error": "Missing 'xml' or 'xslt' parameter"}, 400

        # Parse XML safely with XXE protection (CWE-611, CWE-776)
        # Disable external entity expansion to prevent XML Entity Expansion attacks
        parser = etree.XMLParser(resolve_entities=False, remove_blank_text=False)
        xml_doc = etree.fromstring(xml_source.encode('utf-8'), parser=parser)

        # Execute XPath query
        result = xml_doc.xpath(xpath_expr)

        # Format results for JSON serialization
        formatted_result = []
        for item in (result if isinstance(result, list) else [result]):
            if isinstance(item, etree._Element):
                formatted_result.append(etree.tostring(item, encoding='unicode'))
            else:
                formatted_result.append(str(item))

        return {"result": formatted_result}

    except etree.XMLSyntaxError as e:
        return {"error": f"Invalid XML: {str(e)}"}, 400
    except etree.XPathError as e:
        return {"error": f"Invalid XPath expression: {str(e)}"}, 400
    except Exception as e:
        return {"error": f"Error processing request: {str(e)}"}, 500
