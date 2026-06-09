from defusedxml import ElementTree as ET
from flask import Flask, request
from html import escape

app = Flask(__name__)

def load_teams_xml(filepath):
    """Load teams from XML file safely, preventing XXE attacks."""
    tree = ET.parse(filepath)
    return tree.getroot()

def get_team_html(root, team_name):
    """Find a team by name and return HTML list of members."""
    for team in root.findall('.//team'):
        # Check if team name matches (handle different XML structures)
        name_element = team.find('name')
        matches = (name_element is not None and name_element.text == team_name) or (team.get('name') == team_name)

        if matches:
            members = []
            for member in team.findall('member'):
                member_text = member.text
                if member_text:
                    members.append(member_text)
                else:
                    member_name = member.get('name')
                    if member_name:
                        members.append(member_name)

            # Generate HTML list with proper escaping
            html = '<ul>\n'
            for member in members:
                html += f'  <li>{escape(member)}</li>\n'
            html += '</ul>'
            return html

    return None

# Load XML at startup
teams_root = load_teams_xml('teams.xml')

@app.route('/teams', methods=['GET'])
def get_team_members():
    team_name = request.args.get('team_name')

    if not team_name:
        return "team_name parameter is required", 400

    html = get_team_html(teams_root, team_name)

    if html is None:
        return "Team not found", 404

    return html, 200, {'Content-Type': 'text/html'}

if __name__ == '__main__':
    app.run()
