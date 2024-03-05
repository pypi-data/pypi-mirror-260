"""

    Test Query

"""
from unittest.mock import Mock

from convex_api.tool.command.query_command import QueryCommand
from convex_api.tool.output import Output


def test_query_command(convex_url: str):
    args = Mock()

    args.command = 'query'
    args.url = convex_url
    args.query = '(address *registry*)'
    args.name_address = None
    args.keyfile = None
    args.keytext = None
    args.password = None
    args.keywords = None

    command = QueryCommand()
    output = Output()
    command.execute(args, output)
    assert output.values['value']
