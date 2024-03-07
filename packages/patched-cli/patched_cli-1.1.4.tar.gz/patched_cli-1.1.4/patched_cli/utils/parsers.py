import pathlib
import platform
import sys
from functools import lru_cache
from typing import Generator

from tree_sitter import Language, Node, Parser, Tree

arch = platform.machine().lower()
platform = platform.system().lower()
if sys.platform == "win32":
    ext = "dll"
else:
    ext = "so"

__LANGUAGES_SHARED = pathlib.Path(__file__).parent.parent / "resources" / f"languages_{platform}_{arch}.{ext}"


@lru_cache(maxsize=10)
def get_language(language: str) -> Language:
    return Language(str(__LANGUAGES_SHARED), language)


@lru_cache(maxsize=10)
def get_parser(language: str) -> Parser:
    parser = Parser()
    parser.set_language(get_language(language))
    return parser


def dfs_tree(tree: Tree) -> Generator[Node, None, None]:
    yield from dfs_node(tree.root_node)


def dfs_node(node: Node) -> Generator[Node, None, None]:
    yield node
    for child in node.children:
        yield from dfs_node(child)
