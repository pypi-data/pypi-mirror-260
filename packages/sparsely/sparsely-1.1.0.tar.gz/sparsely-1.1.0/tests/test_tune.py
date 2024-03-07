import numpy as np
import pandas as pd
import pytest

from sparsely import tune_estimator, SparseLinearRegressor


@pytest.mark.parametrize("max_iters_no_improvement", [None, 1])
@pytest.mark.parametrize("return_search_log", [True, False])
def test_tune_estimator(
    regression_dataset: tuple[
        np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray
    ],
    max_iters_no_improvement: int,
    return_search_log: bool,
):
    X_train, X_test, y_train, y_test, coef = regression_dataset
    output = tune_estimator(
        X_train,
        y_train,
        estimator=SparseLinearRegressor(),
        k_min=1,
        k_max=5,
        max_iters_no_improvement=max_iters_no_improvement,
        return_search_log=return_search_log,
    )
    if return_search_log:
        estimator, search_log = output
        assert isinstance(search_log, pd.DataFrame)
        assert (search_log.columns == ["k", "score", "std"]).all()
        if max_iters_no_improvement is None:
            assert len(search_log) == 5
        else:
            assert 1 < len(search_log) < 5
    else:
        estimator = output
    assert estimator.score(X_train, y_train) > 0.8
    assert estimator.score(X_test, y_test) > 0.8
    assert estimator._coef.shape == (X_train.shape[1],)
    assert (~np.isclose(coef, 0)).sum() <= estimator._k
    assert (np.isclose(estimator._coef, 0) == np.isclose(coef, 0)).all()
