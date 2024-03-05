# pylint: disable=too-many-lines
# -*- coding: utf-8 -*-

"""

morast.nodes

Documentation nodes generated from a module’s abstract syntax tree


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
import datetime
import logging
import re

from typing import Any, Dict, List, Optional, Type, Union

from smdg import elements as mde
from smdg import strings as mds

import morast


#
# Constants
#


BLANK = " "
EQUALS_OP = "="
EMPTY = ""
ARGS_JOINER = ", "

MD_ASSIGNMENT_NARROW = mde.InlineElement("=")
MD_ASSIGNMENT_BROAD = mde.InlineElement(" = ")
MD_DICT_ITEM_JOINER = mde.InlineElement(": ")
MD_ANNOTATION_JOINER = mde.InlineElement(": ")
MD_STAR = mde.InlineElement("*")
MD_RETURN_ARROW = mde.InlineElement(" → ")
MD_ARGS_JOINER = mde.InlineElement(ARGS_JOINER)
MD_HR20 = mde.HorizontalRule(20)
MD_HR60 = mde.HorizontalRule(60)

__all__ = [
    "MorastBinOp",
    "MorastDict",
    "MorastKeyword",
    "MorastCall",
    "MorastConstant",
    "MorastFormattedValue",
    "MorastJoinedStr",
    "MorastList",
    "MorastName",
    "MorastNamespace",
    "MorastStarred",
    "MorastSubscript",
    "MorastTuple",
    "MorastBaseNode",
    "MorastErrorNode",
]

OP_LOOKUP: Dict[Type, str] = {
    ast.Add: "+",
    ast.Sub: "+",
    ast.Mult: "*",
    ast.Div: "/",
    ast.FloorDiv: "//",
    ast.Mod: "%",
    ast.Pow: "**",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitOr: "|",
    ast.BitXor: "^",
    ast.BitAnd: "&",
    # TODO:  ast.MatMult: "@",
}


#
# Functions
#


def failsafe_mde(item: Any) -> mde.BaseElement:
    """Return a MarkDown element
    from an item of any type
    """
    if isinstance(item, MorastBaseNode):
        return item.as_markdown()
    #
    return mde.InlineElement(str(item))


def get_operator_text(operator_obj: ast.AST) -> str:
    """Return the string representation matching
    _operator\\_obj_, an ast binary operator object
    (`+`, `-`, `*`, `/`, etc)
    """
    return OP_LOOKUP[type(operator_obj)]


def get_augmentation_operator(operator_obj: ast.AST) -> str:
    """Return the string representation matching
    _operator\\_obj_, an ast binary operator object
    when used in an ast augmentation object
    (`+=`, `-=`, `*=`, `/=`, etc)
    """
    return f"{get_operator_text(operator_obj)}="


def get_node(element: Union[str, ast.AST]) -> "MorastBaseNode":
    """Return a MoRAST document Node
    for the provided _element_ which may be a string
    or an ast object.
    """
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-return-statements
    if isinstance(element, str):
        # name
        return MorastName(element)
    #
    if isinstance(element, ast.Name):
        # name
        return MorastName(element.id)
    #
    if isinstance(element, ast.Attribute):
        # namespaced name
        return MorastNamespace(get_node(element.value), get_node(element.attr))
    #
    if isinstance(element, ast.BinOp):
        # Binary operator
        return MorastBinOp(
            get_node(element.left), element.op, get_node(element.right)
        )
    #
    if isinstance(element, ast.Constant):
        # constant / literal
        return MorastConstant(element.value)
    #
    if isinstance(element, ast.Dict):
        # Dict representation
        return MorastDict(element)
    #
    if isinstance(element, ast.keyword):
        # keyword argument without annotation
        arg = getattr(element, "arg", None)
        return MorastKeyword(get_node(element.value), arg=arg)
    #
    if isinstance(element, ast.FormattedValue):
        # formatted value inside a format string
        conversion = getattr(element, "conversion", -1)
        format_spec = getattr(element, "format_spec", None)
        format_spec_items: List[str] = []
        if format_spec:
            format_spec_items.extend(
                str(get_node(item.value)) for item in format_spec
            )
        #
        return MorastFormattedValue(
            get_node(element.value), conversion, *format_spec_items
        )
    #
    if isinstance(element, ast.JoinedStr):
        # Format string consisting of literals and formatted values
        parts: List[Union[MorastConstant, MorastFormattedValue]] = []
        for item in element.values:
            current_node = get_node(item)
            if isinstance(
                current_node, (MorastConstant, MorastFormattedValue)
            ):
                parts.append(current_node)
            else:
                return MorastErrorNode(
                    f"Source line {element.lineno}:"
                    f" {ast.dump(item)} (in {ast.dump(element)})"
                    " not implemented yet"
                )
            #
        #
        return MorastJoinedStr(*parts)
    #
    if isinstance(element, (ast.List, ast.Set, ast.Tuple)):
        # List, Set or Tuple literal
        params: List[MorastBaseNode] = [
            get_node(item) for item in element.elts
        ]
        if isinstance(element, ast.List):
            target_class: Type[MorastBaseNode] = MorastList
        if isinstance(element, ast.Set):
            target_class = MorastSet
        else:
            target_class = MorastTuple
        #
        return target_class(*params)
    #
    if isinstance(element, ast.Starred):
        # Sinsle starred argument
        return MorastStarred(get_node(element.value))
    #
    if isinstance(element, ast.Subscript):
        # Subscripted object
        return MorastSubscript(
            get_node(element.value), get_node(element.slice)
        )
    #
    if isinstance(element, ast.Call):
        # function call
        params = []
        for arg_or_kw in element.args + element.keywords:
            params.append(get_node(arg_or_kw))
        #
        return MorastCall(get_node(element.func), *params)
    #
    return MorastErrorNode(
        f"Source line {element.lineno}:"
        f" {ast.dump(element)} not implemented yet"
    )


def remove_hanging_indent(text: str, level: int = 1) -> str:
    """Return a text block with hanging indent removed,
    which is used in conversion of docstrings.

    *   _text_: the source text
    *   _level_: the number of indent levels to decrease.
        Default is 1 (suitable for module-level classes and functions);
        for any type of methods, 2 is recommended choice.
        Values lower than 1 return the text block unchanged.

    One index unit is counted as 4 Spaces or one Tab.

        {
            Extra indent is preserved
            so embedding a code block in a docstring is possible,
            as shown right here.
        }
    """
    if level < 1:
        return text
    #
    prx_hanging_indent = re.compile(f"^(    |\\t){{{level}}}")
    fixed_lines: List[str] = []
    for index, line in enumerate(text.splitlines(keepends=True)):
        if index is None:
            fixed_lines.append(line)
            continue
        #
        fixed_lines.append(prx_hanging_indent.sub(EMPTY, line))
    #
    return EMPTY.join(fixed_lines)


#
# Classes
#


class MorastBaseNode:
    """Base class for all Morast nodes"""

    def __init__(self) -> None:
        """init method to be overridden in subclasses"""

    def __repr__(self) -> str:
        """Return as string representation"""
        return f"<{self.__class__.__name__} instance>"

    @property
    def quotes_required(self) -> bool:
        """Return True in subclasses if quotes are required"""
        return False

    def plain_display(self) -> str:
        """Return the plain display of the element"""
        as_str = str(self)
        if self.quotes_required:
            return repr(as_str)
        #
        return as_str

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown element repesenting the node.
        If not overridden, this method simlpy returns a
        MarkDown inline element from the string conversion of the object.
        """
        return mde.InlineElement(self.plain_display())


