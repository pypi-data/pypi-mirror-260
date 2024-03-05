# -*- coding: utf-8 -*-

"""

tests.test_nodes

Unit test the nodes module


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
import logging

from unittest import TestCase

from smdg import elements as mde

from morast import nodes


EXPECTED_MBN_REPR = "<MorastBaseNode instance>"


class Functions(TestCase):
    """Module-level functions"""


class MorastBaseNode(TestCase):
    """MorastBaseNode class"""

    def test_repr(self) -> None:
        """__repr__() special method"""
        mbn = nodes.MorastBaseNode()
        self.assertEqual(repr(mbn), EXPECTED_MBN_REPR)

    def test_str(self) -> None:
        """string representation – in this case, equal to repr()"""
        mbn = nodes.MorastBaseNode()
        self.assertEqual(str(mbn), EXPECTED_MBN_REPR)

    def test_properties(self) -> None:
        """instance properties"""
        mbn = nodes.MorastBaseNode()
        self.assertFalse(mbn.quotes_required)

    def test_plain_display(self) -> None:
        """.plain_display() method"""
        mbn = nodes.MorastBaseNode()
        self.assertEqual(mbn.plain_display(), EXPECTED_MBN_REPR)

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        mbn = nodes.MorastBaseNode()
        self.assertEqual(
            mbn.as_markdown(), mde.InlineElement(EXPECTED_MBN_REPR)
        )


class MorastErrorNode(TestCase):
    """MorastErrorNode class"""

    def test_message_attr(self) -> None:
        """message sttribute + logging"""
        message = "error message"
        with self.assertLogs(
            logging.getLogger(), level=logging.WARNING
        ) as log_cm:
            with self.subTest("warning logged"):
                men = nodes.MorastErrorNode(message)
                self.assertIn(message, log_cm.output[0])
            #
        #
        with self.subTest("message is stored"):
            self.assertEqual(men.message, message)
        #

    def test_as_markdown(self) -> None:
        """.as_markdown() method + logging"""
        message = "error_* message [addendum]"
        with self.assertLogs(
            logging.getLogger(), level=logging.WARNING
        ) as log_cm:
            with self.subTest("warning logged"):
                men = nodes.MorastErrorNode(message)
                self.assertIn(message, log_cm.output[0])
            #
        #
        with self.subTest("markdown as expected"):
            self.assertEqual(men.as_markdown(), mde.Paragraph(message))
        #


class MorastKeyword(TestCase):
    """MorastKeyword class"""

    def test_str(self) -> None:
        """string representation"""
        with self.subTest("value only"):
            value = nodes.MorastName("varname")
            mkw = nodes.MorastKeyword(value)
            self.assertEqual(str(mkw), f"**{value}")
        #
        with self.subTest("arg and value only"):
            arg = "varname"
            value = nodes.MorastName("value_var")
            mkw = nodes.MorastKeyword(value, arg=arg)
            self.assertEqual(str(mkw), f"{arg}={value}")
        #

    def test_prefix(self) -> None:
        """prefix property"""
        with self.subTest("value only"):
            value = nodes.MorastName("varname")
            mkw = nodes.MorastKeyword(value)
            self.assertEqual(mkw.prefix, "**")
        #
        with self.subTest("arg and value only"):
            arg = "varname"
            value = nodes.MorastName("value_var")
            mkw = nodes.MorastKeyword(value, arg=arg)
            self.assertEqual(mkw.prefix, f"{arg}=")
        #


class MorastConstant(TestCase):
    """MorastConstant class"""

    def test_str(self) -> None:
        """string representation"""
        for value, expected_str in (
            (Ellipsis, "…"),
            ("test_string", "test_string"),
            (7, "7"),
            (5.5, "5.5"),
            (True, "True"),
            (None, "None"),
        ):
            with self.subTest(value=value, expected_str=expected_str):
                mco = nodes.MorastConstant(value)
                self.assertEqual(str(mco), expected_str)
            #
        #

    def test_quotes_required(self) -> None:
        """quotes_required property"""
        for value, expected_quote_requirement in (
            (Ellipsis, False),
            ("test_string", True),
            (7, False),
            (5.5, False),
            (True, False),
            (None, False),
        ):
            with self.subTest(
                value=value,
                expected_quote_requirement=expected_quote_requirement,
            ):
                mco = nodes.MorastConstant(value)
                self.assertEqual(
                    mco.quotes_required, expected_quote_requirement
                )
            #
        #

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        for value, expected_mde in (
            (Ellipsis, mde.InlineElement("…")),
            ("test_string", mde.CodeSpan("'test_string'")),
            (7, mde.CodeSpan("7")),
            (5.5, mde.CodeSpan("5.5")),
            (True, mde.CodeSpan("True")),
            (None, mde.CodeSpan("None")),
        ):
            with self.subTest(value=value, expected_mde=expected_mde):
                mco = nodes.MorastConstant(value)
                self.assertEqual(mco.as_markdown(), expected_mde)
            #
        #


# TODO: MorastFormattedValue
# TODO: MorastJoinedStr
# TODO: MorastBinOp
# TODO: MorastName
# TODO: MorastNamespace
# TODO: MorastDictItem
# TODO: MorastStarred


class CompoundNode(TestCase):
    """CompoundNode class"""

    def test_add(self) -> None:
        """.add() method"""
        mcn = nodes.CompoundNode()
        if not mcn.add_supported:
            self.assertRaisesRegex(
                ValueError,
                "^Adding elements not supported",
                mcn.add,
                nodes.MorastBaseNode(),
            )
        #

    def test_get_contents(self) -> None:
        """.get_contents() method"""
        mcn = nodes.CompoundNode(
            nodes.MorastName("abc"),
            nodes.MorastConstant(7),
            nodes.MorastConstant("xyz"),
            nodes.MorastConstant(Ellipsis),
        )
        self.assertEqual(
            mcn.get_contents(),
            ["abc", ", ", "7", ", ", "'xyz'", ", ", "…"],
        )

    def test_str(self) -> None:
        """string representation"""
        mcn = nodes.CompoundNode(
            nodes.MorastName("abc"),
            nodes.MorastConstant(7),
            nodes.MorastConstant("xyz"),
            nodes.MorastConstant(Ellipsis),
        )
        self.assertEqual(
            str(mcn),
            "abc, 7, 'xyz', …",
        )

    def test_get_contents_md(self) -> None:
        """.get_contents_md() method"""
        md_joiner = mde.InlineElement(", ")
        mcn = nodes.CompoundNode(
            nodes.MorastName("abc"),
            nodes.MorastConstant(7),
            nodes.MorastConstant("xyz"),
            nodes.MorastConstant(Ellipsis),
        )
        self.assertEqual(
            mcn.get_contents_md(),
            [
                mde.InlineElement("abc"),
                md_joiner,
                mde.CodeSpan("7"),
                md_joiner,
                mde.CodeSpan("'xyz'"),
                md_joiner,
                mde.InlineElement("…"),
            ],
        )

    def test_get_full_md(self) -> None:
        """.get_full_md() method – same as
        get_contents_md() in this base class
        """
        mcn = nodes.CompoundNode(
            nodes.MorastName("abc"),
            nodes.MorastConstant(7),
            nodes.MorastConstant("xyz"),
            nodes.MorastConstant(Ellipsis),
        )
        self.assertEqual(
            mcn.get_full_md(),
            mcn.get_contents_md(),
        )

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        md_joiner = mde.InlineElement(", ")
        mcn = nodes.CompoundNode(
            nodes.MorastName("abc"),
            nodes.MorastConstant(7),
            nodes.MorastConstant("xyz"),
            nodes.MorastConstant(Ellipsis),
        )
        self.assertEqual(
            mcn.as_markdown(),
            mde.CompoundInlineElement(
                mde.InlineElement("abc"),
                md_joiner,
                mde.CodeSpan("7"),
                md_joiner,
                mde.CodeSpan("'xyz'"),
                md_joiner,
                mde.InlineElement("…"),
            ),
        )


class MorastCall(TestCase):
    """MorastCall class"""

    def test_str(self) -> None:
        """string representation"""
        mcn = nodes.MorastCall(
            nodes.MorastNamespace(
                nodes.MorastName("namespace"),
                nodes.MorastName("func_name"),
            ),
            nodes.MorastName("abc"),
            nodes.MorastConstant(7),
            nodes.MorastConstant("xyz"),
            nodes.MorastConstant(Ellipsis),
        )
        self.assertEqual(
            str(mcn),
            "namespace.func_name(abc, 7, 'xyz', …)",
        )


class MorastDict(TestCase):
    """MorastDict class"""

    def test_str(self) -> None:
        """string representation"""
        mcd = nodes.MorastDict(
            ast.Dict(
                keys=[ast.Constant(value="a"), ast.Constant(value="c")],
                values=[ast.Constant(value="b"), ast.Constant(value=3)],
            )
        )
        self.assertEqual(
            str(mcd),
            "{'a': 'b', 'c': 3}",
        )

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        mcd = nodes.MorastDict(
            ast.Dict(
                keys=[ast.Constant(value="a"), ast.Constant(value="c")],
                values=[ast.Constant(value="b"), ast.Constant(value=3)],
            )
        )
        md_joiner = mde.InlineElement(", ")
        dict_item_joiner = mde.InlineElement(": ")
        self.assertEqual(
            mcd.as_markdown(),
            mde.CompoundInlineElement(
                mde.InlineElement("{"),
                mde.CodeSpan("'a'"),
                dict_item_joiner,
                mde.CodeSpan("'b'"),
                md_joiner,
                mde.CodeSpan("'c'"),
                dict_item_joiner,
                mde.CodeSpan("3"),
                mde.InlineElement("}"),
            ),
        )


class MorastSubscript(TestCase):
    """MorastSubscript class"""

    def test_str(self) -> None:
        """string representation"""
        msub = nodes.MorastSubscript(
            nodes.MorastName("sequence"),
            nodes.MorastConstant(17),
        )
        self.assertEqual(
            str(msub),
            "sequence[17]",
        )

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        msub = nodes.MorastSubscript(
            nodes.MorastName("mapping"),
            nodes.MorastConstant("key"),
        )
        self.assertEqual(
            msub.as_markdown(),
            mde.CompoundInlineElement(
                mde.InlineElement("mapping"),
                mde.InlineElement("["),
                mde.CodeSpan("'key'"),
                mde.InlineElement("]"),
            ),
        )


class MorastClassBases(TestCase):
    """MorastClassBases class"""

    def test_str(self) -> None:
        """string representation"""
        mcb = nodes.MorastClassBases("parent_1", "parent_2")
        self.assertEqual(
            str(mcb),
            "🏠 Inherits from: parent_1, parent_2",
        )

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        mcb = nodes.MorastClassBases("parent_1", "parent_2")
        md_joiner = mde.InlineElement(", ")
        self.assertEqual(
            mcb.as_markdown(),
            mde.CompoundInlineElement(
                mde.InlineElement("🏠 Inherits from: "),
                mde.InlineElement("parent_1"),
                md_joiner,
                mde.InlineElement("parent_2"),
            ),
        )


class MorastTuple(TestCase):
    """MorastTuple class"""

    def test_str(self) -> None:
        """string representation"""
        with self.subTest("empty tuple"):
            mtu = nodes.MorastTuple()
            self.assertEqual(
                str(mtu),
                "()",
            )
        #
        with self.subTest("2 names"):
            mtu = nodes.MorastTuple(
                nodes.MorastName("item_1"),
                nodes.MorastName("item_2"),
            )
            self.assertEqual(
                str(mtu),
                "item_1, item_2",
            )
        #
        with self.subTest("2 literals"):
            mtu = nodes.MorastTuple(
                nodes.MorastConstant("literal string"),
                nodes.MorastConstant(False),
            )
            self.assertEqual(
                str(mtu),
                "'literal string', False",
            )
        #
        with self.subTest("1 literal"):
            mtu = nodes.MorastTuple(nodes.MorastConstant("literal string"))
            self.assertEqual(
                str(mtu),
                "('literal string',)",
            )
        #

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        md_joiner = mde.InlineElement(", ")
        with self.subTest("empty tuple"):
            mtu = nodes.MorastTuple()
            self.assertEqual(
                mtu.as_markdown(),
                mde.CompoundInlineElement(
                    mde.InlineElement("("),
                    mde.InlineElement(")"),
                ),
            )
        #
        with self.subTest("2 names"):
            mtu = nodes.MorastTuple(
                nodes.MorastName("item_1"),
                nodes.MorastName("item_2"),
            )
            self.assertEqual(
                mtu.as_markdown(),
                mde.CompoundInlineElement(
                    mde.InlineElement("item_1"),
                    md_joiner,
                    mde.InlineElement("item_2"),
                ),
            )
        #
        with self.subTest("2 literals"):
            mtu = nodes.MorastTuple(
                nodes.MorastConstant("literal string"),
                nodes.MorastConstant(False),
            )
            self.assertEqual(
                mtu.as_markdown(),
                mde.CompoundInlineElement(
                    mde.CodeSpan("'literal string'"),
                    md_joiner,
                    mde.CodeSpan("False"),
                ),
            )
        #
        with self.subTest("1 literal"):
            mtu = nodes.MorastTuple(nodes.MorastConstant("literal string"))
            self.assertEqual(
                mtu.as_markdown(),
                mde.CompoundInlineElement(
                    mde.InlineElement("("),
                    mde.CodeSpan("'literal string'"),
                    mde.InlineElement(","),
                    mde.InlineElement(")"),
                ),
            )
        #


class MorastList(TestCase):
    """MorastList class"""

    def test_str(self) -> None:
        """string representation"""
        with self.subTest("empty list"):
            mli = nodes.MorastList()
            self.assertEqual(
                str(mli),
                "[]",
            )
        #
        with self.subTest("2 names"):
            mli = nodes.MorastList(
                nodes.MorastName("item_1"),
                nodes.MorastName("item_2"),
            )
            self.assertEqual(
                str(mli),
                "[item_1, item_2]",
            )
        #
        with self.subTest("2 literals"):
            mli = nodes.MorastList(
                nodes.MorastConstant("literal string"),
                nodes.MorastConstant(False),
            )
            self.assertEqual(
                str(mli),
                "['literal string', False]",
            )
        #

    def test_add(self) -> None:
        """.add() method"""
        mli = nodes.MorastList(
            nodes.MorastName("item_1"),
            nodes.MorastName("item_2"),
        )
        with self.subTest("before add"):
            self.assertEqual(
                str(mli),
                "[item_1, item_2]",
            )
        #
        mli.add(nodes.MorastName("item_3"))
        with self.subTest("after add"):
            self.assertEqual(
                str(mli),
                "[item_1, item_2, item_3]",
            )
        #


class MorastSet(TestCase):
    """MorastSet class"""

    def test_str(self) -> None:
        """string representation"""
        with self.subTest("empty set"):
            mse = nodes.MorastSet()
            self.assertEqual(
                str(mse),
                "set()",
            )
        #
        with self.subTest("2 names"):
            mse = nodes.MorastSet(
                nodes.MorastName("item_1"),
                nodes.MorastName("item_2"),
            )
            self.assertEqual(
                str(mse),
                "{item_1, item_2}",
            )
        #
        with self.subTest("2 literals"):
            mse = nodes.MorastSet(
                nodes.MorastConstant("literal string"),
                nodes.MorastConstant(False),
            )
            self.assertEqual(
                str(mse),
                "{'literal string', False}",
            )
        #

    def test_add(self) -> None:
        """.add() method"""
        mse = nodes.MorastSet(
            nodes.MorastName("item_1"),
            nodes.MorastName("item_2"),
        )
        with self.subTest("before add"):
            self.assertEqual(
                str(mse),
                "{item_1, item_2}",
            )
        #
        mse.add(nodes.MorastName("item_3"))
        with self.subTest("after add"):
            self.assertEqual(
                str(mse),
                "{item_1, item_2, item_3}",
            )
        #

    def test_as_markdown(self) -> None:
        """.as_markdown() method"""
        md_joiner = mde.InlineElement(", ")
        with self.subTest("empty set"):
            mse = nodes.MorastSet()
            self.assertEqual(
                mse.as_markdown(),
                mde.CompoundInlineElement(
                    mde.InlineElement("set()"),
                ),
            )
        #
        with self.subTest("2 names"):
            mse = nodes.MorastSet(
                nodes.MorastName("item_1"),
                nodes.MorastName("item_2"),
            )
            self.assertEqual(
                mse.as_markdown(),
                mde.CompoundInlineElement(
                    mde.InlineElement("{"),
                    mde.InlineElement("item_1"),
                    md_joiner,
                    mde.InlineElement("item_2"),
                    mde.InlineElement("}"),
                ),
            )
        #


# TODO: Assignment
# TODO: DocString
# TODO: Signature
# TODO: Advertisement


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
