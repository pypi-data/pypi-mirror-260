"""

    Tool command Account Create


"""
import logging
import secrets
from argparse import Namespace
from typing import Literal

from convex_api import KeyPair
from convex_api.tool.command.argparse_typing import (
    BaseArgs,
    SubParsersAction
)
from convex_api.tool.output import Output

from .command_base import CommandBase

logger = logging.getLogger(__name__)


class AccountCreateArgs(BaseArgs):
    command: Literal['account']
    account_command: Literal['create']
    topup: bool = False
    name: str | None = None


class AccountCreateCommand(CommandBase):

    def __init__(self, sub_parser: SubParsersAction | None = None):
        super().__init__('create', sub_parser)

    def create_parser(self, sub_parser: SubParsersAction):
        parser = sub_parser.add_parser(
            self._name,
            description='Create a new account',
            help='Create a new account'
        )

        parser.add_argument(
            '--topup',
            action='store_true',
            help='Topup account with sufficient funds. This only works for development networks. Default: False',
        )

        parser.add_argument(
            '-n',
            '--name',
            nargs='?',
            help='account name to register'
        )

        return parser

    def execute(self, args: Namespace, output: Output):
        typed_args = AccountCreateArgs.model_validate(vars(args))
        convex = self.load_convex(typed_args.url)

        key_pair = self.import_key_pair(typed_args)
        if key_pair is None:
            key_pair = KeyPair()

        logger.debug('creating account')
        account = convex.create_account(key_pair)

        if typed_args.topup:
            logger.debug('auto topup of account balance')
            convex.topup_account(account)

        if typed_args.name:
            logger.debug(f'registering account name {typed_args.name}')
            convex.topup_account(account)
            account = convex.register_account_name(typed_args.name, account)
        if typed_args.password:
            password = typed_args.password
        else:
            password = secrets.token_hex(32)
        values = {
            'password': password,
            'address': account.address,
            'public_key': key_pair.public_key,
            'keyfile': key_pair.export_to_text(password),
            'keywords': key_pair.export_to_mnemonic,
            'balance': convex.get_balance(account)
        }
        if account.name:
            values['name'] = account.name
        output.set_values(values)
        output.add_line_values(values)
