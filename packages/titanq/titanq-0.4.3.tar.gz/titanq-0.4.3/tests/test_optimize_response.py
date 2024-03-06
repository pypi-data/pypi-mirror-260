import numpy as np

from titanq import OptimizeResponse

def test_get_variable_result():
    result = np.random.rand(6).astype(np.float32)
    response = OptimizeResponse("x",  result, {})

    assert np.array_equal(response.x, result)
    assert np.array_equal(response.result_vector(), result)


def test_get_metrics():
    metrics = {"metrics1": 1, "metrics2": "value2"}
    response = OptimizeResponse("x",  np.random.rand(6).astype(np.float32), metrics)

    assert response.metrics1 == metrics["metrics1"]
    assert response.metrics2 == metrics["metrics2"]
    assert response.metrics("metrics1") == metrics["metrics1"]
    assert response.metrics("metrics2") == metrics["metrics2"]
    assert response.metrics() == metrics