# pylint: disable=too-few-public-methods


class MorastErrorNode(MorastBaseNode):
    """Error element

    Initialization argument:

    * _message_: the error message which is stored as a public attribute
    """

    def __init__(self, message: str) -> None:
        """Store _message_ and log a warning"""
        logging.warning(message)
        self.message = message

    def as_markdown(self) -> mde.BaseElement:
        """Return the error message in a MarkDown paragraph"""
        return mde.Paragraph(self.message)


class MorastKeyword(MorastBaseNode):
    """Keyword argument from ast

    Initialization arguments:

    * _value_: the argument value
      (or the name to be prefixed with stars if arg is `None`)
    * _arg_: the argument name
    """

    def __init__(
        self, value: MorastBaseNode, arg: Optional[str] = None
    ) -> None:
        """Store _value_ and _arg_"""
        self._value = value
        self._arg = arg

    @property
    def prefix(self) -> str:
        """Prefix for the value
        (`arg=` or `**`), epending on the value of arg
        """
        if self._arg is None:
            return "**"
        #
        return f"{self._arg}="

    def __str__(self) -> str:
        """String conversion:
        either `arg=value` or `**value` if arg is `None`
        """
        return f"{self.prefix}{self._value}"


class MorastConstant(MorastBaseNode):
    """Literal constant from ast

    Initialization argument:

    * _value_: the value
    """

    def __init__(self, value: Any) -> None:
        """Store the value"""
        self._value = value

    @property
    def quotes_required(self) -> bool:
        """Quotes are required for string values"""
        return isinstance(self._value, str)

    def __str__(self) -> str:
        """String conversion"""
        if self._value is Ellipsis:
            return "…"
        #
        return str(self._value)

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown CodeSpan element
        from the string conversion of the value.
        For string values, use the _representation_
        of the string (ie. the string enclosed in quotes).
        For the special value _Ellipsis_, return
        an inline element containing representation as **…**
        """
        if self._value is Ellipsis:
            return mde.InlineElement(str(self))
        #
        return mde.CodeSpan(self.plain_display())


class MorastFormattedValue(MorastBaseNode):
    """Formatted value in an f-string

    Initialization arguments:

    * _value_: a MorastBaseNode subclass instance
      representing the value
    * _conversion_: the conversion character ASCII code as documented in
      <https://docs.python.org/3/library/ast.html#ast.FormattedValue>
    * _format\\_spec\\_items: the parts of the format\\_spec attribute
      (converted to strings before)
    """

    def __init__(
        self, value: MorastBaseNode, conversion: int, *format_spec_items: str
    ):
        """Store the values"""
        self._value = value
        modifier_parts: List[str] = []
        if conversion > -1:
            modifier_parts.append(f"!{chr(conversion)}")
        #
        if format_spec_items:
            modifier_parts.append(f":{EMPTY.join(format_spec_items)}")
        #
        self._modifiers = EMPTY.join(modifier_parts)

    @property
    def quotes_required(self) -> bool:
        """Quotes are required."""
        return True

    def __str__(self) -> str:
        """Return as string"""
        return f"{self._value}{self._modifiers}"

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown CodeSpan from the string representation"""
        return mde.CodeSpan(self.plain_display())


