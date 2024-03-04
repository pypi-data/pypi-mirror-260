import typing as t

import numpy as np
import pandas as pd

from regression import __version__ as _version
from regression.config.core import config
from regression.processing.data_manager import load_pipeline
from regression.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
loan_amount_pipeline = load_pipeline(filename=pipeline_file_name)


def make_prediction(*, input_data: t.Union[pd.DataFrame, dict]) -> dict:
    """make prediction using the saved model pipeline"""

    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)
    results = {}

    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = loan_amount_pipeline.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": [np.expm1(pred) for pred in predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results
