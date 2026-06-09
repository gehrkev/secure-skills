from flask import Flask, request
from html import escape
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def get_team_members():
    team_name = request.args.get('team_name')

    if not team_name:
        return '<p>Error: team_name parameter required</p>', 400

    try:
        tree = ET.parse('teams.xml')
        root = tree.getroot()
    except FileNotFoundError:
        return '<p>Error: teams.xml not found</p>', 404
    except ET.ParseError:
        return '<p>Error: invalid XML document</p>', 500

    # Find the team
    for team in root.findall('.//team'):
        # Check by name attribute
        if team.get('name') == team_name:
            return format_members_html(team_name, team)

        # Check by name element
        name_elem = team.find('name')
        if name_elem is not None and name_elem.text == team_name:
            return format_members_html(team_name, team)

    return f'<p>Team "{escape(team_name)}" not found</p>', 404

def format_members_html(team_name, team_elem):
    members = []

    # Find members directly under team
    for member in team_elem.findall('member'):
        if member.text:
            members.append(member.text)

    # Find members in a members container
    if not members:
        members_container = team_elem.find('members')
        if members_container is not None:
            for member in members_container.findall('member'):
                if member.text:
                    members.append(member.text)

    html = f'<h1>{escape(team_name)}</h1>\n<ul>\n'
    for member in members:
        html += f'<li>{escape(member)}</li>\n'
    html += '</ul>'

    return html

if __name__ == '__main__':
    app.run()
