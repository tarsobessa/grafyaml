# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import inspect
import sys

from oslo_config import cfg

from grafana_dashboards.builder import Builder
from grafana_dashboards import config

CONF = cfg.CONF


class Commands(object):

    def __init__(self):
        self.builder = Builder()

    def execute(self):
        exec_method = getattr(self, CONF.action.name)
        args = inspect.getargspec(exec_method)
        args.args.remove('self')
        kwargs = {}
        for arg in args.args:
            kwargs[arg] = getattr(CONF.action, arg)
        exec_method(**kwargs)

    def update(self, path):
        self.builder.update_dashboard(path)


def main():

    def add_command_parsers(subparsers):
        parser_update = subparsers.add_parser('update')
        parser_update.add_argument(
            'path', help='colon-separated list of paths to YAML files or'
            ' directories')

    CONF.register_cli_opt(
        cfg.SubCommandOpt('action', handler=add_command_parsers))
    config.prepare_args(sys.argv)

    Commands().execute()
    sys.exit(0)
