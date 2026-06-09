from flask import Flask, request, abort
from lxml import etree
from flask import jsonify
import html
app = Flask(__name__)

xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<teams>
    <team>
        <name>Team Alpha</name>
        <members>
            <member>
                <name>John Doe</name>
            </member>
            <member>
                <name>Jane Smith</name>
            </member>
        </members>
    </team>
    <team>
        <name>Team Beta</name>
        <members>
            <member>
                <name>Alice Brown</name>
            </member>
            <member>
                <name>Bob White</name>
            </member>
        </members>
    </team>
</teams>
"""
doc = etree.fromstring(xml)

@app.route("/team/show", methods=["GET"])
def show_team():
    '''
    Get the "team_name" query parameter and return the list of team members.
    @return: An HTML  list of team members.
    '''
    team_name = request.args.get('team_name')

    if not team_name:
        abort(400)

    # Find the team with the given name (safe comparison, no XPath injection)
    for team in doc.findall('.//team'):
        name_elem = team.find('name')
        if name_elem is not None and name_elem.text == team_name:
            members = team.find('members')
            if members is not None:
                member_list = []
                for member in members.findall('member'):
                    member_name_elem = member.find('name')
                    if member_name_elem is not None and member_name_elem.text:
                        member_list.append(member_name_elem.text)

                html_content = '<ul>'
                for member in member_list:
                    html_content += f'<li>{html.escape(member)}</li>'
                html_content += '</ul>'
                return html_content

    abort(404)
