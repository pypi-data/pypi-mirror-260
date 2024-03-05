import sys
from builtins import hasattr as has_attribute
from os import getenv
from pathlib import Path
from shutil import copyfile as copy_file
from typing import AbstractSet as AnySet
from typing import Any, Dict, TypeVar

from entrypoint import entrypoint
from setuptools import Distribution, Extension
from setuptools.command.build_ext import build_ext

TRUE = frozenset(("1", "true", "t", "yes", "y"))
FALSE = frozenset(("0", "false", "f", "no", "n"))

CAN_NOT_PARSE = "can not parse `{}` to `bool`"


def parse_bool(string: str, true: AnySet[str] = TRUE, false: AnySet[str] = FALSE) -> bool:
    string = string.casefold()

    if string in true:
        return True

    if string in false:
        return False

    raise ValueError(CAN_NOT_PARSE.format(string))


SetupKeywords = Dict[str, Any]

S = TypeVar("S", bound=SetupKeywords)

# C Extensions
EXTENSIONS_NAME = "XOR_CIPHER_EXTENSIONS"

EXTENSIONS = getenv(EXTENSIONS_NAME)

if EXTENSIONS is None:
    with_extensions = True

else:
    with_extensions = parse_bool(EXTENSIONS)


PYPY_VERSION_INFO = "pypy_version_info"

if has_attribute(sys, PYPY_VERSION_INFO):
    with_extensions = False


LANGUAGE_LEVEL = "3"


extensions = []

if with_extensions:
    from Cython.Build import cythonize

    extensions = cythonize(
        [Extension("xor_cipher.extension", ["xor_cipher/extension.pyx"])],
        language_level=LANGUAGE_LEVEL,
    )


PACKAGE = "xor-cipher"


def build(setup_keywords: S) -> S:
    distribution = Distribution(dict(name=PACKAGE, ext_modules=extensions))

    command = build_ext(distribution)
    command.ensure_finalized()
    command.run()

    # Copy built extensions back to the project
    for output in map(Path, command.get_outputs()):
        relative_extension = output.relative_to(command.build_lib)

        if not output.exists():
            continue

        copy_file(output, relative_extension)

    return setup_keywords


@entrypoint(__name__)
def main() -> None:
    build({})
