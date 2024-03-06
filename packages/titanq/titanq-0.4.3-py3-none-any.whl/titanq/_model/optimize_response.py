from typing import Any, Dict, List, Tuple, Union
import numpy as np

class OptimizeResponse:
    """
    Object containing Optimization response and all its metrics.
    """
    def __init__(self, var_name: str, result_array: np.ndarray, metrics: Dict[str, Any]) -> None:
        self._var_name = var_name
        self._result_vector = result_array
        self._metrics = metrics

    def __getattr__(self, attr: str):
        # if attribute is the _var_name
        if attr == self._var_name:
            return self.result_vector()

        # else return the metrics name corresponding
        try:
            return self._metrics[attr]
        except KeyError as ex:
            raise AttributeError(attr) from ex


    def result_vector(self) -> np.ndarray:
        """
        :return: The result vector of this optimization.
        """
        return self._result_vector

    def result_items(self) -> List[Tuple[int, np.ndarray]]:
        """
        ex. [(-10000, [0, 1, 1, 0]), (-20000, [1, 0, 1, 0]), ...]

        :return: list of tuples containing the ising energy and it's corresponding result vector
        """
        return [(self.ising_energy[i], self._result_vector[i]) for i in range(len(self._result_vector))]

    def metrics(self, key: str = None) -> Union[str, Dict[str, Any]]:
        """
        :return: All metrics if no key is given of the specific metrics with the associated key if one is provided.

        :raise KeyError: The given key does not exist
        """
        if key:
            return self._metrics[key]
        else:
            return self._metrics
