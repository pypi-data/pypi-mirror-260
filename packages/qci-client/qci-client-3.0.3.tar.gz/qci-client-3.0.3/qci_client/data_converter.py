"""Functions for data conversion."""

from math import floor
import sys
import time
from typing import Union

import networkx as nx
import numpy as np
import scipy.sparse as sp

from qci_client import enum

# We want to limit the memory size of each uploaded chunk to be safely below the max of 15 * MebiByte (~15MB).
# See https://git.qci-dev.com/qci-dev/qphoton-files-api/-/blob/main/service/files.go#L32.
MEMORY_MAX: int = 8 * 1000000  # 8MB


def get_size(obj, seen=None) -> int:
    """
    Recursively finds size of objects

    :param obj: data object to recursively compute size of
    :param seen: takes a set and is used in the recursive step only to record whether an object has been counted yet.

    :return int:
    """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(get_size(v, seen) for v in obj.values())
        size += sum(get_size(k, seen) for k in obj.keys())
    elif hasattr(obj, "__dict__"):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(get_size(i, seen) for i in obj)
    return size


def _get_soln_size(soln):
    # Check whether first entry is a graph node/class assignment, eg., {'id': 4, 'class': 2}
    if isinstance(soln[0], dict):
        return get_size(soln)

    return sys.getsizeof(soln[0]) * len(soln)


def compute_results_step_len(data: Union[np.ndarray, list]) -> int:
    """
    Compute the step length for "chunking" the providd data.

    Args:
        data: An numpy array or list of data

    Returns:
        The step length for "chunking" the data
    """
    # total mem size of soln vector
    soln_mem = _get_soln_size(data)
    # num_vars * step_len < 30k => step_len < 30k/num_vars
    chunk_ratio = MEMORY_MAX / soln_mem
    step_len = floor(chunk_ratio) if chunk_ratio >= 1 else 1
    return step_len

def data_to_json(file: dict, debug: bool = False) -> dict:
    """
    Converts data in file input into JSON string that can be passed to Qatalyst REST API
    :param file: file object whose data of type numpy.ndarray, scipy.sparse.spmatrix, or networkx.Graph is to be converted to JSON
    :param debug: Optional, if set to True, enables debug output (default = False for no debug output)

    :return: string (JSON format)
    :note: could add support for matrices stored as lists
    """
    start = time.perf_counter()

    supported_file_types = [
        "graph",
        "qubo",
        "hamiltonian",
        "objective",
        "constraints",
    ]

    file_type = enum.get_file_type(file=file).value

    if file_type not in supported_file_types:
        raise AssertionError(
            f"Unsupported file type input, specify one of {supported_file_types}"
        )

    data = file['file_config'][file_type]['data']
    file_config = {}

    if file_type == "graph":
        
        if not isinstance(data, nx.Graph):
            raise AssertionError("file_type 'graph' data must be type networkx.Graph")

        data = {
            **nx.node_link_data(data),
            "num_edges": data.number_of_edges(),
            "num_nodes": data.number_of_nodes(),
        }
    else:
        if isinstance(data, nx.Graph):
            raise AssertionError(
                "file_types ['objective', 'qubo', 'constraints', 'hamiltonian'] do not"
                "support networkx.Graph data"
            )

        data_ls = []

        if sp.isspmatrix_dok(data):
            for idx, val in zip(data.keys(), data.values()):
                data_ls.append({"i": int(idx[0]), "j": int(idx[1]), "val": val})
        elif sp.isspmatrix(data) or isinstance(data, np.ndarray):
            data = sp.coo_matrix(data)

            for i, j, val in zip(
                data.row.tolist(), data.col.tolist(), data.data.tolist()
            ):
                data_ls.append({"i": i, "j": j, "val": val})
        else:
            raise ValueError(
                "file_types = ['qubo', 'objective', 'constraints', 'hamiltonian'] only "
                "support types numpy.ndarray and scipy.sparse.spmatrix, got "
                f"{type(data)}"
            )

        rows, cols = data.get_shape()
        data = {"data": data_ls}

        if file_type == "constraints":
            # Constraints matrix is [A | -b]
            file_config.update({"num_constraints": rows, "num_variables": cols-1})
        else:
            # This works for hamiltonians, qubos, and objectives.
            file_config["num_variables"] = rows

    file_config.update(data)

    if debug:
        print(f"Time to convert data to json: {time.perf_counter()-start} s.")

    return {
        "file_name": file.get("file_name", f"{file_type}.json"),
        "file_config": {file_type: file_config}
    }
