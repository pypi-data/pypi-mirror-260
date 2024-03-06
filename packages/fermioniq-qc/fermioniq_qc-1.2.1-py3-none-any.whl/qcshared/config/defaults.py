from typing import Any, Sequence, cast

import numpy as np

from ..serializers.custom_types import Circuit
from ..serializers.serializer import (
    get_default_qubit_objects,
    get_qubits_from_serialized_circuit,
    serialize_circuit,
    serialize_qubits,
)
from .constants import (
    MAX_EASY_BOND_DIM,
    MAX_ELEMENTS,
    MPO_BOND_DIM_NO_NOISE,
    MPO_BOND_DIM_WITH_NOISE,
    NUM_ROWS,
)
from .resources import _num_elements_without_bond_dim_dmrg


def standard_input_from_any(
    circuit: Circuit | list[dict[str, Any]],
    effort: float = 0.1,
    noise: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Given a circuit in any known format, return a default config setup and serialized circuit.

    Parameters
    ----------
    circuit
        Circuit in Qiskit, Cirq or serialized format.
    effort
        A float between 0 and 1 that specifies the 'effort' that should be put
        into emulation. A number closer to 1 will aim to maximize fidelity of the emulation
        (up to memory limitations).
    noise
        Indicate whether this is a noisy simulation or not.

    Returns
    -------
    config
        Standard config based on the circuit.
    serialized_circuit
        Circuit in serialized format.
    """
    if not (isinstance(effort, (float, int)) and 0 <= effort <= 1):
        raise ValueError(f"Effort should be a float between 0 and 1 (got {effort}).")

    try:
        circuit = cast(Circuit, circuit)
        return standard_input_from_cirq_qiskit(circuit, effort, noise)
    except TypeError:
        circuit = cast(list[dict[str, Any]], circuit)
        return standard_input_from_serialized_circuit(circuit, effort, noise)


def standard_input_from_serialized_circuit(
    circuit: list[dict[str, Any]],
    effort: float = 0.1,
    noise: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Given a serialized circuit, return a default config setup.

    Parameters
    ----------
    circuit
        Circuit in serialized format.
    effort
        A float between 0 and 1 that specifies the 'effort' that should be put
        into emulation. A number closer to 1 will aim to maximize fidelity of the emulation
        (up to memory limitations).
    noise
        Indicate whether this is a noisy simulation or not.

    Returns
    -------
    config
        Standard config based on the circuit.
    serialized_circuit
        Circuit in serialized format.
    """
    qubits = get_qubits_from_serialized_circuit(circuit)

    # Get the standard configuration
    config = standard_config_from_serialized_circuit(
        serialized_circuit=circuit,
        serialized_qubits=qubits,
        effort=effort,
        noise=noise,
    )
    return config, circuit


def standard_input_from_cirq_qiskit(
    circuit: Circuit,
    effort: float = 0.1,
    noise: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Given a circuit in qiskit or cirq, return a default config setup that should perform well on this circuit, as well as a serialized circuit.

    The effort parameter is used to control how much computational effort will be put into emulating
    this circuit. More effort will usually mean higher fidelity, although it depends on the difficulty
    of the circuit.

    Parameters
    ----------
    circuit
        The circuit as qiskit QuantumCircuit or cirq Circuit.
    effort
        A float between 0 and 1 that specifies the 'effort' that should be put into emulation. A number closer to 1 will aim to maximize fidelity of the emulation (up to memory limitations).
    noise
        Indicate whether this is a noisy simulation or not.

    Returns
    -------
    config
        Config with standard settings.
    serialized_circuit
        Serialized circuit.
    """

    if not (isinstance(effort, (float, int)) and 0 <= effort <= 1):
        raise ValueError(f"Effort should be a float between 0 and 1 (got {effort}).")

    # Serialize the circuit and qubit objects
    serialized_circuit = serialize_circuit(circuit)
    qubits = get_default_qubit_objects(circuit)
    serialized_qubits = serialize_qubits(qubits)

    qubit_str_to_obj_map = {
        q_str: q_obj for q_str, q_obj in zip(serialized_qubits, qubits)
    }

    # Get the standard configuration
    config = standard_config_from_serialized_circuit(
        serialized_circuit=serialized_circuit,
        serialized_qubits=serialized_qubits,
        effort=effort,
        noise=noise,
    )

    # Set the qubit order and grouping back to be qubit objects
    config["qubits"] = qubits
    config["grouping"] = [
        [qubit_str_to_obj_map[q] for q in group] for group in config["grouping"]
    ]

    return config, serialized_circuit


def standard_config_from_serialized_circuit(
    serialized_circuit: list[dict[str, Any]],
    serialized_qubits: tuple[str, ...],
    effort: float = 0.1,
    noise: bool = False,
):
    """Given a serialized circuit, return a default config setup that should perform well on this circuit.

    The effort parameter is used to control how much computational effort will be put into emulating this circuit.
    More effort will usually mean higher fidelity, although it depends on the difficulty of the circuit.

    Parameters
    ----------
    serialized_circuit
        The serialized circuit.
    serialized_qubits
        The serialized qubits.
    effort
        A float between 0 and 1 that specifies the 'effort' that should be put into emulation.
        A number closer to 1 will aim to maximize fidelity of the emulation (up to memory limitations).
    noise
        A bool indicating whether this is a noisy simulation or not.

    Returns
    -------
    config:
        A dictionary with the standard configuration determined for the circuit.
    """
    # Group size is small for optimal memory usage
    if noise or len(serialized_qubits) == 2:
        max_group_size = 1
    else:
        max_group_size = 2

    # Heuristically select a grouping (and order) up to a maximum group size
    grouping, _ = grouping_from_circuit(
        serialized_circuit, serialized_qubits, max_group_size=max_group_size
    )

    # Compute the maximum bond dimension that saturates available memory
    bond_dim = bond_dim_from_grouping(grouping, noise=noise, effort=effort)

    # DMRG specific options (dmrg is the default emulation option)
    dmrg_config_settings = {
        "D": bond_dim,
        "convergence_window_size": 2 * len(grouping),  # Twice length of grouping
        "max_subcircuit_rows": NUM_ROWS,
        "mpo_bond_dim": None,
        "regular_grid": True,
        "truncate_rows": True,
    }

    # By default take 1000 samples
    output_settings = {}
    output_settings["expectation_values"] = {"enabled": False, "observables": []}
    output_settings["sampling"] = {"enabled": True, "n_shots": 1000}
    output_settings["mps"] = {"enabled": False}
    output_settings["amplitudes"] = {
        "enabled": False,
        "bitstrings": "all" if len(serialized_qubits) < 6 else [0],
    }

    config = {
        "mode": "dmrg",
        "qubits": list(serialized_qubits),
        "grouping": [[q for q in group] for group in grouping],
        "dmrg": dmrg_config_settings,
        "noise": {"validate_model": True},
        "output": output_settings,
    }

    return config


def grouping_from_circuit(
    serialized_circuit: list[dict[str, Any]],
    serialized_qubits: Sequence[str],
    max_group_size: int = 1,
) -> tuple[tuple[tuple[str, ...], ...], tuple[int, ...]]:
    """Given a circuit, produce a grouping of qubits that minimizes the number of between-group gates*.

    *Up to a maximum group size.

    Parameters
    ----------
    serialized_circuit :
        The  serialized circuit.
    serialized_qubits :
        The serialized qubits (as a sequence of strings).
    max_group_size :
        Maximum size of a qubit group.

    Returns
    -------
    qubit_grouping
        The qubit grouping arranged as a tuple of tuples of strings.
    mps_bond_indices
        A tuple of integers, specifying which bonds of the MPS connect
        different connected components of the circuit (and should be set to 1).
    """
    # Special case of a single qubit
    if len(serialized_qubits) == 1:
        return ((serialized_qubits[0],),), tuple()

    # Make the adjacency matrix of qubit-qubit interactions,
    # and construct the Fiedler vector as qubit ordering.
    A = grouping_to_adj_matrix([[q] for q in serialized_qubits], serialized_circuit)

    # If there are no 2-qubit gates, return a trivial grouping
    if np.allclose(A, 0):
        return tuple((q,) for q in serialized_qubits), tuple()

    # Loop over all connected components and append qubits
    # to qubit_order per connected component
    con_comps = get_connected_components(A.copy())
    grouping: list = []
    separating_bond_idxs = []  # bonds that separate connected components
    for cc in con_comps:
        cc_serialized_qubits = [serialized_qubits[i] for i in cc]
        grouping += grouping_for_connected_component(
            A[np.ix_(cc, cc)], cc_serialized_qubits, max_group_size
        )
        separating_bond_idxs.append(
            len(grouping) - 1
        )  # -1 because of convention mps.pad
    # Return grouping and all dim_one_bonds except the last (that's the rightmost bond)
    # (Also works if separating_bond_idxs is empty)
    return tuple(tuple(group) for group in grouping), tuple(separating_bond_idxs[:-1])


def grouping_to_adj_matrix(
    qubit_grouping: list[list[str]], circuit: list[dict[str, Any]]
) -> np.ndarray:
    """Return the adjacency matrix corresponding to a particular grouping and circuit.

    Given a grouping (list of list of string labels) and a circuit, returns an adjacency matrix
    with weighted edges representing the number of gates acting between groups in the grouping.

    Parameters
    ----------
    qubit_grouping :
        The grouping of qubits, given as a tuple of tuples of strings.
    circuit :
        The serialized circuit as a list of dicts.

    Returns
    -------
    GA
        The grouping adjacency matrix.
    """
    # Group index of each qubit
    qubit_group_idxs = {
        q: idx for idx, group in enumerate(qubit_grouping) for q in group
    }
    qubit_labels = list(qubit_group_idxs.keys())

    GA = np.zeros((len(qubit_grouping), len(qubit_grouping)))
    for gate in circuit:
        acts_on = gate["qubits"]
        if len(acts_on) == 2:
            q1, q2 = acts_on
            if q1 in qubit_labels and q2 in qubit_labels:
                GA[qubit_group_idxs[q1], qubit_group_idxs[q2]] += 1
                GA[qubit_group_idxs[q2], qubit_group_idxs[q1]] += 1
        elif len(acts_on) != 1:
            raise ValueError(f"Only 1- and 2-qubit gates are currently supported.")
    return GA


def get_connected_components(A: np.ndarray) -> list[list[int]]:
    """Output a list of connected components of an adjacency matrix.

    Each component will be a list of vertices indexed by integers.

    Parameters
    ----------
    A :
        The adjacency matrix describing the connections between components.

    Returns
    -------
    connected_components
        A list of connected components, each group being a list of integers.
    """

    def get_component_inds(B: np.ndarray) -> list[int]:
        """Given an adjacency matrix, do a breadth-first search to obtain the connected component of the first vertex.

        Parameters
        ----------
        B :
            The adjacency matrix.

        Returns
        -------
        connected_component
            List of integers (indices of vertices in connected component).
        """
        # Start with first vertex (indexed by 0)
        vertices_to_check = set([0])
        connected_component = set()
        while vertices_to_check:
            # pop next vertex and add to connected component
            next_vertex = vertices_to_check.pop()
            connected_component.add(next_vertex)
            # Add neighbors of next_vertex to vertices_to_check
            vertices_to_check = vertices_to_check.union(
                set(np.nonzero(B[next_vertex])[0])
            )
            # Remove all vertices that have been checked before
            vertices_to_check = vertices_to_check.difference(connected_component)
        return sorted(list(connected_component))

    remaining_vertices = [v for v in range(len(A[0:]))]
    connected_components = []
    while remaining_vertices:
        # Get single connected component
        component_inds = get_component_inds(A)
        # Map component indices to vertex labels
        connected_component = [remaining_vertices[i] for i in component_inds]
        # Append component to list of connected components
        connected_components.append(connected_component)
        # Remove rows and columns corresponding to component_inds from A
        # (pop above also removed them from remaining_vertices)
        A = np.delete(np.delete(A, component_inds, 0), component_inds, 1)
        # Update remaining_vertices
        remaining_vertices = [
            v for v in remaining_vertices if v not in connected_component
        ]
    return connected_components


def grouping_for_connected_component(
    A_cc: np.ndarray,
    qubits: Sequence[str],
    max_group_size: int = 1,
) -> list[list[str]]:
    """Returns the grouping for a connected component of a circuit.

    Given the adjancency matrix A_cc of a connected component, orders the
    qubits according to the fiedler ordering, then groups the qubits into groups
    of size 'max_group_size', and then constructs the adjacency matrix corresponding
    to the found grouping, and fiedler-orders the groups.

    Parameters
    ----------
    A_cc :
        The adjacency matrix of the connected component.
    qubits :
        Qubits (as a sequence of strings).
    max_group_size :
        Maximum size of a qubit group.

    Returns
    -------
    groups
        A list of groups, each group being a list of qubit labels (str).
    """
    # Fielder order of qubit (indices) within connected component
    qubit_idx_fiedler = list(_fiedler_order(A_cc))

    # Simple grouping is just the Fiedler ordering + collecting qubits into groups
    idx_grouping = [
        qubit_idx_fiedler[i : min(i + max_group_size, len(qubit_idx_fiedler))]
        for i in range(0, len(qubit_idx_fiedler), max_group_size)
    ]
    return [[qubits[i] for i in group] for group in idx_grouping]


def _fiedler_order(A: np.ndarray) -> np.ndarray:
    """Computes the Fiedler order of the vertices of adjacency matrix A.

    Parameters
    ----------
    A
        The adjacency matrix.

    Returns
    -------
    fiedler_order
        The Fiedler order of the vertices of A.
    """
    # If A is 1 x 1, return trivial ordering
    if A.shape[0] == 1:
        return np.array([0])

    # Construct graph Laplacian and compute Fiedler vector
    D = np.diag([sum(row) for row in A])  # Diagonal of degrees
    L = A - D  # Laplacian
    W, V = np.linalg.eigh(L)  # Take the eigendecomposition
    fiedler = V[
        :, -2
    ]  # Fiedler vector is the eigenvector corresponding to the first non-zero eigenvalue
    return np.argsort(fiedler)  # Return the order given by the Fiedler vector


def bond_dim_from_grouping(
    grouping: Sequence[Sequence[str]], noise: bool, effort: float = 0.1
) -> int:
    """Return the maximal bond dimension (up to a limit) for a particular grouping.

    Given a particular grouping, determines the maximal bond dimension
    that does not exceed a maximum space requirement (given by MAX_ELEMENTS).
    This function never returns a bond dimension larger than that needed for
    exact emulation.

    Parameters
    ----------
    grouping :
        The grouping of qubits.
    noise :
        Whether noise is on or off. If on, then the 'qubits' are taken to be dim-4 qudits.
    effort :
        Optional float between 0 and 1 that determines the effort put into obtaining
        a high-fidelity.

    Returns
    -------
    bond_dim
        The computed bond dimension.
    """
    # If there is only one group, we don't need a bond dimension
    if len(grouping) == 1:
        return 1

    phys_dim = 4 if noise else 2

    # Compute the maximum number of elements created without including the bond dimension
    group_dim = phys_dim ** max(len(group) for group in grouping)
    mpo_bond_dim = MPO_BOND_DIM_WITH_NOISE if noise else MPO_BOND_DIM_NO_NOISE
    mps_length = len(grouping)

    num_elements = _num_elements_without_bond_dim_dmrg(
        group_dim, mpo_bond_dim, mps_length, noise
    )

    max_bond_dim = int(np.floor(np.sqrt(MAX_ELEMENTS / num_elements)))

    # Compute the log of the minimum bond dim required for an exact emulation
    log_max_ltr = np.cumsum([len(group) for group in grouping[:-1]])
    log_max_rtl = np.cumsum([len(group) for group in grouping[::-1][:-1]])[::-1]
    log_exact_fidelity_bond_dim = np.max(list(map(min, zip(log_max_ltr, log_max_rtl))))

    # If the bond dimension for a fidelity one emulation is achievable below the 'easy' maximum,
    #  we always do that
    log_max_easy_bond_dim = np.log2(MAX_EASY_BOND_DIM) / np.log2(phys_dim)
    if log_exact_fidelity_bond_dim < log_max_easy_bond_dim:
        return phys_dim**log_exact_fidelity_bond_dim

    # Otherwise, if the exact is smaller than min(effort * max_bond_dim, MAX_EASY_BOND_DIM), we return that,
    #   else we return the maximum of the effort * max_bond_dim and the max_easy_bond_dim
    return min(
        phys_dim**log_exact_fidelity_bond_dim,
        max(effort * max_bond_dim, MAX_EASY_BOND_DIM),
    )
