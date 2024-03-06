import datetime
import io
import json
import uuid
import numpy as np
import pytest
from typing import Any, Dict, List
import zipfile

from titanq import Model, Vtype, errors, Target
from titanq._storage.s3_storage import S3Storage
from titanq._storage.managed_storage import ManagedStorage
from titanq._client.model import SolveResponse

from .mock import TitanQClientMock, MockS3StorageClient

from collections import namedtuple


def file_in_filename_list(filename: str, filename_list: List[str]) -> bool:
    return any(filename in s for s in filename_list)

def np_array_to_bytes(arr: np.ndarray) -> bytes:
    buf = io.BytesIO()
    np.save(buf, arr)
    return buf.getvalue()

@pytest.fixture
def mock_metrics() -> Dict[str, Any]:
    return {"metrics1": 1, "metrics2": "value2"}

@pytest.fixture
def mock_result() -> Dict[str, Any]:
    return [np.random.rand(10).astype(np.float32) for _ in range(10)]

@pytest.fixture
def mock_s3_storage(mock_metrics, mock_result) -> MockS3StorageClient:
    # expected npy result file content
    expected_result_buffer = io.BytesIO()
    np.save(expected_result_buffer, mock_result)

    # set mock client with mock values
    buff = io.BytesIO()
    with zipfile.ZipFile(buff, 'w') as file:
        file.writestr("result.npy", expected_result_buffer.getvalue())
        file.writestr("metrics.json", json.dumps(mock_metrics).encode())

    return MockS3StorageClient(buff.getvalue())

@pytest.fixture
def mock_titanq_client() -> TitanQClientMock:
    return TitanQClientMock(solve_response=SolveResponse(
        computation_id=str(uuid.uuid4()),
        status="queued",
        message="Computation have been queued"
    ))

@pytest.fixture
def model_s3_client(mock_s3_storage, mock_titanq_client) -> Model:
    model = Model(
        api_key="test_api_key",
        storage_client=mock_s3_storage
    )

    model._titanq_client = mock_titanq_client
    return model


@pytest.fixture
def constant_datetime(monkeypatch):
    constant_datetime = datetime.datetime(2024,1,1,8,0,0)
    class MockDatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return constant_datetime

    monkeypatch.setattr(datetime, 'datetime', MockDatetime)
    return constant_datetime

@pytest.mark.parametrize("api_key, storage_client ,expected_storage_class", [
    ("api_key", S3Storage(access_key="aws_access_key", secret_key="aws_secret_access_key", bucket_name="bucket_name"), S3Storage),
    ("api_key", ManagedStorage(TitanQClientMock()), ManagedStorage),
])
def test_selected_storage(api_key, storage_client, expected_storage_class):
    model = Model(api_key=api_key, storage_client=storage_client)
    assert isinstance(model._storage_client, expected_storage_class)


@pytest.mark.parametrize("name, size, vtype, error", [
    ('x', 1, Vtype.BINARY, None),
    ('x', 47, Vtype.BINARY, None),
    ('x', -1, Vtype.BINARY, ValueError),
    ('x', 0, Vtype.BINARY, ValueError)
])
def test_new_variable(model_s3_client, name, size, vtype, error):
    if error:
        with pytest.raises(error):
            model_s3_client.add_variable_vector(name, size, vtype)
    else:
        model_s3_client.add_variable_vector(name, size, vtype)


def test_multiple_variable(model_s3_client):
    model_s3_client.add_variable_vector('x', 1, Vtype.BINARY)

    with pytest.raises(errors.MaximumVariableLimitError):
        model_s3_client.add_variable_vector('y', 2, Vtype.BINARY)