class MorastJoinedStr(MorastBaseNode):
    """An f-string

    Initialization arguments:

    * _parts_: the parts of the f-string
      (a sequence of MorastConstant and/or MorastFormattedValue
      instances)
    """

    def __init__(
        self,
        *parts: Union[MorastConstant, MorastFormattedValue],
    ):
        """Store the parts"""
        self._parts = parts

    @property
    def quotes_required(self) -> bool:
        """Quotes are required."""
        return True

    def __str__(self) -> str:
        """Return as string (parts simply joined together)"""
        return EMPTY.join(str(part) for part in self._parts)

    def plain_display(self) -> str:
        """Return the plain display of the element"""
        return f"f{super().plain_display()}"

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown CodeSpan element from the representation string"""
        return mde.CodeSpan(self.plain_display())


class MorastBinOp(MorastBaseNode):
    """Binary operator from ast"""

    def __init__(
        self, left: MorastBaseNode, operator_obj: Any, right: MorastBaseNode
    ) -> None:
        """Set the operator representation"""
        self._operator = f" {get_operator_text(operator_obj)} "
        self.left = left
        self.right = right

    def __str__(self) -> str:
        """Return as string"""
        return f"{self.left}{self._operator}{self.right}"


class MorastName(MorastBaseNode):
    """Name from ast"""

    def __init__(self, name: str) -> None:
        """Set the name"""
        self._name = name

    def __str__(self) -> str:
        """Return as string"""
        return self._name


class MorastNamespace(MorastBaseNode):
    """Namespace(d name) from ast"""

    def __init__(
        self, namespace: MorastBaseNode, descendant: MorastBaseNode
    ) -> None:
        """Set the name"""
        self._namespace = namespace
        self._descendant = descendant

    def strip_first(self) -> MorastBaseNode:
        """Return the descendant only"""
        return self._descendant

    def __str__(self) -> str:
        """Return as string"""
        return f"{self._namespace}.{self._descendant}"


class MorastDictItem(MorastBaseNode):
    """Dict item from ast"""

    def __init__(
        self, key: Optional[ast.AST], value: Optional[ast.AST]
    ) -> None:
        """Set the name"""
        self._kwarg: Optional[MorastBaseNode] = None
        self._key: Optional[MorastBaseNode] = None
        self._value: Optional[MorastBaseNode] = None
        if isinstance(value, ast.AST):
            value_node = get_node(value)
        else:
            value_node = MorastBaseNode()
        #
        if key is None:
            self._kwarg = MorastKeyword(value_node)
        else:
            self._key = get_node(key)
            self._value = value_node
        #

    def __str__(self) -> str:
        """Return as string"""
        if isinstance(self._key, MorastBaseNode) and isinstance(
            self._value, MorastBaseNode
        ):
            return (
                f"{self._key.plain_display()}:"
                f" {self._value.plain_display()}"
            )
        #
        if isinstance(self._kwarg, MorastBaseNode):
            return str(self._kwarg)
        #
        raise ValueError("invalid DictItem – should not happen")

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown element"""
        if isinstance(self._kwarg, MorastBaseNode):
            return self._kwarg.as_markdown()
        #
        key = failsafe_mde(self._key)
        value = failsafe_mde(self._value)
        return mde.CompoundInlineElement(key, MD_DICT_ITEM_JOINER, value)


