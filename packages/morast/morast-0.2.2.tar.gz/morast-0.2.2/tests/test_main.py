# -*- coding: utf-8 -*-

"""

tests.test_main

Unit test the __main__ module


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import io
import sys

from unittest import TestCase

from unittest.mock import patch

from morast import __main__ as pkg_main

from .commons import GenericCallResult, RETURNCODE_OK


class ExecResult(GenericCallResult):
    """Program execution result"""

    @classmethod
    def do_call(cls, *args, **kwargs):
        """Do the real function call"""
        return pkg_main.main(*args)


class Program(TestCase):
    """Test the Program class"""

    @patch("sys.argv", new=[sys.argv[0]])
    @patch("sys.stdout", new_callable=io.StringIO)
    def test_execute(self, mock_stdout: io.StringIO) -> None:
        """execute() method, returncode only"""
        result = ExecResult.from_call("show-config", stdout=mock_stdout)
        self.assertEqual(result.returncode, RETURNCODE_OK)

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_version(self, mock_stdout: io.StringIO) -> None:
        """execute() method, version output"""
        with self.assertRaises(SystemExit) as cmgr:
            pkg_main.main("--version")
        #
        self.assertEqual(cmgr.exception.code, RETURNCODE_OK)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
            pkg_main.commandline.__version__,
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