@pytest.mark.parametrize("weights_shape, bias_shape, objective, error", [
    ((10, 10), (10,), Target.MINIMIZE, None),
    ((11, 10), (10,), Target.MINIMIZE, ValueError),
    ((10, 11), (10,), Target.MINIMIZE, ValueError),
    ((11, 11), (10,), Target.MINIMIZE, ValueError),
    ((10, 10, 10), (10,), Target.MINIMIZE, ValueError),
    ((10,), (10,), Target.MINIMIZE, ValueError),
    ((10,10), (9,), Target.MINIMIZE, ValueError),
    ((10,10), (10,1), Target.MINIMIZE, ValueError),
    ((10,10), (10,2), Target.MINIMIZE, ValueError),
])
def test_set_objective(model_s3_client, weights_shape, bias_shape, objective, error):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    weights = np.random.rand(*weights_shape).astype(np.float32)
    bias = np.random.rand(*bias_shape).astype(np.float32)

    if error:
        with pytest.raises(error):
            model_s3_client.set_objective_matrices(weights, bias, objective)
    else:
        model_s3_client.set_objective_matrices(weights, bias, objective)

@pytest.mark.parametrize("weights_data_type, bias_data_type, error", [
    (np.float32, np.float32, None),
    (np.float64, np.float32, ValueError),
    (np.float32, np.float64, ValueError),
    (np.int32, np.float32, ValueError),
    (np.float32, np.int32, ValueError),
    (np.bool_, np.float32, ValueError),
    (np.float32, np.bool_, ValueError),
    (np.byte, np.float32, ValueError),
    (np.float32, np.byte, ValueError),
    (np.short, np.float32, ValueError),
    (np.float32, np.short, ValueError),
])
def test_objective_matrices_data_type(model_s3_client, weights_data_type, bias_data_type, error):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    weights = np.random.rand(10, 10).astype(weights_data_type)
    bias = np.random.rand(10).astype(bias_data_type)

    if error:
        with pytest.raises(error):
            model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)
    else:
        model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)


def test_set_objective_without_variable(model_s3_client):
    weights = np.random.rand(10, 10)
    bias = np.random.rand(10)

    with pytest.raises(errors.MissingVariableError):
        model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)


def test_set_2_objective(model_s3_client):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    weights = np.random.rand(10, 10).astype(np.float32)
    bias = np.random.rand(10).astype(np.float32)

    model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)

    with pytest.raises(errors.ObjectiveAlreadySetError):
        model_s3_client.set_objective_matrices(weights, bias, Target.MINIMIZE)


def test_optimize_no_variable(model_s3_client):
    with pytest.raises(errors.MissingVariableError):
        model_s3_client.optimize()


def test_optimize_no_objective(model_s3_client):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    with pytest.raises(errors.MissingObjectiveError):
        model_s3_client.optimize()


def test_optimize_no_constraints(model_s3_client, mock_s3_storage, mock_metrics, mock_result):
    model = model_s3_client

    # optimize using sdk
    weights = np.random.rand(10, 10).astype(np.float32)
    bias = np.random.rand(10).astype(np.float32)

    model.add_variable_vector('x', 10, Vtype.BINARY)
    model.set_objective_matrices(weights, bias)
    response = model.optimize()

    assert response.metrics() == mock_metrics
    assert (response.result_vector() == mock_result).all()

    assert mock_s3_storage.array_uploaded['bias'] == np_array_to_bytes(bias)
    assert mock_s3_storage.array_uploaded['weights'] == np_array_to_bytes(weights)
    assert mock_s3_storage.array_uploaded['constraint_weights'] == None
    assert mock_s3_storage.array_uploaded['constraint_bounds'] == None

    assert mock_s3_storage.file_removed

