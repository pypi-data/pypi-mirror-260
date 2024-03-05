# -*- coding: utf-8 -*-

"""

tests.test_core

Unit test the core module


Copyright (C) 2024 Rainer Schwarzbach

This file is part of morast.

morast is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

morast is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


import ast

# import logging

from typing import Iterator
from unittest import TestCase

from smdg import elements as mde
from smdg import strings as mds

from morast import core
from morast import nodes


EXPECTED_MBN_REPR = "<MorastBaseNode instance>"

JIGSAW_PUZZLE_PIECE_EMOJI = "\U0001f9e9"

SOURCE_DATACLASS = '''
@dataclasses.dataclass
class DataStorage:
    """class docstring"""

    number: int
    flag: bool = False
    identifier: str = "dummy"
'''


def parsed_body(source: str) -> Iterator[ast.AST]:
    """Return the body od a parsed module"""
    parsed_module = ast.parse(source)
    for item in parsed_module.body:
        if isinstance(item, ast.AST):
            yield item
        #
    #


class Functions(TestCase):
    """Module-level functions"""


class MorastClassDef(TestCase):
    """MorastClassDef class"""

    maxDiff = None

    def test_dataclass(self) -> None:
        """test initialization of a data class"""
        ast_class_def = list(parsed_body(SOURCE_DATACLASS))[0]
        if isinstance(ast_class_def, ast.ClassDef):
            class_def = core.MorastClassDef(ast_class_def)
        else:
            raise ValueError("Excpected a class definition")
        #
        with self.subTest("name"):
            self.assertEqual(class_def.name, "DataStorage")
        #
        with self.subTest("is a dataclass"):
            self.assertTrue(class_def.is_a_dataclass)
        #
        for item in ("number", "flag", "identifier"):
            with self.subTest("instamce_attribute", item=item):
                current_node = class_def.instance_attrs[item]
                if isinstance(current_node, nodes.Assignment):
                    self.assertEqual(
                        str(nodes.MorastName(item)),
                        str(current_node.target),
                    )
                else:
                    raise ValueError("expected an Assignment")
                #
            #
        #
        with self.subTest("MarkDown elements"):
            self.assertEqual(
                list(class_def.markdown_elements()),
                [
                    mde.HorizontalRule(20),
                    mde.Header(3, "Dataclass DataStorage()"),
                    mde.BlockQuote(mds.sanitize("class docstring")),
                    mde.HorizontalRule(20),
                    mde.Header(4, "instance attributes"),
                    mde.CompoundInlineElement(
                        mde.InlineElement(
                            f"{JIGSAW_PUZZLE_PIECE_EMOJI} DataStorage."
                        ),
                        mde.BoldText(mde.InlineElement("number")),
                        mde.InlineElement(": "),
                        mde.InlineElement("int"),
                    ),
                    mde.BlockQuote(
                        mds.sanitize("🚧 TODO: write number documentation")
                    ),
                    mde.CompoundInlineElement(
                        mde.InlineElement(
                            f"{JIGSAW_PUZZLE_PIECE_EMOJI} DataStorage."
                        ),
                        mde.BoldText(mde.InlineElement("flag")),
                        mde.InlineElement(": "),
                        mde.InlineElement("bool"),
                        mde.InlineElement(" = "),
                        mde.CodeSpan("False"),
                    ),
                    mde.BlockQuote(
                        mds.sanitize("🚧 TODO: write flag documentation")
                    ),
                    mde.CompoundInlineElement(
                        mde.InlineElement(
                            f"{JIGSAW_PUZZLE_PIECE_EMOJI} DataStorage."
                        ),
                        mde.BoldText(mde.InlineElement("identifier")),
                        mde.InlineElement(": "),
                        mde.InlineElement("str"),
                        mde.InlineElement(" = "),
                        mde.CodeSpan("'dummy'"),
                    ),
                    mde.BlockQuote(
                        mds.sanitize("🚧 TODO: write identifier documentation")
                    ),
                ],
            )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
