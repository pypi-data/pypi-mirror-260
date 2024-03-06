import io
import json
import logging
import numpy as np
import zipfile
from typing import Any, Dict, List, Tuple

from .constraints import Constraints
from .errors import ConstraintsAlreadySetError, MaximumVariableLimitError, MissingVariableError, MissingObjectiveError, ObjectiveAlreadySetError, OptimizeError
from .objective import Objective, Target
from .optimize_response import OptimizeResponse
from .variable import VariableVector, Vtype
from .._client import api_model, Client
from .._storage import ManagedStorage, StorageClient

log = logging.getLogger("TitanQ")

_TITANQ_BASE_URL = "https://titanq.infinityq.io"


class Model:
    """
    Root object to define a problem to be optimize
    """

    def __init__(
        self,
        *,
        api_key: str,
        storage_client: StorageClient = None,
        base_server_url: str = _TITANQ_BASE_URL
        ) -> None:
        """
        Initiate the model with a storage client depending on the provided arguments.

        If the storage_client is missing, the storage will be managed by titanQ.

        NOTE: the storage manged by titanQ supports weight matrices with a size up to 10k

        :param api_key: TitanQ api key to access the service.
        :param storage_client: Storage to choose in order to store some items
        :param base_server_url: titanQ server url


        Example
        ~~~~~~~
        ..  highlight:: python
        ..  code-block:: python
        from titanq import Model, S3Storage

        # s3 storage on AWS
        model = Model(
            api_key="{insert API key here}",
            storage_client=S3Storage(
                access_key="{insert aws bucket access key here}",
                secret_key="{insert aws bucket secret key here}",
                bucket_name="{insert bucket name here}"
            )
        )

        # managed Storage (Up to 10k variables only)
        model = Model(api_key="{insert API key here}")
        """
        self._variables: VariableVector = None
        self._objective: Objective = None
        self._constraints: Constraints = None
        self._titanq_client = Client(api_key, base_server_url)

        # the user chose a managed storage or left it as default
        if storage_client is None:
            storage_client = ManagedStorage(self._titanq_client)

        self._storage_client = storage_client


    def add_variable_vector(self, name='', size=1, vtype=Vtype.BINARY):
        """
        Add a vector of variable to the model. Only a single vector of variables can be set.
        Calling this method again will override the current vector of variables

        :param name: The name given to this variable vector.
        :param size: The size of the vector.
        :param vtype: Type of the variables inside the vector.

        :raise MaximumVariableLimitError: If a variable is already defined.
        :raise ValueError: If the size of the vector is < 1.

        Example
        ~~~~~~~
        ..  highlight:: python
        ..  code-block:: python
        import numpy as np
        from titanq import Model, Vtype

        # set up model
        ...

        model.add_variable_vector('x', size, Vtype.BINARY)
        """
        if self._variables is not None:
            raise MaximumVariableLimitError("Cannot add additional variable without busting the maximum number of variable (1).")

        log.debug(f"add variable name='{name}'.")

        self._variables = VariableVector(name, size, vtype)


    def set_objective_matrices(self, weights: np.ndarray, bias: np.ndarray, target=Target.MINIMIZE):
        """
        Set the objective matrices for the model.

        :param weights: The quadratic objective matrix, **this matrix needs to be symmetrical**
        :type weights: a NumPy 2-D dense ndarray (must be float32)

        :param bias: The linear constraint vector
        :type bias:  a NumPy 1-D ndarray

        :param target: The target of this objective matrix.
        :type target: Target Enum

        :raise MissingVariableError: If no variable have been added to the model.
        :raise ObjectiveAlreadySetError: If an objective has already been setted in this model.
        :raise ValueError: If the weights shape or the bias shape does not fit the variable in the model.
        :raise ValueError: If the weights or bias data type is not f32.

        Example
        ~~~~~~~
        ..  highlight:: python
        ..  code-block:: python
        from titanq import Model, Target

        edges = {0:[4,5,6,7], 1:[4,5,6,7], 2:[4,5,6,7], 3:[4,5,6,7], 4:[0,1,2,3], 5:[0,1,2,3], 6:[0,1,2,3], 7:[0,1,2,3]}
        size = len(edges)

        # construct the weight matrix from the edges list
        weights = np.zeros((size, size), dtype=np.float32)
        for root, connections in edges.items():
            for c in connections:
                weights[root][c] = 1

        # construct the bias vector (Uniform weighting across all nodes)
        bias = np.asarray([0]*size, dtype=np.float32)

        # set up model
        ...

        model.set_objective_matrices(weights, bias, Target.MINIMIZE)
        """

        if self._variables is None:
            raise MissingVariableError("Cannot set objective before adding a variable to the model.")

        if self._objective is not None:
            raise ObjectiveAlreadySetError("An objective has already have been set for this model.")

        log.debug(f"set objective matrix and bias vector.")

        self._objective = Objective(self._variables.size(), weights, bias, target)


    def set_constraints_matrices(self, constraint_weights: np.ndarray, constraint_bounds: np.ndarray):
        """
        Set the constraints matrices for the model.

        :param constraint_weights: The constraint_weights matrix of shape (M, N) where M the number of constraints and N is the number of variables
        :type constraint_weights: a NumPy 2-D dense ndarray (must be float32)

        :param constraint_bounds: The constraint_bounds vector of shape (M,2) where M is the number of constraints
        :type constraint_bounds:  a NumPy 1-D ndarray (must be float32)

        :raise MissingVariableError: If no variable have been added to the model.
        :raise ConstraintsAlreadySetError: If a constraints has already been setted in this model.
        :raise ValueError: If the constraint_weights shape or the constraint_bounds shape does not fit the expected shape of this model.
        :raise ValueError: If the constraint_weights or constraint_bounds data type is not f32.
        """
        if self._variables is None:
            raise MissingVariableError("Cannot set constraints before adding a variable to the model.")

        if self._constraints is not None:
            raise ConstraintsAlreadySetError("Constraints has already have been set for this model.")

        log.debug(f"set weights constraints matrix and bias constraints vector.")

        self._constraints = Constraints(self._variables.size(), constraint_weights, constraint_bounds)


    def optimize(self, *, beta=[0.1], coupling_mult=0.5, timeout_in_secs=10.0, num_chains=8, num_engines=1, normalized=False):
        """
        Optimize this model.

        Note: All of the files used during the computation will be cleaned at the end.

        :param beta: beta hyper parameter used by the backend solver.
        :param coupling_mult: coupling_mult hyper parameter used by the backend solver.
        :param timeout_in_secs: Maximum time (in seconds) the backend solver can take to resolve this problem.
        :param num_chains: num_chains hyper parameter used by the backend solver.
        :param num_engines: num_engines parameter used by the backend solver.
        :param normalized: normalized paramater used by backend solver.

        :raise MissingVariableError: If no variable have been added to the model.
        :raise MissingObjectiveError: If no variable have been added to the model.

        Example
        ~~~~~~~
        ..  highlight:: python
        ..  code-block:: python
        # set up model, objective and variable
        ...

        # basic solve
        response = model.optimize(timeout_in_secs=60)

        # multiple engine
        response = model.optimize(timeout_in_secs=60, num_engines=2)

        # custom values
        response = model.optimize(beta=[0.1], coupling_mult=0.75, num_chains=8)

        # print values
        print("-" * 15, "+", "-" * 26, sep="")
        print("Ising energy   | Result vector")
        print("-" * 15, "+", "-" * 26, sep="")
        for ising_energy, result_vector in response.result_items():
            print(f"{ising_energy: <14f} | {result_vector}")
        """
        if self._variables is None:
            raise MissingVariableError("Cannot optimize before adding a variable to the model.")

        if self._objective is None:
            raise MissingObjectiveError("Cannot optimize before adding an objective to the model.")

        result, metrics = self._solve(beta, coupling_mult, timeout_in_secs, num_chains, num_engines, normalized)

        return OptimizeResponse(self._variables.name(), result, metrics)

    def _solve(self,
            beta: List[float],
            coupling_mult: float,
            timeout_in_secs: float,
            num_chains: int,
            num_engines: int,
            normalized: bool
        ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        issue a solve request and wait for it to complete.

        :param beta: beta hyper parameter used by the backend solver.
        :param coupling_mult: coupling_mult hyper parameter used by the backend solver.
        :param timeout_in_secs: Maximum time (in seconds) the backend solver can take to resolve this problem.
        :param num_chains: num_chains hyper parameter used by the backend solver.
        :param num_engines: num_engines parameter used by the backend solver.

        :return: the result numpy array and the metric json object
        """
        with self._storage_client.temp_files_manager(
            self._objective.bias(),
            self._objective.weights(),
            self._constraints.bias() if self._constraints else None,
            self._constraints.weights() if self._constraints else None,
        ) as temp_files:
            request = api_model.SolveRequest(
                input=temp_files.input(),
                output=temp_files.output(),
                parameters=api_model.Parameters(
                    beta=beta,
                    coupling_mult=coupling_mult,
                    num_chains=num_chains,
                    num_engines=num_engines,
                    normalized=normalized,
                    timeout_in_secs=timeout_in_secs,
                    variables_format=str(self._variables.vtype())
                )
            )

            solve_response = self._titanq_client.solve(request)

            # wait for result to be uploaded by the solver and download it
            archive_file_content = temp_files.download_result()
            with zipfile.ZipFile(io.BytesIO(archive_file_content), 'r') as zip_file:
                try:
                    metrics_content = zip_file.read("metrics.json")
                    result_content = zip_file.read("result.npy")
                except KeyError as ex:
                    try:
                        error_content = zip_file.read("error.json")
                        raise OptimizeError(json.loads(error_content)["error"]) from ex
                    except KeyError as e:
                        raise OptimizeError(
                            "Unexpected error in the solver, please contact titanQ support for more help" \
                            f" and provide the following computation id {solve_response.computation_id}") from e

        log.debug("Optimization completed")
        return np.load(io.BytesIO(result_content)), json.loads(metrics_content)