def test_optimize_with_constraints(model_s3_client, mock_s3_storage, mock_metrics, mock_result):
    model = model_s3_client

    # optimize using sdk
    weights = np.random.rand(10, 10).astype(np.float32)
    constraint_weights = np.random.rand(4, 10).astype(np.float32)
    bias = np.random.rand(10).astype(np.float32)
    constraint_bounds = np.random.rand(4, 2).astype(np.float32)

    model.add_variable_vector('x', 10, Vtype.BINARY)
    model.set_objective_matrices(weights, bias)
    model.set_constraints_matrices(constraint_weights, constraint_bounds)
    response = model.optimize()

    assert response.metrics() == mock_metrics
    assert (response.result_vector() == mock_result).all()

    assert mock_s3_storage.array_uploaded['bias'] == np_array_to_bytes(bias)
    assert mock_s3_storage.array_uploaded['weights'] == np_array_to_bytes(weights)
    assert mock_s3_storage.array_uploaded['constraint_weights'] == np_array_to_bytes(constraint_weights)
    assert mock_s3_storage.array_uploaded['constraint_bounds'] == np_array_to_bytes(constraint_bounds)

    assert mock_s3_storage.file_removed

@pytest.mark.parametrize("vtype", [
    Vtype.BINARY, Vtype.BIPOLAR,
])
def test_vtype_sent(model_s3_client, mock_titanq_client, vtype):
    model = model_s3_client
    mock_client = mock_titanq_client

    # optimize using sdk
    weights = np.random.rand(10, 10).astype(np.float32)
    bias = np.random.rand(10).astype(np.float32)

    model.add_variable_vector('x', 10, vtype)
    model.set_objective_matrices(weights, bias)

    model.optimize()

    assert mock_client.request_sent.parameters.variables_format == str(vtype)

@pytest.mark.parametrize("constraint_weights_shape, constraint_bounds_shape, error", [
    ((2, 10), (2,2), None),
    ((10, 10), (10,2), None),
    ((2, 10), (3,2), ValueError),
    ((2, 10), (2,), ValueError),
    ((2, 10), (10,2), ValueError),
    ((10, 2), (2,2), ValueError),
    ((10, ), (1,2), ValueError),
    ((2, 10), (3,2), ValueError),
    ((2, 11), (2,2), ValueError),
    ((0, 10), (0,2), ValueError),
])
def test_set_constraints(model_s3_client, constraint_weights_shape, constraint_bounds_shape, error):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    constraint_weights = np.random.rand(*constraint_weights_shape).astype(np.float32)
    constraint_bounds = np.random.rand(*constraint_bounds_shape).astype(np.float32)

    if error:
        with pytest.raises(error):
            model_s3_client.set_constraints_matrices(constraint_weights, constraint_bounds)
    else:
        model_s3_client.set_constraints_matrices(constraint_weights, constraint_bounds)

@pytest.mark.parametrize("constraint_weights_dtype, constraint_bounds_dtype, error", [
    (np.float32, np.float32, None),
    (np.float64, np.float32, ValueError),
    (np.float32, np.float64, ValueError),
    (np.int32, np.int32, ValueError),
])
def test_constraints_dtype(model_s3_client, constraint_weights_dtype, constraint_bounds_dtype, error):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    constraint_weights = np.random.rand(2, 10).astype(constraint_weights_dtype)
    constraint_bounds = np.random.rand(2, 2).astype(constraint_bounds_dtype)

    if error:
        with pytest.raises(error):
            model_s3_client.set_constraints_matrices(constraint_weights, constraint_bounds)
    else:
        model_s3_client.set_constraints_matrices(constraint_weights, constraint_bounds)


def test_constraints_without_variable(model_s3_client):
    constraint_weights = np.random.rand(2, 10).astype(np.float32)
    constraint_bounds = np.random.rand(2).astype(np.float32)

    with pytest.raises(errors.MissingVariableError):
        model_s3_client.set_constraints_matrices(constraint_weights, constraint_bounds)


def test_set_constraints_multiple_time(model_s3_client):
    model_s3_client.add_variable_vector('x', 10, Vtype.BINARY)

    weights = np.random.rand(2, 10).astype(np.float32)
    bias = np.random.rand(2, 2).astype(np.float32)
    model_s3_client.set_constraints_matrices(weights, bias)

    with pytest.raises(errors.ConstraintsAlreadySetError):
        model_s3_client.set_constraints_matrices(weights, bias)