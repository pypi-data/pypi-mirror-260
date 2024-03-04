import numpy as np
from config.core import config
from pipeline import loan_amount_pipeline
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """ " train the model."""

    # read the training data
    data = load_dataset(filename=config.app_config.training_data)

    # divide the train and val
    x_train, x_test, y_train, y_test = train_test_split(
        data[config.model_config.features],
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    # Obtain the mode of the target variabke and use it in filling missing data
    mode = int(y_train.mode())

    # to address missing values in loanamount, which is  our target variable
    # we can replace nan with 0
    y_train = y_train.fillna(mode)

    # we apply logarithm transformation
    y_train = np.log1p(y_train)

    # fit the model
    loan_amount_pipeline.fit(x_train, y_train)

    # persist the trained model
    save_pipeline(pipeline_to_persist=loan_amount_pipeline)


if __name__ == "__main__":
    run_training()
