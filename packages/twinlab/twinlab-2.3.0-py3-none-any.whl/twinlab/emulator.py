# Standard imports
import io
import json
from pprint import pprint
import time
from typing import Optional, Tuple, Union, List, Dict

# Third-party imports
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typeguard import typechecked

# Project imports
from . import api
from .dataset import Dataset
from .params import (
    TrainParams,
    ScoreParams,
    BenchmarkParams,
    SampleParams,
    PredictParams,
    RecommendParams,
    CalibrateParams,
    DesignParams,
)

from .plotting import plot, heatmap
from .plotting import DIGILAB_COLORS as digilab_colors
from .plotting import DIGILAB_CMAP as digilab_cmap
from .prior import Prior
from . import utils


# Converts between acquisiton function 'nice' names and their library names
ACQ_FUNC_DICT = {
    "EI": "EI",
    "qEI": "qEI",
    "LogEI": "LogEI",
    "qLogEI": "qLogEI",
    "PSD": "PSD",
    "qNIPV": "qNIPV",
    "ExpectedImprovement": "EI",
    "qExpectedImprovement": "qEI",
    "LogExpectedImprovement": "LogEI",
    "qLogExpectedImprovement": "qLogEI",
    "PosteriorStandardDeviation": "PSD",
    "qNegIntegratedPosteriorVariance": "qNIPV",
}

PING_TIME_TRAIN_DEFAULT = 5.0  # Seconds
PING_TIME_USE_DEFAULT = 5.0  # Seconds
PROCESSOR_DEFAULT = "cpu"


def _get_response_message(body):
    if "message" in body:  # TODO: Yuck!
        message = body["message"]
    else:
        message = body["process_status"]
    return message


