# SPDX-FileCopyrightText: 2023-present Anders Steen <asteennilsen@gmail.com
#
# SPDX-License-Identifier: MIT
import click
from openai import AuthenticationError

from zshgpt.__about__ import __version__


@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name='zshgpt')
@click.argument('user_query')
def zshgpt(user_query: str) -> str:
    from zshgpt.util.chat_util import get_message

    try:
        message = get_message(user_query)
    except AuthenticationError as auth_error:
        raise click.ClickException(auth_error.message) from auth_error
    click.echo(message.content, nl=False)
