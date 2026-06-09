from flask import Flask, request
from xml.etree import ElementTree as ET
from html import escape
import defusedxml.ElementTree as DefusedET

app = Flask(__name__)

def load_teams_xml(filename='teams.xml'):
    try:
        tree = DefusedET.parse(filename)
        return tree.getroot()
    except Exception:
        return None

@app.route('/teams')
def get_team_members():
    team_name = request.args.get('team_name', '').strip()

    if not team_name:
        return '<html><body><p>Error: team_name parameter is required</p></body></html>', 400

    root = load_teams_xml()
    if root is None:
        return '<html><body><p>Error: Unable to load teams data</p></body></html>', 500

    team = None
    for t in root.findall('.//team'):
        if t.get('name') == team_name:
            team = t
            break

    if team is None:
        return '<html><body><p>Error: Team not found</p></body></html>', 404

    html = '<!DOCTYPE html><html><head><title>{}</title></head><body>'.format(escape(team_name))
    html += '<h1>{}</h1><ul>'.format(escape(team_name))

    members = team.findall('.//member')
    if members:
        for member in members:
            member_name = member.text or ''
            html += '<li>{}</li>'.format(escape(member_name))
    else:
        html += '<li>No members found</li>'

    html += '</ul></body></html>'

    return html, 200

if __name__ == '__main__':
    app.run(debug=False)
