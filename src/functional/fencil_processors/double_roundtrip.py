from typing import Any

from functional.fencil_processors import roundtrip
from functional.iterator import ir as itir
from functional.iterator.processor_interface import fencil_executor


@fencil_executor
def executor(fencil_def: itir.FencilDefinition, *args: Any, **kwargs: Any):
    roundtrip.executor(fencil_def, *args, dispatch_backend=roundtrip.executor, **kwargs)