class MorastStarred(MorastBaseNode):
    """Starred item"""

    def __init__(
        self,
        *value: MorastBaseNode,
    ):
        """Store the value"""
        self._value = value

    def __str__(self) -> str:
        """Return as string"""
        return f"*{self._value}"


class CompoundNode(MorastBaseNode):
    """Element containing a number of other ones"""

    prefix_node: Optional[MorastBaseNode] = None
    opener: str = EMPTY
    closer: str = EMPTY
    joiner: str = ARGS_JOINER
    add_supported: bool = False

    def __init__(self, *contents: MorastBaseNode) -> None:
        """set name and contents"""
        self._contents = list(contents)

    def __str__(self) -> str:
        """String representation"""
        str_all: List[str] = []
        if self.prefix_node is not None:
            str_all.append(str(self.prefix_node))
        #
        if self.opener:
            str_all.append(self.opener)
        #
        str_all.extend(self.get_contents())
        if self.closer:
            str_all.append(self.closer)
        #
        return EMPTY.join(str_all)

    def add(self, element: MorastBaseNode) -> None:
        """add the new element"""
        if self.add_supported:
            self._contents.append(element)
        else:
            raise ValueError("Adding elements not supported")
        #

    def get_contents(self) -> List[str]:
        """Return a list of strings from contents,
        including joiners
        """
        str_contents: List[str] = []
        for index, element in enumerate(self._contents):
            if index > 0 and len(self.joiner) > 0:
                str_contents.append(self.joiner)
            #
            str_contents.append(element.plain_display())
        #
        return str_contents

    def get_contents_md(self) -> List[mde.BaseElement]:
        """Return a list of MarkDown elements from contents,
        including joiners
        """
        contents_joiner = mde.InlineElement(self.joiner)
        md_contents: List[mde.BaseElement] = []
        for index, element in enumerate(self._contents):
            if index > 0 and len(contents_joiner) > 0:
                md_contents.append(contents_joiner)
            #
            md_contents.append(element.as_markdown())
        #
        return md_contents

    def get_full_md(self) -> List[mde.BaseElement]:
        """Return a list of MarkDown elements including prefix,
        opener and closer
        """
        md_all: List[mde.BaseElement] = []
        if self.prefix_node is not None:
            md_all.append(self.prefix_node.as_markdown())
        #
        if self.opener:
            md_all.append(mde.InlineElement(self.opener))
        #
        md_all.extend(self.get_contents_md())
        if self.closer:
            md_all.append(mde.InlineElement(self.closer))
        #
        return md_all

    def as_markdown(self) -> mde.BaseElement:
        """Return a compound markdown element"""
        return mde.CompoundInlineElement(*self.get_full_md())


