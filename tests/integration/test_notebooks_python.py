# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
import pytest
import papermill as pm
from tests.notebooks_common import OUTPUT_NOTEBOOK, KERNEL_NAME


TOL = 0.5


@pytest.mark.integration
@pytest.mark.parametrize(
    "size, result_list",
    [
        ("1m", [0.06, 0.30, 0.27, 0.10]),
        ("10m", [0.10, 0.32, 0.27, 0.15]),
        #       ("20m", [0.03, 0.15, 0.14, 0.08]), # raises MemoryError
    ],
)
def test_als_pyspark_integration(notebooks, size, result_list):
    notebook_path = notebooks["sar_single_node"]
    pm.execute_notebook(
        notebook_path,
        OUTPUT_NOTEBOOK,
        kernel_name=KERNEL_NAME,
        parameters=dict(TOP_K=10, MOVIELENS_DATA_SIZE=size),
    )
    nb = pm.read_notebook(OUTPUT_NOTEBOOK)
    df = nb.dataframe
    result_map = df.loc[df["name"] == "map", "value"].values[0]
    assert result_map == pytest.approx(result_list[0], TOL)
    result_ndcg = df.loc[df["name"] == "ndcg", "value"].values[0]
    assert result_ndcg == pytest.approx(result_list[1], TOL)
    result_precision = df.loc[df["name"] == "precision", "value"].values[0]
    assert result_precision == pytest.approx(result_list[2], TOL)
    result_recall = df.loc[df["name"] == "recall", "value"].values[0]
    assert result_recall == pytest.approx(result_list[3], TOL)

