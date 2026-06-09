from flask import Flask, request, abort
from lxml import etree
from flask import jsonify
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
    team_name = request.args.get("team_name", "")

    # Input validation: build whitelist of valid team names
    valid_teams = {team.find("name").text for team in doc.findall("team")}

    # Reject if team_name not in whitelist (prevents XML injection)
    if team_name not in valid_teams:
        abort(400)

    # Find team safely without dynamic XPath
    team = None
    for t in doc.findall("team"):
        if t.find("name").text == team_name:
            team = t
            break

    if team is None:
        abort(404)

    # Extract members
    members = team.findall("members/member/name")

    # Build HTML list
    html = "<ul>"
    for member in members:
        html += f"<li>{member.text}</li>"
    html += "</ul>"

    return html, 200, {"Content-Type": "text/html"}
