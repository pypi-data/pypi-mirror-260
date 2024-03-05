# -*- coding: utf-8 -*-

"""

morast.core

Core functionality


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
import collections
import logging
import pathlib

from threading import Lock
from typing import Any, Dict, Iterator, List, Optional, Tuple, Union

from smdg import elements as mde

from morast import BRAND
from morast import nodes


#
# Constants
#


UNDERLINE = "_"

CLASS_METHOD = 0
STATIC_METHOD = 1
INSTANCE_METHOD = 2
MODULE_LEVEL_FUNCTION = 9

METHODS: Tuple[int, int, int] = (CLASS_METHOD, STATIC_METHOD, INSTANCE_METHOD)
METHOD_TYPES: Tuple[str, str, str] = (
    "Class method",
    "Static method",
    "Instance method",
)

TYPES_BY_DECORATOR: Dict[str, int] = {
    "classmethod": CLASS_METHOD,
    "staticmethod": STATIC_METHOD,
}

KW_CLASS = "class"
KW_INSTANCE = "instance"

EXCLUDED_MODULE_VARIABLES: Tuple[str, ...] = ("__all__",)


#
# Functions
#


def morast_prefix(name: str) -> str:
    """Prefix _name_ with `'MoRAST:'`"""
    return f"{BRAND}:{name}"


MORAST_BASES = morast_prefix("bases")
MORAST_DOCSTRING = morast_prefix("docstring")
MORAST_SIGNATURE = morast_prefix("signature")
MORAST_ADVERTISEMENT = morast_prefix("generator")


def camel_to_snake_case(name: str) -> str:
    """Convert _name_ (an identifier) from CamelCase
    to lower\\_snake\\_case
    """
    output_collector: List[str] = []
    for index, character in enumerate(name):
        if character.isupper():
            character = character.lower()
            if index:
                output_collector.append(UNDERLINE)
            #
        output_collector.append(character)
    #
    return "".join(output_collector)


#
# Classes
#


class MorastSection:
    """Documentation section with a headline and other nodes.
    May also contain other sections.

    Initialization arguments:

    * _name_: the name of the section (public attribute)
    * _level_: section level in the document hierarchy
    * _headline_: deviant headline if provided
      (else, the headline will just be _name_)

    Keeps an internal collection of contained
    MorastBaseNode and MorastSection instances.
    """

    def __init__(
        self, name: str, level: int = 1, headline: Optional[str] = None
    ) -> None:
        """Store the attributes and initialize
        the internal collection of contained items.
        """
        self.name = name
        if isinstance(headline, str):
            self._headline = headline
        else:
            self._headline = name
        #
        self._level = level
        self._contents: collections.OrderedDict[
            str, Union[nodes.MorastBaseNode, "MorastSection"]
        ] = collections.OrderedDict()
        self._naming_lock = Lock()

    def __getitem__(
        self,
        name: str,
    ) -> Union[nodes.MorastBaseNode, "MorastSection"]:
        """Directly return the node or subsection stored as _name_"""
        return self._contents[name]

    def __len__(self) -> int:
        """Total number of contained nodes and subsections"""
        return len(self._contents)

    def items(
        self,
    ) -> Iterator[Tuple[str, Union[nodes.MorastBaseNode, "MorastSection"]]]:
        """Return an iterator (_name_, _item_ tuples)
        over all contained nodes and subsections
        """
        yield from self._contents.items()

    def subsections(self) -> Iterator[Tuple[str, "MorastSection"]]:
        """Return an iterator (_name_, _subsection_ tuples)
        over all contained subsections"""
        for sub_name, subnode in self.items():
            if isinstance(subnode, MorastSection):
                yield sub_name, subnode
            #
        #

    def adjust_level(self, new_level: int) -> None:
        """Change the level to _new\\_level_,
        recurse into all subsections and
        propagate the change.
        If a docstring is present,
        adjust its level as well.
        """
        self._level = new_level
        for _, child_section in self.subsections():
            child_section.adjust_level(new_level + 1)
        #
        try:
            docstring = self[MORAST_DOCSTRING]
        except KeyError:
            return
        #
        if isinstance(docstring, nodes.DocString):
            docstring.adjust_level(new_level)
        #

    def _get_unique_name(self, name: str) -> str:
        """Return a new unique name instead of _name_.
        Should be called only while holding `self._naming_lock`.
        """
        number = 0
        candidate = name
        while candidate in self._contents:
            number += 1
            candidate = f"{name}_{number}"
            if number > 1000:
                raise ValueError("Exhausted renaming attempts")
            #
        #
        return candidate

    def add_subnode(
        self,
        name: str,
        subitem: Union[nodes.MorastBaseNode, "MorastSection"],
    ) -> None:
        """Add _subitem_ (a node or section)
        and make it accessible through _name_.
        """
        self._contents.setdefault(name, subitem)
        if subitem is not self._contents[name]:
            with self._naming_lock:
                unique_name = self._get_unique_name(name)
                self._contents[unique_name] = subitem
            #
        #

    def add_subsection(
        self,
        name: str = "undefined",
        subsection: Optional["MorastSection"] = None,
    ) -> None:
        """Add a new subsection.
        If a MorastSection instance is provided through _subsection_,
        store it, make it available under its own name,
        and adjust its level to reflect the sections hierarchy.
        else initialize a new one and and make it available as _name_.
        """
        if subsection is None:
            subsection = MorastSection(name, level=self._level + 1)
        else:
            sub_name = subsection.name
            subsection.adjust_level(self._level + 1)
        #
        self.add_subnode(sub_name, subsection)

    def markdown_elements(self) -> Iterator[mde.BaseElement]:
        """Return an iterator over MarkDown elements for all
        contained nodes, recursing into all subsections.
        """
        if self._level > 1:
            yield nodes.MD_HR20
        #
        logging.info("Section: %r", self.name)
        yield mde.Header(self._level, self._headline)
        for sub_name, sub_element in self._contents.items():
            logging.info("MarkDown Element: %r", sub_name)
            if isinstance(sub_element, MorastSection):
                yield from sub_element.markdown_elements()
            else:
                yield sub_element.as_markdown()
            #
        #


class MorastFunctionDef(MorastSection):
    """Represents a module-level function,
    or a class, static, or instance method.

    Initialization arguments:

    * _element_: the ast.FunctionDef instance from which
      the function name, signature and docstring are determined
    * _level_: the level in the document hierarchy:
      `3` for module-level functions,
      `4` for methods
    * _function\\_type_: the function type
    * _parent\\_name_: the name of the containing parent (module or class)
    """

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-branches
    def __init__(
        self,
        element: ast.FunctionDef,
        level: int = 3,
        function_type: int = MODULE_LEVEL_FUNCTION,
        parent_name: str = "",
    ) -> None:
        """Determine and store attributes"""
        # Evaluate function_type and parent_class_name
        try:
            mtype_desc = METHOD_TYPES[function_type]
        except IndexError:
            mtype_desc = "Module-level function"
            function_type = MODULE_LEVEL_FUNCTION
        #
        name = element.name
        if function_type in METHODS:
            msg_prefix = f"{parent_name} class: "
        else:
            msg_prefix = ""
        #
        logging.info("%saccepted %s %r", msg_prefix, mtype_desc.lower(), name)
        skip_first_arg = False
        if function_type in (CLASS_METHOD, INSTANCE_METHOD):
            skip_first_arg = True
        #
        if function_type == INSTANCE_METHOD:
            headline_prefix = f"{camel_to_snake_case(parent_name)}_instance."
            signature_prefix = "."
        else:
            signature_prefix = f"{parent_name}."
            if function_type == MODULE_LEVEL_FUNCTION:
                headline_prefix = "Function: "
            else:
                headline_prefix = signature_prefix
            #
        #
        if function_type == STATIC_METHOD:
            signature_prefix = f"staticmethod {signature_prefix}"
        #
        super().__init__(
            name,
            level=level,
            headline=f"{headline_prefix}{name}()",
        )
        docstring: Optional[nodes.DocString] = None
        for sub_element in element.body:
            if isinstance(sub_element, ast.Expr):
                try:
                    docstring = nodes.DocString(sub_element, level=self._level)
                except ValueError:
                    continue
                else:
                    break
                #
            #
        #
        self.add_subnode(
            MORAST_SIGNATURE,
            nodes.Signature(
                self.name,
                element.args,
                returns=element.returns,
                prefix=signature_prefix,
                skip_first_arg=skip_first_arg,
            ),
        )
        if docstring is not None:
            self.add_subnode(MORAST_DOCSTRING, docstring)
        #


class MorastClassDef(MorastSection):
    """Represents a class.

    Initialization arguments:

    * _element_: the ast.ClassDef instance from which
      the class name, signature, docstring, attributes
      and methods are determined
    * _level_: the level in the document hierarchy: `3`
    * _signature\\_prefix_: prefix for the signature
    """

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=too-many-locals

    def __init__(
        self,
        element: ast.ClassDef,
        level: int = 3,
        signature_prefix: str = "",
    ) -> None:
        """Determine and store attributes"""
        name = element.name
        super().__init__(
            name,
            level=level,
            headline=f"Class {name}()",
        )
        decorators: List[nodes.MorastBaseNode] = [
            nodes.get_node(single_dec) for single_dec in element.decorator_list
        ]
        self.is_a_dataclass = False
        for item in decorators:
            if str(item) in ("dataclass", "dataclasses.dataclass"):
                self.is_a_dataclass = True
            #
        #
        class_prefix = "Dataclass" if self.is_a_dataclass else "Class"
        super().__init__(
            name,
            level=level,
            headline=f"{class_prefix} {name}()",
        )
        self.signature_prefix = signature_prefix
        docstring: Optional[nodes.DocString] = None
        init_method: Optional[ast.FunctionDef] = None
        # self.body_elements: List[MorastBaseNode] = []
        class_attrs = MorastSection(
            f"{KW_CLASS} attributes", level=self._level + 1
        )
        self.instance_attrs = MorastSection(
            f"{KW_INSTANCE} attributes", level=self._level + 1
        )
        class_methods = MorastSection(f"{KW_CLASS} methods", level=self._level)
        instance_methods = MorastSection(
            f"{KW_INSTANCE} methods", level=self._level
        )
        target_collections: Dict[int, MorastSection] = {
            CLASS_METHOD: class_methods,
            STATIC_METHOD: class_methods,
            INSTANCE_METHOD: instance_methods,
        }
        attribute_targets: Dict[str, MorastSection] = {
            KW_CLASS: class_attrs,
            KW_INSTANCE: self.instance_attrs,
        }
        attributes_dest = KW_INSTANCE if self.is_a_dataclass else KW_CLASS
        for sub_element in element.body:
            if isinstance(sub_element, ast.Expr) and docstring is None:
                try:
                    docstring = nodes.DocString(sub_element, level=self._level)
                except ValueError:
                    continue
                #
            #
            if isinstance(
                sub_element, (ast.Assign, ast.AnnAssign, ast.AugAssign)
            ):
                class_ass = nodes.Assignment(
                    sub_element, prefix=f"🧩 {self.name}."
                )
                target = str(class_ass.target)
                if target.startswith(UNDERLINE):
                    logging.info(
                        "%s class: ignored private %s attribute %r",
                        self.name,
                        attributes_dest,
                        target,
                    )
                    continue
                #
                logging.info(
                    "%s class: accepted %s attribute %r",
                    self.name,
                    attributes_dest,
                    target,
                )
                attribute_targets[attributes_dest].add_subnode(
                    target, class_ass
                )
                attribute_targets[attributes_dest].add_subnode(
                    f"{MORAST_DOCSTRING}:{target}",
                    nodes.DocString(
                        f"🚧 TODO: write {target} documentation",
                        sanitize=True,
                    ),
                )
            #
            if isinstance(sub_element, ast.FunctionDef):
                method_name = str(sub_element.name)
                # logging.warning("%r method %r", self.name, method_name)
                if method_name == "__init__":
                    init_method = sub_element
                    continue
                #
                if method_name.startswith(UNDERLINE):
                    logging.info(
                        "%s class: ignored private method %r",
                        self.name,
                        method_name,
                    )
                    continue
                #

                for dec in sub_element.decorator_list:
                    if isinstance(dec, ast.Name):
                        try:
                            method_type = TYPES_BY_DECORATOR[dec.id]
                        except KeyError:
                            continue
                        #
                        break
                    #
                else:
                    method_type = INSTANCE_METHOD
                #
                target_collections[method_type].add_subsection(
                    subsection=MorastFunctionDef(
                        sub_element,
                        level=4,
                        function_type=method_type,
                        parent_name=self.name,
                    )
                )
            #
            #
        #
        # TODO: handle inheritance
        bases: List[Any] = getattr(element, "bases", [])
        if bases:
            self.add_subnode(MORAST_BASES, nodes.MorastClassBases(*bases))
        #
        if isinstance(init_method, ast.FunctionDef):
            self._add_signature(init_method)
        #
        if docstring is not None:
            self.add_subnode(MORAST_DOCSTRING, docstring)
        #
        for subsection in (
            class_attrs,
            self.instance_attrs,
        ):
            if len(subsection):
                self.add_subsection(subsection=subsection)
            #
        #
        for subsection in (
            class_methods,
            instance_methods,
        ):
            for method_name, method in subsection.subsections():
                self.add_subsection(method_name, method)
            #
        #

    def _add_signature(self, init_method: ast.FunctionDef) -> None:
        """Add the signature"""
        instance_vars = set()
        for init_statement in init_method.body:
            if isinstance(init_statement, (ast.Assign, ast.AnnAssign)):
                try:
                    init_ass = nodes.Assignment(
                        init_statement,
                        prefix="🧩 .",
                    )
                except ValueError:
                    continue
                #
                target = str(init_ass.target)
                if not target.startswith("self."):
                    continue
                #
                init_ass.strip_first()
                target = str(init_ass.target)
                if target.startswith(UNDERLINE):
                    logging.info(
                        "%s class: ignored private instance attribute %r",
                        self.name,
                        target,
                    )
                    continue
                #
                if target not in instance_vars:
                    self.instance_attrs.add_subnode(target, init_ass)
                    self.instance_attrs.add_subnode(
                        f"{MORAST_DOCSTRING}:{target}",
                        nodes.DocString(
                            f"🚧 TODO: write {target} documentation",
                            sanitize=True,
                        ),
                    )
                    instance_vars.add(target)
                    logging.info(
                        "%s class: accepted instance attribute %r",
                        self.name,
                        target,
                    )
                #
            #
        #
        self.add_subnode(
            MORAST_SIGNATURE,
            nodes.Signature(
                self.name,
                init_method.args,
                returns=None,
                prefix=self.signature_prefix,
                skip_first_arg=True,
            ),
        )


class MorastModule(MorastSection):
    """Represents a module in the document tree

    Initialization arguments:

    * _module_: an ast.Module instance from which this instance is built
    * _name_: the module name (public attribute)
    * _namespace_: the module namespace (only used in the headline)
    * _advertise_: append a line specifying which MoRAST version was used
      to extract the documentation from the source module (disabled by default)
    * _excluded\\_module\\_variables_: excluded module-level variables
      (usually constants, defaults to EXCLUDED\\_MODULE\\_VARIABLES)
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        module: ast.Module,
        name: str,
        namespace: str = "",
        advertise: bool = False,
        excluded_module_variables: Tuple[str, ...] = EXCLUDED_MODULE_VARIABLES,
    ) -> None:
        """Pretty print a parsed module"""
        namespace_prefix = f"{namespace}." if namespace else ""
        super().__init__(
            name, level=1, headline=f"Module {namespace_prefix}{name}"
        )
        docstring: Optional[nodes.DocString] = None
        self.module_contents = MorastSection("Module contents", level=2)
        self.classes = MorastSection("Classes", level=2)
        self.functions = MorastSection("Functions", level=2)
        self._excluded_module_variables = excluded_module_variables
        for element in module.body:
            if docstring is None and isinstance(element, ast.Expr):
                try:
                    docstring = nodes.DocString(element, level=self._level)
                except ValueError as error:
                    logging.error(str(error))
                    continue
                #
                self.add_subnode(MORAST_DOCSTRING, docstring)
            else:
                try:
                    self._add_element(element)
                except TypeError as error:
                    logging.info(str(error))
                #
            #
        #
        for subsection in (self.module_contents, self.functions, self.classes):
            if len(subsection):
                self.add_subsection(subsection=subsection)
            #
        #
        if advertise:
            self.add_subnode(MORAST_ADVERTISEMENT, nodes.Advertisement())
        #

    def _add_element(self, element: ast.AST) -> None:
        """Add _element_ to the body blocks.
        Currently, ast assignment
        (ie. ast.Assign, ast.AnnAssign, ast.AugAssign),
        ast.ClassDef and ast.FunctionDef instances are supported.
        """
        if isinstance(element, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            assignment = nodes.Assignment(element, prefix=f"🧩 {self.name}.")
            target = str(assignment.target)
            if target in self._excluded_module_variables:
                raise TypeError(f"Excluded {target!r} as configured")
            #
            self.module_contents.add_subnode(target, assignment)
            self.module_contents.add_subnode(
                f"{MORAST_DOCSTRING}:{target}",
                nodes.DocString(
                    f"🚧 TODO: write {target} documentation",
                    sanitize=True,
                ),
            )
        elif isinstance(element, ast.ClassDef):
            self.classes.add_subsection(
                subsection=MorastClassDef(
                    element, signature_prefix=f"{self.name}.", level=3
                )
            )
        elif isinstance(element, ast.FunctionDef):
            self.functions.add_subsection(
                subsection=MorastFunctionDef(
                    element, parent_name=self.name, level=3
                )
            )
        else:
            raise TypeError(f"{type(element)} not supported yet")
        #

    def render(self) -> str:
        """Generate MarkDown output from this instance"""
        return mde.render(*self.markdown_elements())

    @classmethod
    def from_file(
        cls,
        path: pathlib.Path,
        encoding: str = "utf-8",
        **kwargs,
    ) -> "MorastModule":
        """**Factory method:**
        read the Python module at _path_,
        analyze it, and return a new MorastModule instance from the
        syntax tree returned by ast.parse().

        The module name is simply derived from the file name,
        and in src-based paths, the namespace is determined automatically.

        Remaining arguments:

        * _encoding_: source file encoding (defaults to `utf-8`)
        * keyword arguments _advertise_ and
          _excluded\\_module\\_variables_ are passed through to the
           initialization method
        """
        source = path.read_text(encoding=encoding)
        module_path_parts = path.parent.parts
        namespace = ""
        src_path = "src"
        if src_path in module_path_parts:
            namespace_root_pos = 0
            while src_path in module_path_parts[namespace_root_pos:]:
                namespace_root_pos = (
                    module_path_parts.index("src", namespace_root_pos) + 1
                )
            #
            namespace = ".".join(module_path_parts[namespace_root_pos:])
            logging.info("Module namespace: %s", namespace)
        #
        module_file = path.name
        module_name = module_file.rsplit(".", 1)[0]
        return cls(
            ast.parse(source=source, filename=path.name),
            name=module_name,
            namespace=namespace,
            **kwargs,
        )


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
