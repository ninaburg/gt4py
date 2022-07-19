from typing import Any

from functional.iterator import ir as itir
from functional.iterator.pretty_parser import pparse
from functional.iterator.pretty_printer import pformat
from functional.iterator.processor_interface import fencil_formatter


@fencil_formatter
def pretty_format_and_check(fencil_def: itir.FencilDefinition, *args: Any, **kwargs: Any) -> str:
    pretty = pformat(fencil_def)
    parsed = pparse(pretty)
    assert parsed == fencil_def
    return pretty
