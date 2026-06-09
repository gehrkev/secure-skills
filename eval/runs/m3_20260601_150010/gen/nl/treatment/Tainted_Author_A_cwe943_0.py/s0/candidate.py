from flask import Flask, request
import xml.etree.ElementTree as ET
import html

app = Flask(__name__)

@app.route('/teams')
def get_team_members():
    team_name = request.args.get('team_name', '')

    if not team_name:
        return '<p>Error: team_name parameter required</p>', 400

    try:
        tree = ET.parse('teams.xml')
        root = tree.getroot()

        # Search for team by name attribute
        for team in root.findall('.//team'):
            if team.get('name') == team_name:
                # Build HTML list of members
                result = '<ul>\n'
                for member in team.findall('member'):
                    name = html.escape(member.text or '')
                    result += f'<li>{name}</li>\n'
                result += '</ul>'
                return result

        return '<p>Team not found</p>', 404

    except FileNotFoundError:
        return '<p>XML file not found</p>', 500
    except ET.ParseError:
        return '<p>Invalid XML format</p>', 500
    except Exception:
        return '<p>Error processing request</p>', 500

if __name__ == '__main__':
    app.run(debug=False)
