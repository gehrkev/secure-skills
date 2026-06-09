import xml.etree.ElementTree as ET
from html import escape


def get_team_members(team_name):
    """
    Look up a team in the XML document and return an HTML list of its members.

    Args:
        team_name: The name of the team to look up

    Returns:
        HTML string containing an unordered list of team members
    """

    parser = ET.XMLParser()
    parser.entity = {}

    try:
        tree = ET.parse('teams.xml', parser=parser)
        root = tree.getroot()

        for team in root.findall('team'):
            if team.get('name') == team_name:
                members = team.findall('member')

                html = '<ul>\n'

                if not members:
                    html += '  <li>No members</li>\n'
                else:
                    for member in members:
                        member_name = member.text or ''
                        escaped_name = escape(member_name)
                        html += f'  <li>{escaped_name}</li>\n'

                html += '</ul>'
                return html

        return '<ul>\n  <li>Team not found</li>\n</ul>'

    except Exception as e:
        return f'<ul>\n  <li>Error: {escape(str(e))}</li>\n</ul>'
