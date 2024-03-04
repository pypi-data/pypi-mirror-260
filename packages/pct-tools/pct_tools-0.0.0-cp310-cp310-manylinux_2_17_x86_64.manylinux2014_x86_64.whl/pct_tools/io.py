from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pct_tools._ext
from scipy.sparse import csr_matrix

if TYPE_CHECKING:
    from typing import Any, Tuple


def construct_matrix(
    filename: str,
    row_indexes: np.ndarray[Any, np.dtype[np.int32]],
    col_indexes: np.ndarray[Any, np.dtype[np.int32]],
    values: np.ndarray[Any, np.dtype[np.float32]],
    img_shape: Tuple[int, int],
    verbose_level: int,
) -> None:
    """Construct and store a matrix from a list of indices and values.

    Args:
        filename: The filename of the output file.
        row_indexes: The row indices of the matrix elements.
        col_indexes: The column indices of the matrix elements.
        values: The values of the matrix elements.
        img_shape: The expected shape of the image.
        verbose_level: The verbosity level.
    """
    return pct_tools._ext.construct_matrix(
        filename, row_indexes, col_indexes, values, img_shape, verbose_level
    )


def read_matrix(filename: str) -> csr_matrix:
    """Read compressed Eigen matrix from disk.

    Args:
        filename: Name of the file containing the matrix.

    Returns:
        The matrix as a sparse matrix of 32-bit floats in CSR format.
    """
    return pct_tools._ext.read_matrix(filename)


def read_dense_matrix(filename: str) -> csr_matrix:
    """Read compressed Eigen matrix from disk.

    Args:
        filename: Name of the file containing the matrix.

    Returns:
        The matrix as a sparse matrix of 32-bit floats in CSR format.
    """
    return pct_tools._ext.read_dense_matrix(filename)


def read_compressed_matrix(filename: str) -> csr_matrix:
    """Read compressed Eigen matrix from disk.

    Args:
        filename: Name of the file containing the matrix.

    Returns:
        The matrix as a sparse matrix of 32-bit floats in CSR format.
    """
    return pct_tools._ext.read_compressed_matrix(filename)


def read_compressed_vector(filename: str) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Read compressed Eigen vector from disk.

    Args:
        filename: Name of the file containing the vector.

    Returns:
        The vector as an array of 32-bit floats.
    """
    return pct_tools._ext.read_compressed_vector(filename)


def read_vector(filename: str) -> np.ndarray[Any, np.dtype[np.float32]]:
    """Read an Eigen vector from disk.

    Args:
        filename: Name of the file containing the vector.

    Returns:
        The vector as an array of 32-bit floats.
    """
    return pct_tools._ext.read_vector(filename)


def recompress_matrix(filename: str, compression_level: int) -> None:
    """Read a compressed matrix and store it with a given compression level.

    Args:
        filename: Name of the file containing the matrix.
        compression_level: The compression level to use when storing it.
    """
    return pct_tools._ext.recompress_matrix(filename, compression_level)


def store_compressed_vector(
    vector: np.ndarray[Any, np.dtype[np.float32]], filename: str, compression_level: int
) -> None:
    """Compress and store a vector.

    Args:
        vector: The vector to compress and store.
        filename: The filename of the output file.
        compression_level: The compression level to use.
    """
    return pct_tools._ext.store_compressed_vector(vector, filename, compression_level)


def store_vector(vector: np.ndarray[Any, np.dtype[np.float32]], filename: str) -> None:
    """Store a vector.

    Args:
        x: The vector to store.
        filename: The filename of the output file.
    """
    return pct_tools._ext.store_vector(vector, filename)