class Emulator:
    """
    # Emulator

    A class representing a trainable twinLab emulator.

    ## Attributes:

    - `id`: `str`. This is the name of the emulator in the twinLab cloud.

    ## Methods:

    - `train()`. Performs the training of an emulator on the `twinLab` cloud.
    - `view()`. Returns the training parameters of a trained emulator on the `twinLab` cloud.
    - `summarise()`. Returns a statistical summary of a trained emulator on the `twinlab` cloud.
    - `score()`. Returns a calibration curve for a trained emulator on the `twinlab` cloud.
    - `benchmark()`. Returns a calibration curve for a trained emulator on the `twinlab` cloud.
    - `predict()`. Returns the emulator prediction on the specified input data.
    - `sample()`. Returns samples generated from the posterior distribution of the estimator.
    - `recommend()`. Returns candidate data points from a trained emulator on the `twinLab` cloud.
    - `calibrate()`. Returns a model that best suits the specified input data.
    - `delete()`. Deletes an emulator on the `twinlab` cloud.

    """

    @typechecked
    def __init__(self, id: str):
        self.id = id

        # @typechecked # TODO: Does not work with List[Prior]??

    def design(
        self,
        priors: List[Prior],
        num_points: int,
        params: DesignParams = DesignParams(),
        verbose: bool = False,
    ) -> pd.DataFrame:
        """
        # Design

        Get an initial design space for your emulator

        ## Arguments:

        - `priors`: `List[Prior]`. A list of `Prior` objects that define the prior distributions for each input.
        - `num_points`: `int`. Number of points to sample in each dimension.
        - `params`: `DesignParams`, `Optional`. An `DesignParams` object that contains all of the optional initial design parameters.

        ## Returns:

        - `pandas.DataFrame` containing the initial design space.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        emulator = tl.Emulator("emulator_id")

        my_priors = [
            tl.Prior("x1", tl.distribution.Uniform(0, 12)),
            tl.Prior("x2", tl.distribution.Uniform(0, 0.5)),
            tl.Prior("x3 ", tl.distribution.Uniform(0, 10)),
        ]

        initial_design = emulator.design(my_priors, 10)

        ```
        """
        # Convert priors to json so they can be passed through the API
        priors = [prior.to_json() for prior in priors]

        # Call the API function
        _, response = api.get_initial_design(
            priors,
            params.sampling_method.to_json(),
            num_points,
            seed=params.seed,
            verbose=verbose,
        )

        # Get result from body of response
        initial_design = utils.get_value_from_body("initial_design", response)
        initial_design = io.StringIO(initial_design)

        # Convert result which is a numpy array to pandas dataframe with correct column names
        initial_design_df = pd.read_csv(initial_design, sep=",")

        if verbose:
            print("Initial design:")
            print(initial_design_df)

        return initial_design_df

    @typechecked
    def train(
        self,
        dataset: Dataset,
        inputs: List[str],
        outputs: List[str],
        params: TrainParams = TrainParams(),
        ping_time: float = PING_TIME_TRAIN_DEFAULT,
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
    ) -> None:
        """
        # Train

        Train an emulator on the `twinLab` cloud.

        ## Arguments:

        - `dataset`: `Dataset`. twinLab dataset object which contains the training data for the emulator.
        - `inputs`: `list[str]`. List of input names in the training dataset.
        - `outputs`; `list[str]`. List of output names in the training dataset.
        - `params`: `TrainParams`, `optional`. A `TrainParams` object that contains all necessary training parameters.
        - `ping_time`: `float`, `optional`. Time  in seconds between pings to the server to check if the job is complete.
        - `processor`: `str`, `optional`. Processor to use for sampling. Can be either `"cpu"` or `"gpu"`.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator.train(dataset, ['X'], ['y'])
        ```
        """

        # Making a dictionary from TrainParams class
        train_dict = params.unpack_parameters()
        train_dict["inputs"] = inputs
        train_dict["outputs"] = outputs
        train_dict["dataset_id"] = dataset.id
        train_dict = utils.coerce_params_dict(train_dict)
        params_str = json.dumps(train_dict)
        _, response = api.train_model(
            self.id, params_str, processor=processor, verbose=debug
        )
        if verbose:
            message = utils.get_message(response)
            print(message)

        # Wait for job to complete
        complete = False
        while not complete:
            status = self.status(verbose=False, debug=debug)
            complete = utils.get_value_from_body("job_complete", status)
            time.sleep(ping_time)
        if verbose:
            print("Training complete!")

    @typechecked
    def status(
        self, verbose: Optional[bool] = False, debug: Optional[bool] = False
    ) -> dict:

        _, response = api.get_status_model(self.id, verbose=debug)

        if verbose:
            message = utils.get_message(response)
            print(message)
        return response

    @typechecked
    def view(self, verbose: bool = False, debug: bool = False) -> dict:
        """
        # View

        View an emulator that exists on the `twinLab` cloud.

        ## Arguments:

        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.

        ## Returns:

        - `dict` containing the emulator training parameters.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])
        emulator_params = emulator.view()
        print(emulator_params)
        ```
        """

        _, response = api.view_model(self.id, verbose=debug)
        parameters = (
            response  # Note that the whole body of the response is the parameters
        )
        if verbose:
            print("Emulator parameters summary:")
            pprint(parameters, compact=True, sort_dicts=False)
        return parameters

    @typechecked
    def view_train_data(
        self, verbose: bool = False, debug: bool = False
    ) -> pd.DataFrame:
        """
        # View Train Data

        View training data with which the emulator was trained in the `twinLab` cloud.

        ## Arguments:

        - `verbose`: `bool`, `Optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `Optional`. Determining level of information logged on the server. Default is False.

        ## Returns:

        - `Pandas.DataFrame` containing the training data on which the emulator was trained.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])
        training_dataset = emulator.view_train_data()
        print(training_dataset)
        ```
        """
        _, response = api.view_data_model(self.id, dataset_type="train", verbose=debug)
        train_csv_string = utils.get_value_from_body("training_data", response)
        train_csv_string = io.StringIO(train_csv_string)
        df_train = pd.read_csv(train_csv_string, sep=",", index_col=0)
        if verbose:
            print("Training data")
            pprint(df_train)
        return df_train

    @typechecked
    def view_test_data(
        self, verbose: bool = False, debug: bool = False
    ) -> pd.DataFrame:
        """
        # View Test Data

        View test data on which the emulator was tested in the `twinLab` cloud.

        ## Arguments:

        - `verbose`: `bool`, `Optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `Optional`. Determining level of information logged on the server. Default is False.

        ## Returns:

        - `Pandas.DataFrame` containing the test data on which the emulator was tested.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])
        test_dataset = emulator.view_test_data()
        print(test_dataset)
        ```
        """
        _, response = api.view_data_model(self.id, dataset_type="test", verbose=debug)
        test_csv_string = utils.get_value_from_body("test_data", response)
        test_csv_string = io.StringIO(test_csv_string)
        df_test = pd.read_csv(test_csv_string, sep=",", index_col=0)
        if verbose:
            print("Test data")
            pprint(df_test)
        return df_test

    @typechecked
    def summarise(self, verbose: bool = False, debug: bool = False) -> dict:
        """
        # Summarise

        Get summary statistics for a pre-trained emulator in the `twinLab` cloud.

        ## Arguments:

        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.


        ## Returns:

        - `dict` containing summary statistics for the pre-trained emulator.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])
        info = emulator.summarise()
        print(info)
        ```
        """
        _, response = api.summarise_model(self.id, verbose=debug)
        summary = utils.get_value_from_body("model_summary", response)
        del summary["data_diagnostics"]
        if verbose:
            print("Trained emulator summary:")
            pprint(summary, compact=True, sort_dicts=False)
        return summary

    @typechecked
    def _use_method(
        self,
        method: str,
        df: Optional[pd.DataFrame] = None,
        df_std: Optional[pd.DataFrame] = None,
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
        **kwargs,  # NOTE: This can be *anything*
    ) -> Union[io.StringIO, list, float]:
        if df is not None:
            data_csv = df.to_csv(index=False)
        else:
            data_csv = None
        if df_std is not None:
            data_std_csv = df_std.to_csv(index=False)
        else:
            data_std_csv = None
        _, response = api.use_model(
            self.id,
            method,
            data_csv=data_csv,
            data_std_csv=data_std_csv,
            processor=processor,
            verbose=debug,
            **kwargs,
        )

        if method in ["predict", "sample", "get_candidate_points", "solve_inverse"]:
            output_csv = utils.get_value_from_body("dataframe", response)
            return io.StringIO(output_csv)
        else:
            output_list = utils.get_value_from_body("result", response)
            return output_list

    @typechecked
    def score(
        self,
        params: ScoreParams = ScoreParams(),
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
    ) -> list:
        """
        # Score

        Quantify the performance of your trained emulator with an emulator score.
        Note that a test dataset must have been defined in order for this to produce a meaningful result.
        This means that `train_test_ratio` must be less than 1 when training your emulator.

        ## Arguments:

        - `params`: `ScoreParams`, `optional`. A `ScoreParams` object that contains all necessary scoring parameters.
        - `processor`: `str`, `optional`. Processor to use for sampling. Can be either `"cpu"` or `"gpu"`.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        ### Returns:

        - `List` containing the trained model score.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        dataset = tl.Dataset("my_dataset")
        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        params = tl.TrainParams(train_test_ratio=0.75)
        emulator.train(dataset, ['X'], ['y'], params)
        score = emulator.score()
        print(score)
        ```
        """

        list = self._use_method(
            method="score",
            **params.unpack_parameters(),
            processor=processor,
            verbose=verbose,
            debug=debug,
        )
        if verbose:
            print("Emulator Score:")
            print(list)
        return list

    @typechecked
    def benchmark(
        self,
        params: BenchmarkParams = BenchmarkParams(),
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
    ) -> list:
        """
        # Benchmark

        Quantify the performance of your trained emulator with a calibration curve.
        Note that a test dataset must have been defined in order for this to produce a meaningful result.
        This means that `train_test_ratio` must be less than 1 when training your emulator.

        ## Arguments:

        - `params`: `BenchmarkParams`, `optional`. A `BenchmarkParams` object that contains all parameters for benchmarking the emulators.
        - `processor`: `str`, `optional`. Processor to use for sampling. Can be either `"cpu"` or `"gpu"`.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        ## Returns:

        - `List` containing the data for the calibration curve.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)

        emulator = tl.Emulator("emulator_id")
        params = tl.TrainParams(train_test_ratio=0.75)
        emulator.train(dataset, ['X'], ['y'], params)

        # Plot the calibration curve
        fraction_observed = emulator.benchmark()
        fraction_expected = np.linspace(0,1,fraction_observed.shape[0])

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_title("Calibration curve")
        ax.set_xlabel("Expected coverage")
        ax.set_ylabel("Observed coverage")

        plt.plot(np.linspace(0, 1, 100), fraction_observed)
        plt.plot(np.linspace(0, 1, 100), np.linspace(0, 1, 100), "--")
        plt.show()
        ```
        """

        list = self._use_method(
            method="get_calibration_curve",
            **params.unpack_parameters(),
            processor=processor,
            verbose=verbose,
            debug=debug,
        )
        if verbose:
            print("Calibration curve information:")
            pprint(list)
        return list

    @typechecked
    def predict(
        self,
        df: pd.DataFrame,
        params: PredictParams = PredictParams(),
        sync: bool = False,
        ping_time: float = PING_TIME_USE_DEFAULT,
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        # Predict

        Make predictions from a pre-trained emulator that exists on the `twinLab` cloud.

        ## Arguments:

        - `df`: `pandas.DataFrame`. A `pandas.DataFrame` containing the values to make predictions on.
        - `params`: `PredictParams`. A `PredictParams` object that contains parameters to make predictions.
        - `sync`: `bool`, `optional`, determining whether to use synchronous or asynchronous method
        - `ping_time`: `float`, `optional`, time between pings to the server to check if the job is complete [s]
        - `processor`: `str`, `optional`. Processor to use for sampling. Can be either `"cpu"` or `"gpu"`.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        **NOTE:** Evaluation data must be a .csv file, or a `pandas.DataFrame` that is interpretable as a .csv file.

        ## Returns:

        - `tuple` containing:
            - `df_mean`: `pandas.DataFrame` containing mean predictions.
            - `df_std`: `pandas.DataFrame` containing standard deviation predictions.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])
        df_test = pd.DataFrame({'X': [1.5, 2.5, 3.5]})
        df_mean, df_std = emulator.predict(df_test)
        print(df_mean)
        print(df_std)
        ```
        """

        if sync:
            csv = self._use_method(
                method="predict",
                df=df,
                **params.unpack_parameters(),
                processor=processor,
                verbose=verbose,
                debug=debug,
            )
        else:
            # Send off the request to predict
            status, response = api.use_request_model(
                model_id=self.id,
                method="predict",
                data_csv=utils.get_csv_string(df),
                **params.unpack_parameters(),
                processor=processor,
                verbose=debug,
            )
            process_id = utils.get_value_from_body("process_id", response)

            # Wait for job to complete
            status = 202
            while status == 202:
                status, response = api.use_response_model(
                    model_id=self.id,
                    method="predict",
                    process_id=process_id,
                    verbose=debug,
                )
                if verbose:
                    message = _get_response_message(response)
                    print("Job status:", message)
                time.sleep(ping_time)

            csv = utils.get_value_from_body("dataframe", response)
            csv = io.StringIO(csv)

        # Munge the response into the mean and std
        df = pd.read_csv(csv, sep=",")
        n = len(df.columns)
        df_mean, df_std = df.iloc[:, : n // 2], df.iloc[:, n // 2 :]
        df_std.columns = df_std.columns.str.removesuffix(" [std_dev]")
        if verbose:
            print("Mean predictions:")
            print(df_mean)
            print("Standard deviation predictions:")
            print(df_std)

        return df_mean, df_std

    @typechecked
    def sample(
        self,
        df: pd.DataFrame,
        num_samples: int,
        params: SampleParams = SampleParams(),
        sync: bool = False,
        ping_time: float = PING_TIME_USE_DEFAULT,
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
    ) -> pd.DataFrame:
        """
        # Sample

        Draw samples from a pre-trained emulator that exists on the `twinLab` cloud.

        ## Arguments:

        - `df` : `pandas.DataFrame`. A `pandas.DataFrame` containing the values to sample from.
        - `num_samples`: `int`. Number of samples to draw for each row of the evaluation data.
        - `params`: `SampleParams`, `optional`. A `SampleParams` object with sampling parameters.
        - `sync`: `bool`, `optional`. If true, send synchronous cloud request, else send asynchronous request.
        - `ping_time`: `float`, `optional`. Time in seconds to wait between each synchronous results response fetch.
        - `processor`: `str`, `optional`. Processor to use for sampling. Can be either `"cpu"` or `"gpu"`.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        **NOTE:** Evaluation data must be a .csv file, or a `pandas.DataFrame` that is interpretable as a .csv file.

        ## Returns:

        - `pandas.DataFrame` with the sampled values.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)

        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])

        df = pd.DataFrame({'X': [1.5, 2.5, 3.5]})
        n = 10
        df_samples = emulator.sample(df, n)
        print(df_samples)

        df_single_sample = tl.get_sample(df_samples, 0) # Accessing Sample 1
        print(df_single_sample)
        ```
        """

        if sync:
            csv = self._use_method(
                method="sample",
                df=df,
                num_samples=num_samples,
                **params.unpack_parameters(),
                processor=processor,
                verbose=verbose,
                debug=debug,
            )
        else:
            # Send off the request to predict
            status, response = api.use_request_model(
                model_id=self.id,
                method="sample",
                data_csv=utils.get_csv_string(df),
                num_samples=num_samples,
                **params.unpack_parameters(),
                processor=processor,
                verbose=debug,
            )
            process_id = utils.get_value_from_body("process_id", response)

            # Wait for job to complete
            status = 202
            while status == 202:
                status, response = api.use_response_model(
                    model_id=self.id,
                    method="sample",
                    process_id=process_id,
                    verbose=debug,
                )
                if verbose:
                    message = _get_response_message(response)
                    print("Job status:", message)
                time.sleep(ping_time)

            csv = utils.get_value_from_body("dataframe", response)
            csv = io.StringIO(csv)

        # Return results
        df_result = pd.read_csv(csv, header=[0, 1], sep=",")
        if verbose:
            print("Samples:")
            print(df_result)
        return df_result

    @typechecked
    def recommend(
        self,
        num_points: int,
        acq_func: str,
        params: RecommendParams = RecommendParams(),
        sync: bool = False,
        ping_time: float = PING_TIME_USE_DEFAULT,
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
    ) -> pd.DataFrame:
        """
        # Recommend

        Draw new candidate data points via active learning from a pre-trained emulator
        that exists on the `twinLab` cloud.

        ## Arguments:
        - `num_points`: `int`. Number of samples to draw for each row of the evaluation data.
        - `acq_func`: `str`. Specifies the acquisition function to be used when recommending new points; this can be chose from a list of possible fucntions:
        `"ExpectedImprovement"`, `"qExpectedImprovement"`, `"LogExpectedImprovement"`, `"qLogExpectedImprovement"`, `"PosteriorStandardDeviation"`, `"qNegIntegratedPosteriorVariance"`.
        - `params`: `RecommendParams`, `optional`. A `RecommendParams` object that contains all recommendation parameters.
        - `sync`: `bool`, `optional`. If `True`, send synchronous cloud request, else send asynchronous request.
        - `ping_time`: `float`, `optional`. Time in seconds between pings to the server to check if the job is complete.
        - `processor`: `str`, `optional`. Processor to use for sampling. Can be either `"cpu"` or `"gpu"`.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        ## Returns:

        - `pandas.DataFrame` containing the recommended sample locations.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)

        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])
        n = 10
        df = emulator.recommend(n, 'qEI')
        print(df)
        ```
        """

        if sync:
            csv = self._use_method(
                model_id=self.id,
                method="get_candidate_points",
                num_points=num_points,
                acq_func=ACQ_FUNC_DICT[acq_func],
                **params.unpack_parameters(),
                processor=processor,
                verbose=verbose,
                debug=debug,
            )

        else:
            # Send off the request to recommend
            status, response = api.use_request_model(
                model_id=self.id,
                method="get_candidate_points",
                num_points=num_points,
                acq_func=ACQ_FUNC_DICT[acq_func],
                **params.unpack_parameters(),
                processor=processor,
                verbose=debug,
            )

            process_id = utils.get_value_from_body("process_id", response)

            # Wait for job to complete
            status = 202
            while status == 202:
                status, response = api.use_response_model(
                    model_id=self.id,
                    method="get_candidate_points",
                    process_id=process_id,
                    verbose=debug,
                )
                if verbose:
                    message = _get_response_message(response)
                    print("Job status:", message)
                time.sleep(ping_time)

            csv = utils.get_value_from_body("dataframe", response)
            csv = io.StringIO(csv)

        df = pd.read_csv(csv, sep=",")
        if verbose:
            print("Recommended samples:")
            print(df)

        return df

    @typechecked
    def calibrate(
        self,
        df_obs: pd.DataFrame,
        df_std: pd.DataFrame,
        params: CalibrateParams = CalibrateParams(),
        sync: bool = False,
        ping_time: float = PING_TIME_USE_DEFAULT,
        processor: str = PROCESSOR_DEFAULT,
        verbose: bool = False,
        debug: bool = False,
    ) -> pd.DataFrame:
        """
        # Calibrate

        Given a set of observations, inverse modelling finds the model that would best suit the data.

        ## Arguments:

        - `df_obs` : `pandas.DataFrame`. A `pandas.DataFrame` containing the observations.
        - `df_std` : `pandas.DataFrame`. A `pandas.DataFrame` containing the error on the observations.
        - `params`: `CalibrateParams`, `optional`. A `CalibrateParams` object that contains all calibration parameters.
        - `sync`: `bool`, `optional`, determining whether to use synchronous or asynchronous method
        - `ping_time`: `float`, `optional`, time between pings to the server to check if the job is complete [s]
        - `processor`: `str`, `optional`. Processor to use for sampling. Can be either `"cpu"` or `"gpu"`.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        ## Returns:

        - `pandas.DataFrame` containing the recommended model statistics.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])
        data_csv = pd.DataFrame({'y': [1]})
        data_std_csv = pd.DataFrame({'y': [0.498]})
        df = emulator.calibrate(data_csv, data_std_csv)
        print(df)
        ```
        """

        if sync:
            csv = self._use_method(
                method="solve_inverse",
                df=df_obs,
                df_std=df_std,
                **params.unpack_parameters(),
                processor=processor,
                verbose=verbose,
                debug=debug,
            )

            df = pd.read_csv(csv, sep=",")

        else:
            # Send off the request to predict
            status, response = api.use_request_model(
                model_id=self.id,
                method="solve_inverse",
                data_csv=utils.get_csv_string(df_obs),
                data_std_csv=utils.get_csv_string(df_std),
                **params.unpack_parameters(),
                processor=processor,
                verbose=debug,
            )
            process_id = utils.get_value_from_body("process_id", response)

            # Wait for job to complete
            status = 202
            while status == 202:
                status, response = api.use_response_model(
                    model_id=self.id,
                    method="solve_inverse",
                    process_id=process_id,
                    verbose=debug,
                )
                if verbose:
                    message = _get_response_message(response)
                    print("Job status:", message)
                time.sleep(ping_time)

            # convert to csv
            csv = utils.get_value_from_body("dataframe", response)
            csv = io.StringIO(csv)

            # deal with Unnamed column in summary table
            # TODO: This seems like a nasty hack
            df = pd.read_csv(csv, sep=",")
            df = df.set_index("Unnamed: 0")
            df.index.name = None
            if "Unnamed: 0.1" in df.columns:
                df = df.drop("Unnamed: 0.1", axis=1)

        if verbose:
            print("Inverse model statistics:")
            print(df)

        return df

    @typechecked
    def delete(self, verbose: bool = False, debug: bool = False) -> None:
        """
        # Delete

        Delete emulator from the `twinLab` cloud.

        ## Arguments:

        - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        emulator = tl.Emulator("emulator_id")
        emulator.train(dataset, ['X'], ['y'])

        emulator.delete()
        ```
        """

        _, response = api.delete_model(self.id, verbose=debug)
        if verbose:
            message = utils.get_message(response)
            print(message)

    @typechecked
    def plot(
        self,
        x_axis: str,
        y_axis: str,
        x_fixed: Dict[str, float] = {},
        x_lim: Optional[Tuple[float, float]] = None,
        label: str = "Emulator",
        color: str = digilab_colors["light_blue"],
        verbose: bool = False,
        debug: bool = False,
    ) -> plt:
        """
        # Plot

        Plot the predictions from an emulator across a single dimension with one and two standard deviation bands.
        This will make a call to the emulator to predict across the specified dimension.
        Note that a multi-dimensional emulator will be sliced across the other dimensions.
        The matplotlib.pyplot object is returned, and can be further modified by the user.

        ## Arguments:
        - `x_axis`: `str`. The name of the x-axis variable.
        - `y_axis`: `str`. The name of the y-axis variable.
        - `x_lim`: `Tuple[float, float]`, `Optional`. The limits of the x-axis. If not provided, the limits will be taken directly from the emulator.
        - `x_fixed`: `dict`, `Optional`. A dictionary of fixed values for the other X variables. Note that all X variables of your emulator must either be specified as x_axis or appear as x_fixed keys. To pass through "None", either leave x_fixed out or pass through an empty dictionary.
        - `label`: `str`. The label for the line in the plot, defaults to "Emulator prediction".
        - `color`: `str`. The color of the plot, defaults to digiLab blue. Can be any valid matplotlib color (https://matplotlib.org/stable/gallery/color/named_colors.html)
        - `verbose`: `bool`, `Optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `Optional`. Determining level of information logged on the server. Default is False.

        ## Returns:
        - `matplotlib.pyplot` object

        ## Example:

        ```python
        import twinlab as tl

        emulator = tl.Emulator("emulator_id") # A pre-trained emulator
        plt = emulator.plot("Time", "Temperature", x_fixed={"Latitude": 0, "Longitude": 30})
        plt.show()
        ```
        """
        # Parameters
        n = 100  # Number of points in X

        # Get information about inputs/outputs from the emulator
        _, response = api.summarise_model(self.id, verbose=debug)
        inputs = set(response["model_summary"]["data_diagnostics"]["inputs"].keys())
        outputs = set(response["model_summary"]["data_diagnostics"]["outputs"].keys())

        # Check function inputs
        if x_axis not in inputs:
            raise ValueError(f"x_axis must be one of the Emulator inputs: {inputs}")
        if y_axis not in outputs:
            raise ValueError(f"y_axis must be one of the Emulator outputs: {outputs}")
        if set([x_axis] + list(x_fixed.keys())) != inputs:
            raise ValueError(
                f"All values {inputs} must be specified as either x_axis or x_fixed keys"
            )

        # Get the range for the x-axis
        if x_lim is not None:
            xmin, xmax = x_lim
        else:
            inputs = response["model_summary"]["data_diagnostics"]["inputs"]
            xmin, xmax = inputs[x_axis]["min"], inputs[x_axis]["max"]

        # Create a dataframe on which to predict
        X = {x_axis: np.linspace(xmin, xmax, n)}
        for x_col, x_val in x_fixed.items():
            X[x_col] = x_val * np.ones(n)
        df_X = pd.DataFrame(X)

        # Predict using the emulator
        df_mean, df_std = self.predict(df_X, verbose=verbose, debug=debug)

        # Plot the results
        plt = plot(x_axis, y_axis, df_X, df_mean, df_std, color=color, label=label)
        return plt  # Return the plot

    @typechecked
    def heatmap(
        self,
        x1_axis: str,
        x2_axis: str,
        y_axis: str,
        x_fixed: Dict[str, float] = {},
        x1_lim: Optional[Tuple[float, float]] = None,
        x2_lim: Optional[Tuple[float, float]] = None,
        cmap=digilab_cmap,
        verbose: bool = False,
        debug: bool = False,
    ) -> plt:
        """
        # Heatmap

        Plot a heatmap of the predictions from an emulator across two dimensions.
        The uncertainty of the emulator is not plotted here.
        This will make a call to the emulator to predict across the specified dimensions.
        Note that a higher-than-two-dimensional emulator will be sliced across the other dimensions.
        The matplotlib.pyplot object is returned, and can be further modified by the user.

        ## Arguments:
        - `x1_axis`: `str`. The name of the x1-axis variable (horizonal axis).
        - `x2_axis`: `str`. The name of the x2-axis variable (vertical axis).
        - `y_axis`: `str`. The name of the plotted variable (heatmap).
        - `x_fixed`: `dict`, `Optional`. A dictionary of fixed values for the other X variables. Note that all X variables of your emulator must either be specified as x1_axis, x2_axis, or appear as x_fixed keys. To pass through "None", either leave x_fixed out or pass through an empty dictionary.
        - `cmap`: `str`. The color of the plot, defaults to digiLab palette. Can be any valid matplotlib color (https://matplotlib.org/stable/users/explain/colors/colormaps.html).
        - `verbose`: `bool`, `Optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `Optional`. Determining level of information logged on the server. Default is False.

        ## Returns:
        - `matplotlib.pyplot` object

        ## Example:

        ```python
        import twinlab as tl

        emulator = tl.Emulator("emulator_id") # A pre-trained emulator
        plt = emulator.heatmap("Latitude", "Longitude", "Rainfall", x_fixed={"Month": 6})
        plt.show()
        ```
        """
        # Parameters
        n = 25  # Number of points in each X dimension

        # Get information about inputs/outputs from the emulator
        _, response = api.summarise_model(self.id, verbose=debug)
        inputs = set(response["model_summary"]["data_diagnostics"]["inputs"].keys())
        outputs = set(response["model_summary"]["data_diagnostics"]["outputs"].keys())

        # Check function inputs
        if x1_axis not in inputs:
            raise ValueError(f"x1_axis must be one of the Emulator inputs:{inputs}")
        if x2_axis not in inputs:
            raise ValueError(f"x2_axis must be one of the Emulator inputs: {inputs}")
        if y_axis not in outputs:
            raise ValueError(f"y_axis must be one of the Emulator outputs: {outputs}")
        if set([x1_axis, x2_axis] + list(x_fixed.keys())) != inputs:
            raise ValueError(
                f"All values {inputs} must be specified as either x1_axis, x2_axis, or x_fixed keys"
            )

        # Get the ranges for the x-axes
        inputs = response["model_summary"]["data_diagnostics"]["inputs"]
        if x1_lim is None:
            x1min, x1max = inputs[x1_axis]["min"], inputs[x1_axis]["max"]
        else:
            x1min, x1max = x1_lim
        if x2_lim is None:
            x2min, x2max = inputs[x2_axis]["min"], inputs[x2_axis]["max"]
        else:
            x2min, x2max = x2_lim

        # Create a grid of points
        x1 = np.linspace(x1min, x1max, n)
        x2 = np.linspace(x2min, x2max, n)
        X1, X2 = np.meshgrid(x1, x2)

        # Create a dataframe on which to predict
        X = {x1_axis: X1.flatten(), x2_axis: X2.flatten()}
        if x_fixed is not None:
            for x_col, x_val in x_fixed.items():
                X[x_col] = x_val * np.ones(n**2)
        df_X = pd.DataFrame(X)

        # Predict using the emulator
        # NOTE: Uncertainty is discarded here
        df_mean, _ = self.predict(df_X, verbose=verbose, debug=debug)

        # Plot the results
        plt = heatmap(
            x1_axis,
            x2_axis,
            y_axis,
            df_X,
            df_mean,
            cmap,
        )
        return plt  # Return the plot
