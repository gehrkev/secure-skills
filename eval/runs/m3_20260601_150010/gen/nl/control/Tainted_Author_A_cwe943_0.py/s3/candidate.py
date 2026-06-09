from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Sample XML data with teams and their members
XML_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<teams>
    <team name="Engineering">
        <members>
            <member>Alice Johnson</member>
            <member>Bob Smith</member>
            <member>Carol Davis</member>
        </members>
    </team>
    <team name="Marketing">
        <members>
            <member>Diana Wilson</member>
            <member>Eve Brown</member>
        </members>
    </team>
    <team name="Sales">
        <members>
            <member>Frank Miller</member>
            <member>Grace Lee</member>
            <member>Henry Chen</member>
        </members>
    </team>
</teams>"""

@app.route('/')
def get_team_members():
    team_name = request.args.get('team_name')

    if not team_name:
        return "<p>Error: team_name query parameter is required</p>", 400

    try:
        root = ET.fromstring(XML_DATA)
    except ET.ParseError:
        return "<p>Error: Failed to parse XML</p>", 500

    # Find the team by name
    team = None
    for t in root.findall('team'):
        if t.get('name') == team_name:
            team = t
            break

    if team is None:
        return f"<p>Team '{team_name}' not found</p>", 404

    # Extract members and build HTML list
    members_elem = team.find('members')
    if members_elem is None:
        html = f"<h1>{team_name}</h1><p>No members found</p>"
        return html, 200

    member_items = []
    for member in members_elem.findall('member'):
        if member.text:
            member_items.append(f"<li>{member.text}</li>")

    html = f"<h1>{team_name}</h1><ul>{''.join(member_items)}</ul>"
    return html, 200

if __name__ == '__main__':
    app.run(debug=True)
