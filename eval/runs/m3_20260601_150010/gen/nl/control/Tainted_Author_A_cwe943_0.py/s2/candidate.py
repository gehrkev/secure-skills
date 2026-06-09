from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def get_team_members():
    team_name = request.args.get('team_name')

    if not team_name:
        return '<p>No team_name provided</p>'

    try:
        tree = ET.parse('teams.xml')
        root = tree.getroot()
    except FileNotFoundError:
        return '<p>XML document not found</p>'

    for team in root.findall('team'):
        name_elem = team.find('name')
        team_id = team.get('name')

        if (name_elem is not None and name_elem.text == team_name) or team_id == team_name:
            members = team.findall('member')
            if not members:
                return '<ul></ul>'

            html = '<ul>'
            for member in members:
                member_name = member.text or member.get('name')
                if member_name:
                    html += f'<li>{member_name}</li>'
            html += '</ul>'
            return html

    return '<p>Team not found</p>'

if __name__ == '__main__':
    app.run()
