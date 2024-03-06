import sys

import click

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonGroup
from tecton_proto.secrets.secrets_service_pb2 import ListSecretScopesRequest


@click.command("secrets", cls=TectonGroup)
def secrets():
    """Manage Tecton secrets and secret scopes."""


@secrets.command("list-scopes", requires_auth=True, cls=TectonCommand)
def list_scopes():
    """List secret scopes in the current Tecton cluster"""
    request = ListSecretScopesRequest()
    response = metadata_service.instance().ListSecretScopes(request)

    if response.scopes == []:
        printer.safe_print("No secret scopes found", file=sys.stderr)
    else:
        for scope in response.scopes:
            printer.safe_print(scope.name)
