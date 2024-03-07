"""This module features helper functions for PyArrow."""

import logging
from typing import List, Tuple, Type, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa

from mac.data_utils.numpy_helpers import convert_multi_dim_numpy_array_to_list
from mac.types import ArrowListDType, IOArrowDType

logger = logging.getLogger(__name__)


def convert_fixed_shape_chunked_array_to_numpy_array(
    array: pa.ChunkedArray,
) -> npt.NDArray:
    """Converts a fixed shape multi-dim pa.ChunkedArray to a numpy array.

    :param array: The pa.ChunkedArray object to convert.

    :return: The converted data to a multi-dim numpy array.
    """
    shape = get_shape_of_multi_dim_chunked_array(
        array=array,
        arrow_list_dtype=get_arrow_list_dtype_from_pa_dtype(array.type),
    )
    return np.array(
        [
            row
            for chunk in array.chunks
            for row in flat_values(chunk)
            .to_numpy(zero_copy_only=False)
            .reshape([len(chunk), *shape])
        ]
    )


def convert_irregular_shape_chunked_array_to_numpy_array(
    array: pa.ChunkedArray,
) -> npt.NDArray:
    """Converts an irregular shape multi-dim pa.ChunkedArray to a numpy array.

    :param array: The pa.ChunkedArray to convert.

    :return: The converted data to a multi-dim numpy array of type `np.object`.
    """
    return np.array(
        [
            row
            for chunk in array.chunks
            for row in chunk.to_numpy(zero_copy_only=False)
        ],
        dtype=object,
    )


def convert_multi_dim_chunked_array_to_numpy_array(
    array: pa.ChunkedArray,
) -> npt.NDArray:
    """Converts a PyArrow chunked array to a numpy array.

    :param array: The PyArrow ChunkedArray to convert.

    :return: The converted data to a numpy array.
    """

    try:
        return convert_fixed_shape_chunked_array_to_numpy_array(array)
    except ValueError:
        # The incoming array is not of fixed shape, so we need to
        # return a numpy array of type object.
        return convert_irregular_shape_chunked_array_to_numpy_array(array)


def convert_numpy_array_to_fixed_shape_tensor_array(
    data: npt.NDArray,
) -> Tuple[pa.FixedShapeTensorType, pa.ExtensionArray]:
    """Converts a numpy array to a fixed shape tensor array.

    :param data: The data to convert.

    :return: The converted data to a FixedShapeTensor array,
        along with the PyArrow data type.
    """
    data_type = pa.from_numpy_dtype(data.dtype)
    data_shape = data[0].shape
    tensor_type = pa.fixed_shape_tensor(
        data_type,
        data_shape,
    )
    flattened_array = [item.flatten().tolist() for item in data]

    storage = pa.array(
        flattened_array,
        pa.list_(data_type, len(flattened_array[0])),
    )
    tensor_array = pa.ExtensionArray.from_storage(tensor_type, storage)

    return (tensor_type, tensor_array)


def convert_numpy_array_to_nested_list_array(
    data: npt.NDArray,
) -> Tuple[pa.ListType, pa.ListArray]:
    """Converts a numpy array to a nested list array.

    :param data: The data to convert.

    :return: The converted data to a nested list array,
        along with the PyArrow data type.
    """
    try:
        data_type = pa.from_numpy_dtype(data.dtype)
    except pa.ArrowNotImplementedError:
        # it's a list of iterables (e.g. list, tuple, dict etc.)
        item_dtype = get_data_type_of_nested_list(data)

        try:
            data_type = (
                pa.null()
                if item_dtype == type(None)
                else get_pa_struct_dtype_from_dict_array(data)
                if item_dtype == dict
                else pa.from_numpy_dtype(item_dtype)
            )
        except pa.ArrowNotImplementedError as exc:
            message = (
                f"Data type `{item_dtype}` of nested list cannot be converted to arrow.\n"  # noqa: E501
                f"Nested list that is causing this error: `{data}`."
            )
            logger.debug(message, exc_info=True)
            raise exc

    max_dim = get_max_depth_of_nested_list(data)
    nested_array = pa.array(
        convert_multi_dim_numpy_array_to_list(data),
        type=nested_pa_list_type_constructor(
            max_dim=max_dim, data_type=data_type
        ),
    )

    return (nested_array.type, nested_array)


def convert_numpy_array_to_pa_array(
    data: npt.NDArray,
) -> Tuple[pa.ListType, pa.Array]:
    """Converts a numpy array to a pa.Array.

    :param data: The data to convert.

    :return: The converted data to a pa.Array,
        along with the PyArrow data type.
    """
    return pa.from_numpy_dtype(data.dtype), pa.array(data)


def flat_values(array: pa.ChunkedArray) -> pa.Array:
    """
    Recursively unnest the `array` until a non-list type is found.

    :param array: The PyArrow ChunkedArray to flatten.

    :return: The inner non-nested values array.
    """
    if isinstance(array, pa.FixedShapeTensorArray):
        array = array.storage
    while pa_type_is_list(array.type):
        array = array.values
    return array


