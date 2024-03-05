# -*- coding: utf-8 -*-

"""

morast.configuration

Configuration handling


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import dataclasses
import logging
import pathlib

from typing import Any, Dict

import yaml


#
# Constants
#


CWD = pathlib.Path(".").resolve()
SRC = "src"
DOCS = "docs"
REFERENCE = "reference"
MORAST_CONFIG_DIR = ".morast"
OVERRIDES = "overrides"

DEFAULT_ENCODING = "utf-8"
DEFAULT_ADVERTISE = False
DEFAULT_SOURCE = CWD / SRC
DEFAULT_DESTINATION = CWD / DOCS / REFERENCE
DEFAULT_CONFIG_FILE = CWD / MORAST_CONFIG_DIR / "config.yaml"
DEFAULT_OVERRIDES_BASEPATH = CWD / MORAST_CONFIG_DIR / OVERRIDES

KW_ADVERTISE = "advertise"
KW_SOURCE_PATH = "source_path"
KW_DESTINATION_PATH = "destination_path"
KW_OVERRIDES_BASEPATH = "overrides_basepath"


#
# classes
#


@dataclasses.dataclass
class GlobalOptions:
    """Global program options"""

    source_path: pathlib.Path = DEFAULT_SOURCE
    destination_path: pathlib.Path = DEFAULT_DESTINATION
    overrides_basepath: pathlib.Path = DEFAULT_OVERRIDES_BASEPATH
    advertise: bool = DEFAULT_ADVERTISE

    def serializable(self) -> Dict[str, Any]:
        """Serializable variant
        as a dict having the path objects converted to strings
        """
        return {
            KW_ADVERTISE: self.advertise,
            KW_DESTINATION_PATH: str(self.destination_path),
            KW_OVERRIDES_BASEPATH: str(self.overrides_basepath),
            KW_SOURCE_PATH: str(self.source_path),
        }

    def dump(self) -> str:
        """return the configuration as a YAML dump"""
        return yaml.dump(
            self.serializable(), default_flow_style=False, indent=2
        )

    @classmethod
    def from_file(
        cls,
        path: pathlib.Path = DEFAULT_CONFIG_FILE,
        advertise_preset=DEFAULT_ADVERTISE,
    ) -> "GlobalOptions":
        """Read the config file and return a GlobalOptions instance"""
        if not path.exists():
            return cls()
        #
        pre_config: Dict[str, Any] = {}
        raw_config = yaml.safe_load(path.read_text(encoding=DEFAULT_ENCODING))
        for path_kw in (
            KW_DESTINATION_PATH,
            KW_OVERRIDES_BASEPATH,
            KW_SOURCE_PATH,
        ):
            try:
                value = raw_config[path_kw]
            except KeyError:
                logging.info(
                    "Keyword %r missing in configuration file"
                    " – using hardcoded preset",
                    path_kw,
                )
            else:
                pre_config[path_kw] = pathlib.Path(value).resolve()
            #
        #
        pre_config[KW_ADVERTISE] = raw_config.get(
            KW_ADVERTISE, advertise_preset
        )
        return cls(**pre_config)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
