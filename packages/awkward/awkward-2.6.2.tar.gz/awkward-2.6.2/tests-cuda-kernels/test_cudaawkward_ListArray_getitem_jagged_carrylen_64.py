# AUTO GENERATED ON 2024-03-04 AT 21:54:28
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import cupy
import pytest

import awkward as ak
import awkward._connect.cuda as ak_cu
from awkward._backends.cupy import CupyBackend

cupy_backend = CupyBackend.instance()

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_1():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([2, 0, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], dtype=cupy.int64)
    slicestops = cupy.array([3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 6, 11], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [5]
    assert cupy.array_equal(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_2():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=cupy.int64)
    slicestops = cupy.array([8, 4, 5, 6, 5, 5, 7], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [16]
    assert cupy.array_equal(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_3():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 4, 5, 6, 5, 5, 7, 1, 2, 1, 3, 1, 5, 3, 2], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [0]
    assert cupy.array_equal(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_4():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([1, 7, 6, 1, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5, 6, 7, 1, 2], dtype=cupy.int64)
    slicestops = cupy.array([1, 9, 6, 2, 4, 5, 3, 6, 3, 4, 2, 4, 5, 5, 7, 8, 2, 3], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [2]
    assert cupy.array_equal(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

def test_cudaawkward_ListArray_getitem_jagged_carrylen_64_5():
    carrylen = cupy.array([123], dtype=cupy.int64)
    slicestarts = cupy.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=cupy.int64)
    slicestops = cupy.array([1, 1, 1, 1, 1, 1, 1, 1], dtype=cupy.int64)
    sliceouterlen = 3
    funcC = cupy_backend['awkward_ListArray_getitem_jagged_carrylen', cupy.int64, cupy.int64, cupy.int64]
    funcC(carrylen, slicestarts, slicestops, sliceouterlen)

    try:
        ak_cu.synchronize_cuda()
    except:
        pytest.fail("This test case shouldn't have raised an error")
    pytest_carrylen = [3]
    assert cupy.array_equal(carrylen[:len(pytest_carrylen)], cupy.array(pytest_carrylen))