class MorastCall(CompoundNode):
    """Function (or other callable) call from ast"""

    opener = "("
    closer = ")"

    def __init__(self, func: MorastBaseNode, *params: MorastBaseNode) -> None:
        """set name and contents"""
        super().__init__(*params)
        # self._func = func
        self.prefix_node = func


class MorastDict(CompoundNode):
    """Dict from ast"""

    opener = "{"
    closer = "}"

    def __init__(
        self,
        ast_dict_obj: ast.Dict,
    ) -> None:
        """set name and contents"""
        dict_items: List[MorastBaseNode] = []
        for index, single_key in enumerate(ast_dict_obj.keys):
            dict_items.append(
                MorastDictItem(single_key, ast_dict_obj.values[index])
            )
        #
        super().__init__(*dict_items)


class MorastSubscript(CompoundNode):
    """Subscript from ast"""

    opener = "["
    closer = "]"

    def __init__(self, value: MorastBaseNode, slice_: MorastBaseNode) -> None:
        """set name and contents"""
        super().__init__(slice_)
        # self._value = value
        self.prefix_node = value


class MorastClassBases(CompoundNode):
    """Class bases from ast

    🌱
    """

    prefix_node = MorastName("🏠 Inherits from: ")
    opener = ""
    closer = ""

    def __init__(self, *bases) -> None:
        """set name and contents"""
        super().__init__(*(get_node(single_base) for single_base in bases))


class MorastTuple(CompoundNode):
    """Tuple from ast"""

    opener = "("
    closer = ")"

    def __init__(self, *contents: MorastBaseNode) -> None:
        """Store contents, and avoid parentheses
        if more thon one element was provided
        """
        super().__init__(*contents)
        if len(self._contents) > 1:
            self.opener = self.closer = EMPTY
        #

    def get_contents(self) -> List[str]:
        """Return a list of strings from contents,
        including joiners.
        Append a trailing comma to length-1 tuples.
        """
        str_contents: List[str] = super().get_contents()
        if len(self._contents) == 1:
            str_contents.append(",")
        #
        return str_contents

    def get_contents_md(self) -> List[mde.BaseElement]:
        """Return a list of MarkDown elements from contents,
        including joiners.
        Append a trailing comma to length-1 tuples.
        """
        md_contents: List[mde.BaseElement] = super().get_contents_md()
        if len(self._contents) == 1:
            md_contents.append(mde.InlineElement(","))
        #
        return md_contents


class MorastList(CompoundNode):
    """List from ast"""

    opener = "["
    closer = "]"
    add_supported = True


class MorastSet(CompoundNode):
    """Set from ast"""

    opener = "{"
    closer = "}"
    add_supported = True

    def __str__(self) -> str:
        """String representation"""
        if len(self._contents) < 1:
            return "set()"
        #
        return super().__str__()

    def get_full_md(self) -> List[mde.BaseElement]:
        """Return a list of MarkDown elements including prefix,
        opener and closer
        """
        if len(self._contents) < 1:
            return [mde.InlineElement("set()")]
        #
        return super().get_full_md()


