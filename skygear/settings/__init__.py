# Copyright 2015 Oursky Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import importlib
from argparse import Namespace

from .parser import SettingsParser
from .module import _config_module, get_module


_parsers = {}
settings = Namespace()


def add_parser(name, parser, parse_now=True):
    """
    Add the specified SettingsParser. If parse_now is True (the default),
    the parser is run immediately.
    """
    global _parsers
    if name in _parsers:
        raise Exception("Parser \"{}\" already defined.", name)
    _parsers[name] = parser
    if parse_now:
        _parse(name, parser)


def _parse(name, parser):
    global settings

    ns = getattr(settings, name, Namespace())
    ns = parser.parse_settings(ns)
    setattr(settings, name, ns)


def parse_all():
    """
    Parse all settings.
    """
    global _parsers
    global settings

    for name, parser in _parsers.items():
        _parse(name, parser)
    return settings


def config_module(name, *args, **kwargs):
    """
    Try to config the already imported module on boot time. If the package is
    not already imported in boot time, will try to import as normal package
    and config it.

    config_module will not import another copy of the module if it was already
    loaded at boot time.
    """
    global settings
    try:
        module = get_module(name)
    except NameError:
        module = importlib.import_module(name)
    _config_module(module, settings, *args, **kwargs)


__all__ = [
    Namespace,
    SettingsParser, settings,
    config_module,
    add_parser, parse_all
]
