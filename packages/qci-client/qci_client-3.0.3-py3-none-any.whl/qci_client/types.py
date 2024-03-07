"""
Types for Python client for files REST API for optimization service.

Copyright 2023, Quantum Computing Incorporated
"""

from typing import Dict, List, Literal, Protocol, TypedDict, Union

# Literals should match corresponding values in enum.FileType.
Hamiltonian = Literal["hamiltonian"]
Qubo = Literal["qubo"]
Objective = Literal["objective"]
Constraints = Literal["constraints"]
Graph = Literal["graph"]
GpResults = Literal["graph_partitioning_results"]
IhoResults = Literal["ising_hamiltonian_optimization_results"]
NqhoContinuousResults = Literal[
    "normalized_qudit_hamiltonian_optimization_continuous_results"
]
NqhoIntegerResults = Literal[
    "normalized_qudit_hamiltonian_optimization_integer_results"
]
QlcboResults = Literal["quadratic_linearly_constrained_binary_optimization_results"]
QuboResults = Literal["quadratic_unconstrained_binary_optimization_results"]


class HealthGetResponseBody(TypedDict):
    """GET health response body."""

    message: str


class VersionGetResponseBody(TypedDict):
    """GET version response body."""

    application_name: str
    version: str


class CountsGetResponseBody(TypedDict):
    """GET file counts response body."""

    count: int


class ConstraintsMetadata(TypedDict):
    """Constraints file metadata."""

    num_constraints: int
    num_variables: int


class ConstraintsMetadataConfig(TypedDict):
    """Constraints file metadata configuration."""

    constraints: ConstraintsMetadata


class GraphMetadata(TypedDict):
    """Graph file metadata."""

    directed: bool
    multigraph: bool
    graph: Dict[str, str]
    num_edges: int
    num_nodes: int


class GraphMetadataConfig(TypedDict):
    """Graph file metadata configuration."""

    graph: GraphMetadata


class HamiltonianMetadata(TypedDict):
    """Hamiltonian file metadata."""

    num_variables: int


class HamiltonianMetadataConfig(TypedDict):
    """Hamiltonian file metadata configuration."""

    hamiltonian: HamiltonianMetadata


class ObjectiveMetadata(TypedDict):
    """Objective file metadata."""

    num_variables: int


class ObjectiveMetadataConfig(TypedDict):
    """Objective file metadata configuration."""

    objective: ObjectiveMetadata


class QuboMetadata(TypedDict):
    """QUBO file metadata."""

    num_variables: int


class QuboMetadataConfig(TypedDict):
    """QUBO file metadata configuration."""

    qubo: QuboMetadata


class GpResultsMetadata(TypedDict):
    """Graph Partitioning (GP) results file metadata."""


class GpResultsMetadataConfig(TypedDict):
    """Graph Partitioning (GP)  results file metadata configuration."""

    graph_partitioning_results: GpResultsMetadata


class IhoResultsMetadata(TypedDict):
    """Ising Hamiltonian Optimization (IHO) results file metadata."""


class IhoResultsMetadataConfig(TypedDict):
    """Ising Hamiltonian Optimization (IHO) results file metadata configuration."""

    ising_hamiltonian_optimization_results: IhoResultsMetadata


class NqhoContinuousResultsMetadata(TypedDict):
    """
    Continuous normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata.
    """


class NqhoContinuousResultsMetadataConfig(TypedDict):
    """
    Continuous Normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata
    configuration.
    """

    normalized_qudit_hamiltonian_optimization_continuous_results: NqhoContinuousResultsMetadata  # pylint: disable=line-too-long


class NqhoIntegerResultsMetadata(TypedDict):
    """
    Integer normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata.
    """


class NqhoIntegerResultsMetadataConfig(TypedDict):
    """
    Integer Normalized-Qudit Hamiltonian Optimization (NQHO) results file metadata
    configuration.
    """

    normalized_qudit_hamiltonian_optimization_integer_results: NqhoIntegerResultsMetadata  # pylint: disable=line-too-long


