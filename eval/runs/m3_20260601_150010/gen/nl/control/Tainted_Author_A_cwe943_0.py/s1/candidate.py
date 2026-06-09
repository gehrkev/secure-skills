from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

def load_teams_xml(filename='teams.xml'):
    """Load and parse the XML document containing teams and members."""
    try:
        tree = ET.parse(filename)
        return tree.getroot()
    except Exception:
        return None

@app.route('/teams')
def get_team_members():
    """Look up team by name and return HTML list of members."""
    team_name = request.args.get('team_name')

    if not team_name:
        return '<p>Error: team_name parameter is required</p>', 400

    root = load_teams_xml()
    if root is None:
        return '<p>Error: XML document not found</p>', 500

    # Search for team with matching name
    for team in root.findall('team'):
        if team.get('name') == team_name:
            members = [member.text for member in team.findall('member') if member.text]

            if not members:
                html = f'<h2>{team_name}</h2><p>No members found</p>'
            else:
                html = f'<h2>{team_name}</h2><ul>'
                html += ''.join(f'<li>{member}</li>' for member in members)
                html += '</ul>'
            return html

    return f'<p>Error: Team "{team_name}" not found</p>', 404

if __name__ == '__main__':
    app.run(debug=True)
