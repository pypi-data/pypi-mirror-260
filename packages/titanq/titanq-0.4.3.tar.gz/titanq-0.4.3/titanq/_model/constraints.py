
import numpy as np


class Constraints:
    """
    Constraints passed to TitanQ platform. It is consisted of the constraint_weights matrix and the constraint_bounds vector.
    """

    def __init__(self, variable_size: int, constraint_weights: np.ndarray, cosntraint_bounds: np.ndarray) -> None:
        """
        :raise ValueError:
        """
        bias_shape = cosntraint_bounds.shape
        weights_shape = constraint_weights.shape

        # validate shapes
        if len(weights_shape) != 2:
            raise ValueError(f"constraint_weights should be a 2d matrix. Got something with shape: {weights_shape}")

        if len(bias_shape) != 2:
            raise ValueError(f"constraint_bounds should be a 2d matrix. Got something with shape: {bias_shape}")

        if weights_shape[1] != variable_size:
            raise ValueError(f"constraint_weights shape does not match variable size. Expected (M, {variable_size}) where M is the number of constraints")
        n_constraints = weights_shape[0]

        if n_constraints == 0:
            raise ValueError("Need at least 1 constraints")

        if bias_shape[0] != n_constraints:
            raise ValueError(f"constraint_bounds shape does not match constraint_weights size. Expected ({n_constraints}, 2)")

        if bias_shape[1] != 2:
            raise ValueError(f"constraint_bounds shape is expected to be ({n_constraints}, 2)")


        # validate dtype
        if constraint_weights.dtype != np.float32:
            raise ValueError(f"Weights constraints vector dtype should be np.float32")

        if cosntraint_bounds.dtype != np.float32:
            raise ValueError(f"Bias constraints vector dtype should be np.float32")

        self._bias = cosntraint_bounds
        self._weights = constraint_weights

    def bias(self) -> np.ndarray:
        """
        :return: The bias vector of this constraint.
        """
        return self._bias

    def weights(self) -> np.ndarray:
        """
        :return: The weights matrix of this constraint.
        """
        return self._weights