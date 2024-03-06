"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import click
import sys
import json
from hcs_cli.service import admin
from hcs_core.ctxp import panic, CtxpException
from hcs_core.ctxp.data_util import load_data_file
import hcs_core.sglib.cli_options as cli
from hcs_core.sglib import payload_util


@click.command()
@cli.org_id
@click.option("--provider", "-p", type=str, default=None, required=False, help="Override the provider instance ID")
@click.option(
    "--file",
    "-f",
    type=click.File("rt"),
    default=sys.stdin,
    help="Specify the payload file name. If not specified, STDIN will be used.",
)
def create(org: str, provider: str, file: str):
    """Create an edge.

    Example:
      hcs admin edge create --file payload/admin/edge-vsphere.json
    """

    payload = payload_util.get_payload_with_defaults(file, org)

    if provider:
        payload["providerInstanceId"] = provider

    _validate(payload)

    ret = admin.edge.create(payload)
    if ret:
        return ret
    return "", 1


def _validate(payload):
    if not payload.get("providerInstanceId"):
        raise CtxpException("Missing providerInstanceId")
