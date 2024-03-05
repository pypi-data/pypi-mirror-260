import pytest
import kernels

def test_awkward_UnionArray_flatten_length_1():
	total_length = [123]
	fromtags = [0, 0, 0, 0]
	fromindex = [0, 1, 2, 3]
	length = 4
	offsetsraws = [[0, 1, 3, 5, 7], [1, 3, 5, 7, 9]]
	funcPy = getattr(kernels, 'awkward_UnionArray_flatten_length')
	funcPy(total_length = total_length,fromtags = fromtags,fromindex = fromindex,length = length,offsetsraws = offsetsraws)
	pytest_total_length = [7]
	assert total_length == pytest_total_length