def get_arrow_list_dtype_from_pa_dtype(
    pa_type: pa.DataType,
) -> ArrowListDType:
    """Gets the ArrowListDType from a given pa.DataType.

    :param pa_type: The pa.DataType to convert.

    :return: The ArrowListDType.
    """
    if pa_type_is_fixed_shape_tensor(pa_type):
        return ArrowListDType.FIXED_SHAPE_TENSOR
    return ArrowListDType.LIST


def get_data_type_from_value_type(value_type: pa.DataType) -> pa.DataType:
    """Gets the data type from the given value type.

    :param value_type: The value type to get the data type from.

    :return: The PyArrow data type.
    """
    try:
        return get_data_type_from_value_type(value_type.value_type)
    except AttributeError:
        return value_type


def get_data_type_of_nested_list(data: Union[npt.NDArray, List]) -> Type:
    """Gets the data type of a nested list.
    :param data: The nested list to get the data type of.
    :return: The data type of the nested list.
    """
    if isinstance(data, (np.ndarray, list, tuple)):
        return get_data_type_of_nested_list(data[0])
    return type(data)


def get_io_arrow_dtype_from_column(
    column_type: pa.DataType,
) -> IOArrowDType:
    """Gets the IOArrowDType from the given column.

    :param column: The column to get the IOArrowDType from.
    """
    if pa_type_is_fixed_shape_tensor(column_type):
        return IOArrowDType.FIXED_SHAPE_TENSOR
    elif pa_type_is_list(column_type):
        return IOArrowDType.LIST
    else:
        return IOArrowDType.SCALAR


def get_max_depth_of_nested_list(data: Union[npt.NDArray, List]) -> int:
    """Gets the maximum depth of a nested list.

    :param data: The nested list to get the maximum depth of.

    :return: The maximum depth of the nested list.
    """
    if isinstance(data, (np.ndarray, list)):
        depths = [get_max_depth_of_nested_list(element) for element in data]
        return 1 + max(depths)
    return 0


def get_pa_struct_dtype_from_dict_array(data: npt.NDArray) -> pa.DataType:
    """Gets the PyArrow data type from a numpy array of dictionaries.
    :param data: The data to get the PyArrow data type from.
    :return: The PyArrow data type.
    """
    while not isinstance(data, dict):
        data = data[0]

    struct_fields = []
    for key, value in data.items():
        try:
            struct_fields.append((key, pa.from_numpy_dtype(type(value))))
        except pa.ArrowNotImplementedError:
            # dict values are of type iterable
            item_dtype = get_data_type_of_nested_list(value)
            list_constructor = nested_pa_list_type_constructor(
                max_dim=len(value),
                data_type=pa.from_numpy_dtype(item_dtype),
            )
            struct_fields.append(
                (
                    key,
                    list_constructor,
                )
            )

    return pa.struct(struct_fields)


def get_shape_of_multi_dim_chunked_array(
    array: pa.ChunkedArray, arrow_list_dtype: ArrowListDType
) -> Tuple[int, ...]:
    """Gets the shape of a multi-dimensional pa.ChunkedArray.

    :param array: The multi-dimensional array to get the shape of.
    :param arrow_list_dtype: The ArrowListDType of the array.

    :return: The shape of the multi-dimensional pa.ChunkedArray.
    """
    if arrow_list_dtype == ArrowListDType.FIXED_SHAPE_TENSOR:
        return tuple(array.type.shape)
    return get_shape_of_nested_pa_list_scalar(array[0])


def get_shape_of_nested_pa_list_scalar(
    data: pa.ListScalar,
) -> Tuple[int, ...]:
    """Gets the shape of a nested pa.ChunkedArray.

    :param data: The nested list to get the shape of.

    :return: The shape of the nested pa.ChunkedArray.
    """
    if isinstance(data, pa.ListScalar) and data is not None:
        return (len(data),) + get_shape_of_nested_pa_list_scalar(data[0])
    return ()


def nested_pa_list_type_constructor(
    max_dim: int, data_type: pa.DataType
) -> pa.ListType:
    """This helper function constructs a nested PyArrow list type.

    :param max_dim: The number of dimensions of the nested list.
    :param data_type: The data type of the nested list.

    :return: The nested PyArrow ListType object.
    """
    while max_dim > 1:
        max_dim -= 1
        return pa.list_(nested_pa_list_type_constructor(max_dim, data_type))
    return data_type


def pa_type_is_fixed_shape_tensor(data_type: pa.DataType) -> bool:
    """Checks if the given PyArrow data type is a fixed shape tensor type.

    :param data_type: The data type to check.

    :return: True if the given data type is a fixed shape tensor type, False otherwise.
    """
    return isinstance(data_type, pa.FixedShapeTensorType)


def pa_type_is_list(data_type: pa.DataType) -> bool:
    """Checks if the given PyArrow data type is a list type.

    :param data_type: The data type to check.

    :return: True if the given data type is a list type, False otherwise.
    """
    return isinstance(data_type, (pa.ListType, pa.FixedSizeListType))
