from typing import Any


class PauliObservable:
    """Class for storing a product of single-qubit Pauli observables.

    Contain the different observables together with their
    respective coefficients (relevant when combining several
    PauliObservables into one PauliSumObservable).

    Attributes
    ----------
    paulis: dict[str, str]
        dictionary with qubit labels (str) as keys, and a Pauli operator
        ('X', 'Y', or 'Z') as values
    coeff: complex
        a complex-valued coefficient.
    """

    def __init__(self, paulis: dict[str, str], coeff: complex):
        if any([p not in ["X", "Y", "Z"] for p in paulis.values()]):
            raise ValueError("Pauli operators must be 'X', 'Y', or 'Z'")
        if any(not isinstance(k, str) for k in paulis.keys()):
            raise ValueError(
                "The qubit labels used as keys in Pauli Observables must be strings"
            )
        self.paulis = paulis
        self.coeff = coeff


class PauliSumObservable:
    """Class for observables composed of a linear combination of local Pauli operators.
    Each PauliObservable contains a 'coeff' attribute that stores the coefficient of the
    operator in question.

    Attributes
    ----------
    observables: list[PauliObservable]
        a list of PauliObservables
    name: str
        name of the PauliSumObservable.
    """

    def __init__(
        self,
        observables: list[PauliObservable],
        name: str,
    ):
        self.observables = observables
        self.name = name

    def serialize(self) -> dict[str, Any]:
        """Serializes the class instance into a tuple of lists, dicts, strings and floats.

        Returns
        -------
        payload:
            a dictionary containing the following fields

            - "serialized_observables": a lists of dicts representing the observables,
            - "name": a str for the name.
        """

        # Serialize PauliObservables
        serialized_observables = []
        for ob in self.observables:
            serialized_observables.append({"paulis": ob.paulis, "coeff": ob.coeff})

        # Return payload
        return {"serialized_observables": serialized_observables, "name": self.name}

    @classmethod
    def deserialize(cls, payload: dict[str, Any]):
        """Deserializes the payload and creates a class instance.

        Parameters
        ----------
        payload:
            a dictionary containing the following fields:

            - "serialized_observables": a lists of dicts representing the observables,
            - "name": a str for the name.

        Returns
        -------
        pauli_sum_observable:
            A PauliSumObservable instance.
        """

        # Create PauliObservables
        observables: list[PauliObservable] = []
        for sob in payload["serialized_observables"]:
            paulis: dict[str, str] = sob["paulis"]
            coeff: float = sob["coeff"]
            observables.append(PauliObservable(paulis, coeff))

        return cls(observables, payload["name"])