class QlcboResultsMetadata(TypedDict):
    """
    Quadratic Linearly Constrained Binary Optimization (QLCBO) results file metadata.
    """


class QlcboResultsMetadataConfig(TypedDict):
    """
    Quadratic Linearly Constrained Binary Optimization (QLCBO) results file metadata
    configuration.
    """

    quadratic_linearly_constrained_binary_optimization_results: QlcboResultsMetadata


class QuboResultsMetadata(TypedDict):
    """Quadratic Unconstrained Binary Optimization (QUBO) results file metadata."""


class QuboResultsMetadataConfig(TypedDict):
    """
    Quadratic Unconstrained Binary Optimization (QUBO) results file metadata
    configuration.
    """

    quadratic_unconstrained_binary_optimization_results: QuboResultsMetadata


class MetadataOptionalPostRequestBody(TypedDict, total=False):
    """Optional file metadata."""

    file_name: str


class InputMetadataPostRequestBody(MetadataOptionalPostRequestBody):
    """Request body for POSTing any input file metadata."""

    file_config: Union[
        ConstraintsMetadataConfig,
        GraphMetadataConfig,
        HamiltonianMetadataConfig,
        ObjectiveMetadataConfig,
        QuboMetadataConfig,
    ]


class ResultsMetadataPostRequestBody(MetadataOptionalPostRequestBody):
    """Request body for POSTing any results file metadata."""

    organization_id: str
    user_id: str
    file_config: Union[
        GpResultsMetadataConfig,
        IhoResultsMetadataConfig,
        NqhoContinuousResultsMetadataConfig,
        NqhoIntegerResultsMetadataConfig,
        QlcboResultsMetadataConfig,
        QuboResultsMetadataConfig,
    ]


# Request body for POSTing any file metadata.
MetadataPostRequestBody = Union[
    InputMetadataPostRequestBody,
    ResultsMetadataPostRequestBody,
]


class MetadataPostResponseBody(TypedDict):
    """File metadata POST response body."""

    file_id: str


class DataDict(TypedDict):
    """Dictionary elements of data array."""

    i: int
    j: int
    val: float


class ConstraintsPart(TypedDict):
    """Constraints file part."""

    data: List[DataDict]


class ConstraintsPartConfig(TypedDict):
    """Constraints file part configuration."""

    constraints: ConstraintsPart


class NodeDict(TypedDict):
    """Dictionary elements of nodes array."""

    id: int


class LinkDictOptional(TypedDict, total=False):
    """Optional fields of dictionary elements of links array."""

    weight: float


class LinkDict(LinkDictOptional):
    """Dictionary elements of links array."""

    source: int
    target: int


class GraphPart(TypedDict):
    """Graph file part."""

    nodes: List[NodeDict]
    links: List[LinkDict]


class GraphPartConfig(TypedDict):
    """Graph file part configuration."""

    graph: GraphPart


class HamiltonianPart(TypedDict):
    """Hamiltonian file part."""

    data: List[DataDict]


class HamiltonianPartConfig(TypedDict):
    """Hamiltonian file part configuration."""

    hamiltonian: HamiltonianPart


class ObjectivePart(TypedDict):
    """Objective file part."""

    data: List[DataDict]


class ObjectivePartConfig(TypedDict):
    """Objective file part configuration."""

    objective: ObjectivePart


class QuboPart(TypedDict):
    """QUBO file part."""

    data: List[DataDict]


class QuboPartConfig(TypedDict):
    """QUBO file part configuration."""

    qubo: QuboPart


class GpResultsPart(TypedDict):
    """GP results file part."""

    balances: List[float]
    counts: List[int]
    cut_sizes: List[float]
    energies: List[float]
    feasibilities: List[bool]
    partitions: List[List[List[int]]]
    solutions: List[List[int]]


class GpResultsPartConfig(TypedDict):
    """GP results file part configuration."""

    graph_partitioning_results: GpResultsPart


