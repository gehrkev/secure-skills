from flask import Flask, request, escape
from defusedxml.ElementTree import parse as defused_parse

app = Flask(__name__)

@app.route('/teams', methods=['GET'])
def get_team_members():
    team_name = request.args.get('team_name', '')

    if not team_name:
        return "<html><body><p>No team name provided</p></body></html>"

    try:
        tree = defused_parse('teams.xml')
        root = tree.getroot()

        for team in root.findall('team'):
            if team.get('name') == team_name:
                members = team.findall('member')
                html = "<html><body><h1>" + escape(team_name) + "</h1><ul>"
                for member in members:
                    member_name = member.text if member.text else ""
                    html += "<li>" + escape(member_name) + "</li>"
                html += "</ul></body></html>"
                return html

        return "<html><body><p>Team not found</p></body></html>"

    except Exception:
        return "<html><body><p>Error processing request</p></body></html>"

if __name__ == '__main__':
    app.run()
