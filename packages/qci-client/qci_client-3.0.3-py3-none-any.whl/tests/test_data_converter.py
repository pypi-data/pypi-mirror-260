"""Test for data conversion functions."""

import time
import unittest

import networkx as nx
import numpy as np
import pytest
import scipy.sparse as sp

from qci_client.data_converter import data_to_json

@pytest.mark.offline
class TestDataToJson(unittest.TestCase):
    """Test suite for data conversion to JSON."""

    #def test_file_type_assert(self):
    #    """Test file generation for bad file type."""
    #    # test file_type assertion
    #    with self.assertRaises(AssertionError):
    #        data_to_json(data=[])

    #def test_filename_blank(self):
    #    """Test file generation for missing file name."""
    #    # test file_name change if blank
    #    name_change = data_to_json(data=[])
    #    self.assertEqual(name_change["file_name"], "rhs.json")

    #def test_file_type_and_name(self):
    #    """Test file generation for file type and name."""
    #    file_name_check = data_to_json(
    #        data=[]
    #    )
    #    #self.assertEqual(file_name_check["file_type"], "rhs")
    #    self.assertEqual(file_name_check["file_name"], "other_name.json")

    def test_graph_file_body(self):
        """Test file generation for graph data."""
        graph = nx.Graph()
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        #graph_dict_check = {
        #    "file_type": "graph",
        #    "file_name": "graph.json",
        #    "directed": False,
        #    "multigraph": False,
        #    "graph": {},
        #    "nodes": [{"id": 1}, {"id": 2}, {"id": 3}],
        #    "links": [{"source": 1, "target": 2}, {"source": 1, "target": 3}],
        #}
        graph_dict_check = {
            "file_name": "graph.json",
            "file_config": {
                "graph": {
                    "directed": False,
                    "multigraph": False,
                    "graph": {},
                    "nodes": [{"id": 1}, {"id": 2}, {"id": 3}],
                    "links": [{"source": 1, "target": 2}, {"source": 1, "target": 3}],
                },
            },
        }

        #graph_body = data_to_json(data=graph)
        #self.assertDictEqual(graph_dict_check, graph_body)

        #with self.assertRaises(AssertionError) as context:
        #    data_to_json(data=np.array([]))

        #self.assertEqual(
        #    str(context.exception), "'graph' file_type must be type networkx.Graph"
        #)

    @pytest.mark.timing
    def test_large_data_conversion(self):
        """Test file generation for large data is sufficiently fast."""
        large_qubo = np.random.normal(size=(3000, 3000))
        large_qubo = large_qubo + large_qubo.T
        start = time.perf_counter()
        data_to_json(file={"file_config": {"qubo": {"data": large_qubo}}})
        end = time.perf_counter()
        conversion_time = end - start

        self.assertTrue(
            conversion_time < 5,
            msg=f"Matrix conversion to JSON took too long: 5s <= {conversion_time}s.",
        )

    #def test_type_not_graph_check(self):
    #    """Test file generation for mismatched data and problem types."""
    #    with self.assertRaises(AssertionError) as context:
    #        graph = nx.Graph()
    #        data_to_json(data=graph)

    #    self.assertEqual(
    #        str(context.exception),
    #        "file_types ['rhs', 'objective', 'qubo', 'constraints', 'constraint_penalties', 'hamiltonian'] do not support networkx.Graph type",
    #    )

    def test_rhs_file_body(self):  # pylint: disable=too-many-locals
        """Test file generation for right-hand-side data."""
        rhs_list = [1, 2, 3]
        rhs_np = np.array([1, 2, 3])
        rhs_np_long = np.array([[1], [2], [3]])
        rhs_sp = sp.csr_matrix(rhs_np)
        rhs_sp_long = sp.csr_matrix(rhs_np_long)
        rhs_body_check = {
            "file_name": "rhs.json",
            "file_config": {
                "rhs": {
                    "num_constraints": 3,
                    "data": [1, 2, 3],
                },
            },
        }

        #commenting out, not currently supported
        #rhs_list_body = data_to_json(data=rhs_list)
        #self.assertDictEqual(rhs_body_check, rhs_list_body)
        #rhs_np_body = data_to_json()
        #self.assertDictEqual(rhs_body_check, rhs_np_body)
        #rhs_sp_body = data_to_json(file_type="rhs")
        #self.assertDictEqual(rhs_body_check, rhs_sp_body)
        #rhs_np_long_body = data_to_json(file_type="rhs")
        #self.assertDictEqual(rhs_body_check, rhs_np_long_body)
        #rhs_sp_long_body = data_to_json(file_type="rhs")
        #self.assertDictEqual(rhs_body_check, rhs_sp_long_body)

        constraint_penalties_list = [1, 2, 3]
        constraint_penalties_np = np.array([1, 2, 3])
        constraint_penalties_np_long = np.array([[1], [2], [3]])
        constraint_penalties_sp = sp.csr_matrix(constraint_penalties_np)
        constraint_penalties_sp_long = sp.csr_matrix(constraint_penalties_np_long)

        #constraint_penalties_body_check = {
        #    "file_type": "constraint_penalties",
        #    "file_name": "constraint_penalties.json",
        #    "num_constraints": 3,
        #    "data": [1, 2, 3],
        #}
        constraint_penalties_body_check = {
            "file_name": "constraint_penalties.json",
            "file_config": {
                "constraint_penalties": {
                    "num_constraints": 3,
                    "data": [1, 2, 3],
                }
            }
        }

        #constraint_penalties_list_body = data_to_json(
        #    data=constraint_penalties_list
        #)
        #self.assertDictEqual(
        #    constraint_penalties_body_check, constraint_penalties_list_body
        #)
        #constraint_penalties_np_body = data_to_json(
        #    data=constraint_penalties_np
        #)
        #self.assertDictEqual(
        #    constraint_penalties_body_check, constraint_penalties_np_body
        #)
        #constraint_penalties_sp_body = data_to_json(
        #    data=constraint_penalties_sp
        #)
        #self.assertDictEqual(
        #    constraint_penalties_sp_body
        #)
        #constraint_penalties_np_long_body = data_to_json(
        #    data=constraint_penalties_np_long
        #)
        #self.assertDictEqual(
        #    constraint_penalties_body_check, constraint_penalties_np_long_body
        #)
        #constraint_penalties_sp_long_body = data_to_json(
        #    data=constraint_penalties_sp_long
        #)
        #self.assertDictEqual(
        #    constraint_penalties_body_check, constraint_penalties_sp_long_body
        #)

    #def test_assert_types_objective_matrix(self):
    #    """Test file generation for improperly formatted qubo data."""
    #    with self.assertRaises(AssertionError) as context:
    #        data_to_json(data=[[1, -1], [-1, 1]])

    #    self.assertEqual(
    #        str(context.exception),
    #        "file_types = ['qubo', 'objective', 'constraints', 'hamiltonian'] only support types np.ndarray and scipy.sparse.spmatrix",
    #    )

    def test_qubo_hamiltonian_constraints_objective_file_body(self):
        """
        Test file generation for a qubo and hamiltonian objectives with constraints.
        """
        # will be used for both qubo and objective since same shape
        q_obj_np = np.array([[-1, 1], [1, -1]])
        q_obj_sp = sp.csr_matrix(q_obj_np)
        # is in i,j sorted order to allow for exact match of lists
        q_obj_data = [
            {"i": 0, "j": 0, "val": -1.0},
            {"i": 0, "j": 1, "val": 1.0},
            {"i": 1, "j": 0, "val": 1.0},
            {"i": 1, "j": 1, "val": -1.0},
        ]

        # using for hamiltonian and constraints
        ham_cons_np = np.array([[-1, 1, 1], [1, -1, 1]])
        ham_cons_sp = sp.csr_matrix(ham_cons_np)
        # is i, j sorted order to allow for exact match of lists
        ham_cons_data = [
            {"i": 0, "j": 0, "val": -1.0},
            {"i": 0, "j": 1, "val": 1.0},
            {"i": 0, "j": 2, "val": 1.0},
            {"i": 1, "j": 0, "val": 1.0},
            {"i": 1, "j": 1, "val": -1.0},
            {"i": 1, "j": 2, "val": 1.0},
        ]

        json_template = {
            "file_name": "placeholder",
            "file_config": {
            }
        }

        # start from using fewest fields to most so can use update on same json_template
        # qubo
        file_type = "qubo"
        json_template.update(
            {
                "file_name": file_type + ".json",
                "file_config": {
                    file_type: {
                        "data": q_obj_data,
                        "num_variables": 2,
                    }
                }
            }
        )
        #qubo_np_body = data_to_json(data=q_obj_np)
        #qubo_np_body["file_config"][file_type]["data"] = sorted(qubo_np_body["file_config"][file_type]["data"], key=itemgetter("i", "j"))
        #self.assertDictEqual(json_template, qubo_np_body)
        # objective
        file_type = "objective"
        #json_template.update({"file_type": file_type, "file_name": file_type + ".json"})
        #objective_sp_body = data_to_json(data=q_obj_sp)
        #objective_sp_body["file_config"][file_type]["data"] = sorted(
        #    objective_sp_body["file_config"][file_type]["data"], key=itemgetter("i", "j")
        #)
        #self.assertDictEqual(json_template, objective_sp_body)
        # hamiltonian
        file_type = "hamiltonian"
        # don't have to update num_variables becaues is the same as was used for qubo and objective
        json_template.update(
            {
                "file_name": file_type + ".json",
                "file_config": {
                    file_type: {
                        "data": ham_cons_data,
                        "num_variables": 2,
                    }
                }
            }
        )
        #ham_np_body = data_to_json(data=ham_cons_np)
        #ham_np_body["file_config"][file_type]["data"] = sorted(ham_np_body["file_config"][file_type]["data"], key=itemgetter("i", "j"))
        #print(ham_np_body)
        #print(json_template)
        #self.assertDictEqual(json_template, ham_np_body)
        # objective
        file_type = "constraints"
        json_template.update(
            {
                "file_name": file_type + ".json",
                "file_config": {
                    file_type: {
                        "num_variables": 3,
                        "num_constraints": 2,
                    }
                }
            }
        )
        #constraints_sp_body = data_to_json(data=ham_cons_sp)
        #constraints_sp_body["file_config"][file_type]["data"] = sorted(
        #    constraints_sp_body["file_config"][file_type]["data"], key=itemgetter("i", "j")
        #)
        #print(constraints_sp_body)
        #print(json_template)
        #self.assertDictEqual(json_template, constraints_sp_body)

    def test_small_graph(self):
        """Test file generation for a small graph problem."""
        graph = nx.Graph()
        edge_wt = 1.0
        graph.add_nodes_from(range(7))

        for node in graph.nodes:
            if node in [0, 1, 2, 3]:
                graph.nodes[node].update({"bipartite": 0})
            else:
                graph.nodes[node].update({"bipartite": 1})

        graph.add_edges_from(
            [
                (0, 4, {"weight": edge_wt}),
                (0, 6, {"weight": edge_wt}),
                (1, 4, {"weight": edge_wt}),
                (2, 5, {"weight": edge_wt}),
                (3, 5, {"weight": edge_wt}),
            ]
        )

        graph_dict_check = {
            "file_type": "graph",
            "file_name": "graph.json",
            "directed": False,
            "multigraph": False,
            "graph": {},
            "nodes": list(graph.nodes(data=True)),
            "links": list(graph.edges(data=True)),
        }

        # get the first element (only one), and also remove the part_num (second tuple element)
        compress = False
        legacy = False