class IhoResultsPart(TypedDict):
    """IHO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[int]]


class IhoResultsPartConfig(TypedDict):
    """IHO results file part configuration."""

    ising_hamiltonian_optimization_results: IhoResultsPart


class NqhoContinuousResultsPart(TypedDict):
    """Continuous NQHO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[float]]


class NqhoContinuousResultsPartConfig(TypedDict):
    """Continuous NQHO results file part configuration."""

    normalized_qudit_hamiltonian_optimization_continuous_results: NqhoContinuousResultsPart  # pylint: disable=line-too-long


class NqhoIntegerResultsPart(TypedDict):
    """Integer NQHO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[int]]


class NqhoIntegerResultsPartConfig(TypedDict):
    """Integer NQHO results file part configuration."""

    normalized_qudit_hamiltonian_optimization_integer_results: NqhoIntegerResultsPart


class QlcboResultsPart(TypedDict):
    """QLCBO results file part."""

    counts: List[int]
    energies: List[float]
    feasibilities: List[bool]
    objective_values: List[float]
    solutions: List[List[int]]


class QlcboResultsPartConfig(TypedDict):
    """QLCBO results file part configuration."""

    quadratic_linearly_constrained_binary_optimization_results: QlcboResultsPart


class QuboResultsPart(TypedDict):
    """QUBO results file part."""

    counts: List[int]
    energies: List[float]
    solutions: List[List[int]]


class QuboResultsPartConfig(TypedDict):
    """QUBO results file part configuration."""

    quadratic_unconstrained_binary_optimization_results: QuboResultsPart


class PartPatchRequestBody(TypedDict):
    """The request body for PATCHing all input and results file parts."""

    file_config: Union[
        ConstraintsPartConfig,
        GraphPartConfig,
        HamiltonianPartConfig,
        ObjectivePartConfig,
        QuboPartConfig,
        GpResultsPartConfig,
        IhoResultsPartConfig,
        NqhoContinuousResultsPartConfig,
        NqhoIntegerResultsPartConfig,
        QlcboResultsPartConfig,
        QuboResultsPartConfig,
    ]


class PartPatchResponseBody(TypedDict):
    """File part PATCH response body."""

    file_id: str


class MetadataOptionalGetResponseBody(TypedDict, total=False):
    """Optional fields for file metadata GET responses."""

    organization_id: str
    user_id: str
    file_name: str


class MetadataGetResponseBody(MetadataOptionalGetResponseBody):
    """GET file metatada response body."""

    file_id: str
    upload_date_rfc3339: str
    last_accessed_rfc3339: str
    num_parts: int
    num_bytes: int
    file_config: Union[
        ConstraintsMetadataConfig,
        GraphMetadataConfig,
        HamiltonianMetadataConfig,
        ObjectiveMetadataConfig,
        QuboMetadataConfig,
        GpResultsMetadataConfig,
        IhoResultsMetadataConfig,
        NqhoContinuousResultsMetadataConfig,
        NqhoIntegerResultsMetadataConfig,
        QlcboResultsMetadataConfig,
        QuboResultsMetadataConfig,
    ]


class GetResponseBody(TypedDict):
    """Fields for GET file metadata responses."""

    files: List[MetadataGetResponseBody]


class PartGetResponseBody(TypedDict):
    """GET file part response body."""

    file_id: str
    part_number: int
    upload_date_rfc3339: str
    file_config: Union[
        ConstraintsPartConfig,
        GraphPartConfig,
        HamiltonianPartConfig,
        ObjectivePartConfig,
        QuboPartConfig,
        GpResultsPartConfig,
        IhoResultsPartConfig,
        NqhoContinuousResultsPartConfig,
        NqhoIntegerResultsPartConfig,
        QlcboResultsPartConfig,
        QuboResultsPartConfig,
    ]


class DeleteResponseBody(TypedDict):
    """File DELETE response body."""

    num_deleted: int


class SupportsAccessTokens(Protocol):  # pylint: disable=too-few-public-methods
    """Interface for clients that are injected to retrieve access tokens."""

    @property
    def access_token(self) -> str:
        """Return a valid access token for the API."""
        ...  # pylint: disable=unnecessary-ellipsis
