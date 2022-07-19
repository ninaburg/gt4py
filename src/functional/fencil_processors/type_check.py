from typing import Any

from functional.iterator import ir as itir, type_inference
from functional.iterator.processor_interface import fencil_formatter
from functional.iterator.transforms import apply_common_transforms


@fencil_formatter
def check(fencil_def: itir.FencilDefinition, *args: Any, **kwargs: Any) -> str:
    type_inference.pprint(type_inference.infer(fencil_def))
    transformed = apply_common_transforms(
        fencil_def, use_tmps=kwargs.get("use_tmps"), offset_provider=kwargs["offset_provider"]
    )
    return type_inference.pformat(type_inference.infer(transformed))
