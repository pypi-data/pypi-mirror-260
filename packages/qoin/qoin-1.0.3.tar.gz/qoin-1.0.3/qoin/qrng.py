# Copyright 2023-2024 Amir Ali Malekani Nezhad.
#
# Licensed under the GPL Ver 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://github.com/ACE07-Sev/QRandom/blob/main/LICENSE
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

__all__ = ['QRNG']

from abc import ABC
from collections.abc import Iterable
from typing import Any
import math

# Import `Qiskit` modules
from qiskit import (QuantumCircuit, execute)
from qiskit_aer import AerSimulator


class QRNG(ABC):
    """ `QRNG` class provides random number generation using quantum computing.
    """
    def __init__(self) -> None:
        """ Initialize a `QRNG` instance.
        """
        self._backend = AerSimulator()

    def randint(self,
                lowerbound: int,
                upperbound: int) -> int:
        """ Generate a random integer from [lowerbound, upperbound).

        Parameters
        ----------
        `lowerbound` (int):
            The lowerbound of the selection.
        `upperbound` (int):
            The upperbound of the selection.

        Returns
        -------
        `random_int` (int): The random number generated from the selection.
        """
        # Define delta (difference between upperbound and lowerbound)
        delta = upperbound - lowerbound

        # Scale delta to the closest power of 2
        scale = delta/2 ** math.ceil(math.log2(delta))
        delta = int(delta/scale)

        # Calculate the number of qubits needed to represent the selection
        num_qubits = math.ceil(math.log2(delta))

        # Define the circuit
        circuit = QuantumCircuit(num_qubits, num_qubits)

        # Create a uniform distribution over all possible integers
        circuit.h(range(num_qubits))

        # Apply measurement
        circuit.measure(range(num_qubits), range(num_qubits))

        # Run the circuit
        counts = execute(circuit,
                         self._backend,
                         shots=1).result().get_counts()

        # Postprocess measurement result
        random_int = int(list(dict(counts).keys())[0], 2)

        # Scale the integer back
        random_int = int(random_int*scale)

        # shift random integer's range from [0;upperbound-lowerbound-1]
        # to [lowerbound;upperbound-1]
        random_int += lowerbound

        # Return random integer
        return random_int

    def random(self,
               num_digits: int) -> float:
        """ Generate a random float between 0 and 1.

        Parameters
        ----------
        `num_bits` (int):
            The number of bits used to represent the angle divider.

        Returns
        -------
        `random_float`(float): The random generated float.
        """
        # Initialize the digit
        random_float = "0."

        for _ in range(num_digits):
            # Generate a random integer between 0 and 9
            random_float += str(self.randint(0, 9))

        # Return the random float
        return float(random_float)

    def choice(self,
               items: Iterable[Any]) -> Any:
        """ Choose a random element from the list of items.

        Parameters
        ----------
        `items` (Iterable[Any]):
            The list of items.

        Returns
        -------
        (Any): The item selected.
        """
        return items[self.randint(0, len(items))]

    def choices(self,
                items: Iterable[Any],
                num_selections: int) -> Any | Iterable[Any]:
        """ Choose random element(s) from the list of items.

        Parameters
        ----------
        `items` (Iterable[Any]):
            The list of items.
        `num_selections` (int):
            The number of selections.

        Returns
        -------
        (Any | Iterable[Any]): The item(s) selected.
        """
        # Define indices list
        indices = []

        # If number of selections is 1, run `.choice` instead.
        if num_selections == 1:
            return self.choice(items)

        # Generate the random indices
        indices = [self.randint(0, len(items)) for _ in range(num_selections)]

        # Return the selections
        return [items[i] for i in indices]

    def sample(self,
               items: Iterable[Any],
               num_selections: int) -> Any | Iterable[Any]:
        """ Choose random element(s) from the list of items.

        Parameters
        ----------
        `items` (Iterable[Any]):
            The list of items.
        `num_selections` (int):
            The number of selections.

        Returns
        -------
        (Any | Iterable[Any]): The item(s) selected.
        """
        # Define indices list
        indices = []

        # If number of selections is 1, run `.choice` instead.
        if num_selections == 1:
            return self.choice(items)

        while True:
            # If the number of selections is met, break the loop
            if len(indices) == num_selections:
                break

            # Generate a random index
            random_index = self.randint(0, len(items))

            # If the random index generated is not unique, do not append it
            if random_index not in indices:
                indices.append(random_index)

        # Return the selections
        return [items[i] for i in indices]