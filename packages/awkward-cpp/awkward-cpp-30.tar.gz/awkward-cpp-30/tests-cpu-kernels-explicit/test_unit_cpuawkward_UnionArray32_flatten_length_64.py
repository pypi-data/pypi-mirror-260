# AUTO GENERATED ON 2024-03-04 AT 21:54:28
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import pytest

from awkward_cpp.cpu_kernels import lib

def test_unit_cpuawkward_UnionArray32_flatten_length_64_1():
    total_length = [123]
    total_length = (ctypes.c_int64*len(total_length))(*total_length)
    fromtags = [0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    fromindex = [0, 1, 2, 3]
    fromindex = (ctypes.c_int32*len(fromindex))(*fromindex)
    length = 4
    offsetsraws = [[0, 1, 3, 5, 7], [1, 3, 5, 7, 9]]
    offsetsraws = ctypes.pointer(ctypes.cast((ctypes.c_int64*len(offsetsraws[0]))(*offsetsraws[0]),ctypes.POINTER(ctypes.c_int64)))
    funcC = getattr(lib, 'awkward_UnionArray32_flatten_length_64')
    ret_pass = funcC(total_length, fromtags, fromindex, length, offsetsraws)
    pytest_total_length = [7]
    assert total_length[:len(pytest_total_length)] == pytest.approx(pytest_total_length)
    assert not ret_pass.str

