# importing necessary libraries

# For data encoding
from feature_engine.encoding import OneHotEncoder

# ===== for feature engineering ===== #
# For imputation
from feature_engine.imputation import (
    AddMissingIndicator,
    CategoricalImputer,
    MeanMedianImputer,
)

# For Data transformation
from feature_engine.transformation import LogCpTransformer
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from regression.config.core import config

loan_amount_pipeline = Pipeline(
    [
        # ===== IMPUTATION =====
        # add missing indicator to numerical variables
        (
            "missing_indicator",
            AddMissingIndicator(variables=config.model_config.num_var_na),
        ),
        # impute numerical variables with the median
        (
            "median_imputation",
            MeanMedianImputer(
                imputation_method="median", variables=config.model_config.num_var_na
            ),
        ),
        # impute categorical variables with string missing
        (
            "categorical_imputation",
            CategoricalImputer(
                imputation_method="missing", variables=config.model_config.cat_vars_na
            ),
        ),
        # == CATEGORICAL ENCODING ======
        # encode categorical variables using one hot encoding into k-1 variables
        (
            "categorical_encoder",
            OneHotEncoder(drop_last=True, variables=config.model_config.cat_vars),
        ),
        # === variable transformation ======
        (
            "log",
            LogCpTransformer(
                variables=config.model_config.num_cont_vars, C=config.model_config.C
            ),
        ),
        # scale
        ("scaler", StandardScaler()),
        # Adding our final estimator
        (
            "SGD",
            SGDRegressor(
                alpha=config.model_config.alpha,
                max_iter=config.model_config.max_iter,
                random_state=config.model_config.random_state,
            ),
        ),
    ]
)
