import ctypes
import math

import jinja2
import numpy as np
import pytest

from functional.fencil_processors import cpp, defs
from functional.fencil_processors.callables.cpp import callable


@pytest.fixture
def source_module():
    entry_point = defs.Function(
        "stencil",
        parameters=[
            defs.BufferParameter("buf", ["I", "J"], ctypes.c_float),
            defs.ScalarParameter("sc", ctypes.c_float),
        ],
    )
    func = cpp.render_function_declaration(
        entry_point,
        """\
        const auto xdim = gridtools::at_key<generated::I_t>(sid_get_upper_bounds(buf));
        const auto ydim = gridtools::at_key<generated::J_t>(sid_get_upper_bounds(buf));
        return xdim * ydim * sc;\
        """,
    )
    src = jinja2.Template("""\
    #include <gridtools/fn/cartesian.hpp>
    #include <gridtools/fn/unstructured.hpp>
    namespace generated {
    struct I_t {} constexpr inline I; 
    struct J_t {} constexpr inline J; 
    }
    {{func}}\
    """).render(func=func)

    return defs.SourceCodeModule(
        entry_point=entry_point,
        source_code=src,
        library_deps=[
            defs.LibraryDependency("gridtools", "master"),
            defs.LibraryDependency("openmp", "*"),
        ],
        language=cpp.language_id,
    )


def test_callable(source_module):
    wrapper = callable.create_callable(source_module)
    buf = np.zeros(shape=(6, 5), dtype=np.float32)
    sc = np.float32(3.1415926)
    res = wrapper(buf, sc)
    assert math.isclose(res, 6 * 5 * 3.1415926, rel_tol=1e-4)
