from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/')
def get_team_members():
    team_name = request.args.get('team_name')

    if not team_name:
        return '''
        <html>
        <body>
        <p>Please provide a team_name query parameter</p>
        </body>
        </html>
        '''

    try:
        tree = ET.parse('teams.xml')
        root = tree.getroot()
    except (FileNotFoundError, ET.ParseError):
        return '''
        <html>
        <body>
        <p>Error loading team data</p>
        </body>
        </html>
        '''

    # Find team with matching name
    for team in root.findall('team'):
        if team.get('name') == team_name:
            members = [m.text for m in team.findall('member') if m.text]

            html = f'''
            <html>
            <body>
            <h1>{team_name}</h1>
            <ul>
            '''

            for member in members:
                html += f'<li>{member}</li>\n'

            html += '''
            </ul>
            </body>
            </html>
            '''

            return html

    return '''
    <html>
    <body>
    <p>Team not found</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run()