class Assignment(MorastBaseNode):
    """Represents an assignment"""

    def __init__(
        self,
        element: Union[ast.Assign, ast.AnnAssign, ast.AugAssign],
        prefix: str = "",
    ) -> None:
        """Store the assignment parts"""
        self.target: MorastBaseNode = MorastName("...")
        self.prefix = prefix
        self.operator: Optional[str] = EQUALS_OP
        self.annotation: Optional[MorastBaseNode] = None
        self.value: Optional[MorastBaseNode] = None
        declared_value = getattr(element, "value", None)
        if declared_value is not None:
            self.value = get_node(declared_value)
        #
        self.__target_list: List[MorastBaseNode] = []
        if isinstance(element, ast.Assign):
            self.__target_list.extend(
                get_node(single_target) for single_target in element.targets
            )
            self.target = self.__target_list[0]
        elif isinstance(element, ast.AnnAssign):
            self.target = get_node(element.target)
            if declared_value is None:
                self.operator = None
            #
            self.annotation = get_node(element.annotation)
        elif isinstance(element, ast.AugAssign):
            self.target = get_node(element.target)
            self.operator = get_augmentation_operator(element.op)
        #
        if not self.__target_list:
            self.__target_list.insert(0, self.target)
        #

    def strip_first(self) -> None:
        """Strip the first namespace part from the first target"""
        if isinstance(self.target, MorastNamespace):
            self.target = self.target.strip_first()
            try:
                self.__target_list[0] = self.target
            except IndexError:
                self.__target_list.append(self.target)
            #
        #

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown representation"""
        parts: List[mde.BaseElement] = []
        if self.prefix:
            parts.append(mde.InlineElement(self.prefix))
        #
        for index, single_target in enumerate(self.__target_list):
            if index:
                parts.append(MD_ASSIGNMENT_BROAD)
            #
            parts.append(mde.BoldText(single_target.as_markdown()))
        #
        if self.annotation is not None:
            parts.extend(
                (
                    mde.InlineElement(": "),
                    self.annotation.as_markdown(),
                )
            )
        #
        if self.operator is not None:
            if isinstance(self.value, MorastBaseNode):
                parts.extend(
                    (
                        mde.InlineElement(f" {self.operator} "),
                        self.value.as_markdown(),
                    )
                )
            #
        #
        return mde.CompoundInlineElement(*parts)


class DocString(MorastBaseNode):
    """Represents a Docstring"""

    def __init__(
        self,
        expression: Union[ast.Expr, str],
        level: int = 1,
        sanitize: bool = False,
    ) -> None:
        """Store the content"""
        if isinstance(expression, str):
            content = expression
        elif isinstance(expression.value, ast.Constant):
            content = expression.value.value
        else:
            raise ValueError("Must be a constant expression!")
        #
        if level < 1:
            raise ValueError("level must be 1 or greater")
        #
        self._level = level
        if sanitize:
            self._sane_content = mds.sanitize(content)
        else:
            self._sane_content = mds.declare_as_safe(content)
        #

    def adjust_level(self, new_level: int) -> None:
        """Change the level to _new\\_level_"""
        if new_level < 1:
            raise ValueError("level must be 1 or greater")
        #
        self._level = new_level

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown representation"""
        content = remove_hanging_indent(
            str(self._sane_content), self._level - 2
        )
        return mde.BlockQuote(mds.declare_as_safe(content))


class Signature(MorastBaseNode):
    """Represents the signature of a class or function"""

    # pylint: disable = too-many-arguments
    def __init__(
        self,
        name: str,
        arguments: ast.arguments,
        returns: Any,
        prefix: Optional[str] = None,
        skip_first_arg: bool = False,
    ) -> None:
        """Store the content"""
        self.name = name
        self._prefix = prefix
        self.args: List[mde.BaseElement] = []
        if arguments.posonlyargs:
            self.args.extend(
                mde.ItalicText(get_node(item.arg).as_markdown())
                for item in arguments.posonlyargs
            )
        #
        if arguments.args and arguments.posonlyargs:
            self.args.append(mde.InlineElement("/"))
        #
        self._add_args(arguments.args, arguments.defaults, from_backwards=True)
        vararg = getattr(arguments, "vararg", None)
        kwarg = getattr(arguments, "kwarg", None)
        if isinstance(vararg, ast.arg):
            self._add_starred_arg(vararg)
        elif (arguments.posonlyargs or arguments.args) and (
            arguments.kwonlyargs or kwarg
        ):
            self.args.append(MD_STAR)
        #
        # add kwonlyargs
        self._add_args(
            arguments.kwonlyargs, arguments.kw_defaults, from_backwards=False
        )
        #
        if isinstance(kwarg, ast.arg):
            self._add_starred_arg(kwarg, 2)
        #
        if skip_first_arg:
            try:
                self.args.pop(0)
            except IndexError:
                logging.warning(
                    "Source line %s (%s): Skipping first arg failed",
                    arguments.lineno,
                    ast.dump(arguments),
                )
            #
        #
        self.returns: Optional[MorastBaseNode] = None
        if returns is not None:
            self.returns = get_node(returns)
        #

    def _add_starred_arg(self, arg_to_star, nstars: int = 1) -> None:
        """Add an argument to maybe-be-starred"""
        annotation = getattr(arg_to_star, "annotation", None)
        prefix_stars = [MD_STAR] * nstars
        compound_arg_parts: List[mde.BaseElement] = [
            mde.ItalicText(
                mde.CompoundInlineElement(
                    *prefix_stars, get_node(arg_to_star.arg).as_markdown()
                )
            )
        ]
        if isinstance(annotation, ast.AST):
            compound_arg_parts.extend(
                (
                    MD_ANNOTATION_JOINER,
                    get_node(annotation).as_markdown(),
                )
            )
        #
        self.args.append(mde.CompoundInlineElement(*compound_arg_parts))

    def _add_args(self, args, defaults, from_backwards=False) -> None:
        """Add args or kwonlyargs"""
        nargs = len(args)
        for index, arg in enumerate(args):
            r_index = index - nargs
            used_index = r_index if from_backwards else index
            if not isinstance(arg, ast.arg):
                if isinstance(arg, ast.AST):
                    logging.warning(
                        "Source line %s (%s): Unhandled arg",
                        arg.lineno,
                        ast.dump(arg),
                    )
                else:
                    logging.warning("Unhandled arg: %r", arg)
                #
            #
            arg_element = get_node(arg.arg).as_markdown()
            annotation = getattr(arg, "annotation", None)
            try:
                ast_default = defaults[used_index]
            except IndexError:
                default: Optional[MorastBaseNode] = None
            else:
                default = get_node(ast_default)
            #
            arg_element = mde.ItalicText(arg_element)
            if annotation is None and default is None:
                self.args.append(arg_element)
                continue
            #
            compound_arg_parts: List[mde.BaseElement] = [arg_element]
            if annotation is None:
                assignment_element = MD_ASSIGNMENT_NARROW
            else:
                assignment_element = MD_ASSIGNMENT_BROAD
                compound_arg_parts.extend(
                    (
                        MD_ANNOTATION_JOINER,
                        get_node(annotation).as_markdown(),
                    )
                )
            #
            if default is not None:
                compound_arg_parts.extend(
                    (assignment_element, default.as_markdown())
                )
            #
            self.args.append(mde.CompoundInlineElement(*compound_arg_parts))
        #

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown representation"""
        # joiner = mde.InlineElement(ARGS_JOINER)
        output_args: List[mde.BaseElement] = []
        for index, single_elem in enumerate(self.args):
            if index:
                output_args.append(MD_ARGS_JOINER)
            #
            if isinstance(single_elem, mde.CompoundElement):
                output_args.extend(single_elem.flattened())
            else:
                output_args.append(single_elem)
            #
        #
        return_annotation: List[mde.BaseElement] = []
        if self.returns is not None:
            return_annotation.extend(
                (
                    MD_RETURN_ARROW,
                    self.returns.as_markdown(),
                )
            )
        #
        name_parts: List[mde.InlineElement] = []
        if self._prefix is not None:
            name_parts.append(mde.InlineElement(self._prefix))
        #
        name_parts.append(mde.BoldText(self.name))
        # logging.warning(repr(name_parts[-1]))
        # logging.warning(str(name_parts[-1]))
        # args = ARGS_JOINER.join(self.args)
        inline_element = mde.CompoundInlineElement(
            "📖 ",
            *name_parts,
            mde.SAFE_LP,
            *output_args,
            mde.SAFE_RP,
            *return_annotation,
        )
        return mde.BlockQuote(
            MD_HR60,
            inline_element,
            MD_HR60,
        )


class Advertisement(MorastBaseNode):
    """Represents the advertisement at the end of the output"""

    def as_markdown(self) -> mde.BaseElement:
        """Return a MarkDown representation"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        return mde.BlockElement(
            MD_HR60,
            mde.Paragraph(
                mde.ItalicText(
                    mde.CompoundInlineElement(
                        "📢 Module contents extracted ",
                        mde.BoldText(today),
                        " by ",
                        mde.BoldText(
                            mde.Link(
                                f"{morast.BRAND} v{morast.__version__}",
                                ref="morast-pypi",
                            )
                        ),
                    )
                )
            ),
            mde.Label("morast-pypi", morast.PYPI_URL),
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
