# Standard imports
import warnings
from typing import Union, Optional, List

# Third-party imports
import pandas as pd

# Project imports
from .dataset import Dataset
from .sampling import Sampling, LatinHypercube


class EstimatorParams:
    """
    # Estimator parameter configuration

    Estimator parameter configuration used in twinLab.

    ## Attributes

    - `detrend`: `bool`, `optional`. Specifies whether to linear detrend the output data before estimator fitting, default is False.
    - `device`: `str`, `optional`. Specifies whether to fit the estimator using "cpu" or "gpu". Default is "cpu".
    - `covar_module`: `str`, `optional`. Specifies the covariance modules for the GP; this can be chosen from a list of possible kernels: `'LIN'`, `'M12'`, `'M32'`, `'M52'`, `'PER'`, `'RBF'`, `'RQF'`. Kernels can also be composed by using `+` and `*` e.g. `"(M52*PER)+RQF`.
    - `estimator_type`: `str`, `optional`. Specifies the GP estimator; this can be chosen from a list of possible emulators: `'single_task_gp'`, `'fixed_noise_gp'`, `'heteroskedastic_gp'`, `'variational_gp'`, `'multi_fidelity_gp'`, `'fixed_noise_multi_fidelity_gp'`.
    """

    def __init__(
        self,
        detrend: bool = False,
        device: str = "cpu",  # TODO: Does this interact with Modal cpu/gpu?
        covar_module: Optional[str] = None,
        estimator_type: Optional[str] = None,
    ):
        self.detrend = detrend
        self.device = device
        self.covar_module = covar_module
        self.estimator_type = estimator_type

    def unpack_parameters(self):
        params = {
            "detrend": self.detrend,
            "device": self.device,
            "covar_module": self.covar_module,
            "estimator_type": self.estimator_type,
        }

        # Logic to avoid sending the covar_module arg to the library for estimators that do not take it as an argument
        # TODO This should be moved to the library level
        if (
            params["estimator_type"]
            in [
                "heteroskedastic_gp",
                "multi_fidelity_gp",
                "fixed_noise_multi_fidelity_gp",
            ]
            and params["covar_module"] != None
        ):
            params.pop("covar_module")
            warnings.warn(
                f"Estimator of type {params['estimator_type']} is not compatible with covariance module selection. Therefore the keyword argument covar_modules will be ignored."
            )

        elif (
            params["estimator_type"]
            in [
                "heteroskedastic_gp",
                "multi_fidelity_gp",
                "fixed_noise_multi_fidelity_gp",
            ]
            and params["covar_module"] == None
        ):
            params.pop("covar_module")

        return params


class ModelSelectionParams:
    """
    # Model selection parameter configuration

    Class for model selection parameter configuration used in twinLab.

    ## Attributes

    - `seed`: `int`, `optional`. Specifies the seed for the random number generator for every trial of the model selection process.
    - `evaluation_metric`: `str`, `optional`. Specifies the evaluation metric used to score different configuration during the model selection process. Can be `"BIC"` or `"MSLL"`. Default is `"MSLL"`.
    - `val_ratio`: `float`, `optional`. Specifies the percentage of random validation data allocated to to compute the `"BIC"` metric. Default is `0.2`.
    - `base_kernels`: Union[`str`,`Set[str]`], `optional`. Specifies the list of kernels to use for Compositional Kernel Search. Can be `"all"`, `"restricted"` or `Set[str]` object. The set of available kernels are ["LIN", "M12", "M32", "M52", "PER", "RBF", "RQF"]. Default is `"restricted"` and uses ["LIN", "M32", "M52", "PER", "RBF"].
    - `depth`: `int`, `optional`. Specifies the number of base kernels to be combined in the Compositional Kernel Search. A `depth=3` means the resulting kernel may be composed from three base kernels, e.g. "(LIN+PER)RBF" or "(M12RBF)+RQF". Default is `1`.
    - `beam`: `int`, `optional`. Specifies the beam width of the Compositional Kernel Search algorithm. A `beam=1` is an exhaustive search (algorithmically 'greedy'), `beam=None` performs breadth-first search, and `beam>1` performs beam search with the specified beam value. Default is `None`.
    - `resources_per_trial`: `dict`, `optional`. The amount of CPU and GPU resources allocated to each trial of model selection. Default is `{"cpu": 1, "gpu": 0}`.
    """

    def __init__(
        self,
        seed: Optional[int] = None,
        evaluation_metric: str = "MSLL",
        val_ratio: float = 0.2,
        base_kernels: Union[str, set] = "restricted",
        depth: int = 1,
        beam: Optional[int] = None,
        resource_per_trial: dict = {"cpu": 1, "gpu": 0},
    ):
        self.seed = seed
        self.evaluation_metric = evaluation_metric
        self.val_ratio = val_ratio
        self.base_kernels = base_kernels
        self.depth = depth
        self.beam = beam
        self.resource_per_trial = resource_per_trial

    def unpack_parameters(self):
        params = {
            "seed": self.seed,
            "evaluation_metric": self.evaluation_metric,
            "val_ratio": self.val_ratio,
            "base_kernels": self.base_kernels,
            "depth": self.depth,
            "beam": self.beam,
            "resource_per_trial": self.resource_per_trial,
        }
        return params


class TrainParams:
    """
    # Emulator training parameters

    Parameters that should be passed to the emulator on training.

    ## Attributes

    - `estimator`: `str`, `optional`. The type of estimator used in the pipeline. Can be either `"gaussian_process_regression"` or `"gradient_boosting_regression"`.
    - `estimator_params`: `EstimatorParams`, `optional`. The parameters for the estimator.
    - `input_retained_dimensions`: `int`, `optional`. The number of dimensions to retain after the truncation of the SVD (Singular Value Decomposition) for functional input.
    - `input_explained_variance`: `float`, `optional`. Specifies how much of the
                    variance should be explained after the truncation of the SVD
                    (Singular Value Decomposition) for functional input.
    - `output_retained_dimensions`: `int`, `optional`. The number of dimensions to retain after the truncation of the SVD (Singular Value Decomposition) for functional output.
    - `output_explained_variance`: `float`, `optional`. Specifies how much of the
                    variance should be explained after the truncation of the SVD
                    (Singular Value Decomposition) for functional output.
    - `fidelity`: `str`, `optional`. Name of the fidelity parameter.
    - `train_test_ratio`: `float`, `optional`. Specifies the ratio of training samples in the dataset.
    - `dataset_std`: `Dataset`, `optional`. A twinLab dataset object which contains the standard deviation of the training data.
    - `model_selection`: `bool`, `optional`. Whether to run model selection.
    - `model_selection_params`: `ModelSelectionParams`, `optional`. The parameters for model selection.
    - `seed`: `int`, `optional`. Seed used to initialise the random number generators for reproducibility.
    """

    def __init__(
        self,
        estimator: str = "gaussian_process_regression",
        estimator_params: EstimatorParams = EstimatorParams(),
        input_explained_variance: Optional[float] = None,
        input_retained_dimensions: Optional[int] = None,
        output_explained_variance: Optional[float] = None,
        output_retained_dimensions: Optional[int] = None,
        fidelity: Optional[str] = None,
        dataset_std: Optional[Dataset] = None,
        train_test_ratio: float = 1.0,
        model_selection: bool = False,
        model_selection_params: ModelSelectionParams = ModelSelectionParams(),
        seed: Optional[int] = None,
    ):
        # Below: parameters that will be passed to the emulator on construction
        self.fidelity = fidelity
        self.estimator = estimator
        self.estimator_params = estimator_params
        self.input_explained_variance = input_explained_variance
        self.input_retained_dimensions = input_retained_dimensions
        self.output_explained_variance = output_explained_variance
        self.output_retained_dimensions = output_retained_dimensions
        # Below: parameters that will be passed to the emulator.fit() method
        self.dataset_std = dataset_std
        self.train_test_ratio = train_test_ratio
        self.model_selection = model_selection
        self.model_selection_params = model_selection_params
        self.seed = seed

    def unpack_parameters(self):
        # TODO: params from above -> kwargs here?
        setup_params = {  # Pass to the campaign in the library
            "fidelity": self.fidelity,
            "estimator": self.estimator,
            "estimator_kwargs": self.estimator_params.unpack_parameters(),
            "input_explained_variance": self.input_explained_variance,
            "input_retained_dimensions": self.input_retained_dimensions,
            "output_explained_variance": self.output_explained_variance,
            "output_retained_dimensions": self.output_retained_dimensions,
        }
        train_params = {  # Pass to campaign.fit() in the library
            "train_test_ratio": self.train_test_ratio,
            "model_selection": self.model_selection,
            "model_selection_kwargs": self.model_selection_params.unpack_parameters(),
            "seed": self.seed,
        }
        if self.dataset_std is not None:
            train_params["dataset_std_id"] = self.dataset_std.id
        return {**setup_params, **train_params}


### ###


### Score ###
class ScoreParams:
    """
    # Emulator.score parameters

    Class for Emulator.score parameters.

    ## Attributes

    - `combined_score`, `bool`. Determining whether to average scores across dimensions. If False, will return a `numpy` array, even if only one dimension.
    """

    def __init__(
        self,
        combined_score: bool = False,
    ):
        self.combined_score = combined_score

    def unpack_parameters(self):
        return {"combined_score": self.combined_score}


### ###

### Benchmark ###


class BenchmarkParams:
    """
    # Emulator.benchmark parameters

    Class for Emulator.benchmark parameters.

    ## Attributes

    - type: `str`, `optional`. Specifies the type of benchmark to be performed. Can be `"quantile"` or `"interval"`. The default is `"quantile"`.
    """

    def __init__(
        self,
        type: str = "quantile",
    ):
        self.type = type

    def unpack_parameters(self):
        return {"type": self.type}


### ###

### Predict ###


class PredictParams:
    """
    # Emulator.predict parameters

    Class for Emulator.predict parameters.

    ## Attributes

    - `observation_noise`: `bool`, `optional`. Whether to include aleatoric noise in the standard deviation of the prediction. Only valid for `"gaussian_process_regression"`. Defaults to True.
    """

    def __init__(
        self,
        observation_noise: bool = True,
    ):
        self.observation_noise = observation_noise

    def unpack_parameters(self):
        return {"kwargs": {"observation_noise": self.observation_noise}}


### ###

### Sample ###


class SampleParams:
    """
    # Emulator.sample parameters

    Class for Emulator.sample parameters.

    ## Attributes

    - `seed`: `int`, `optional`. Seed used to initialise the random number generators for reproducibility.
    - `fidelity`: `pandas.DataFrame`, `optional`. Fidelity information provided if `estimator_type="multi_fidelity_gp"`. Must be a single column `pandas.DataFrame` with the same sample order as X.
    """

    def __init__(
        self,
        seed: Optional[int] = None,
        fidelity: Optional[pd.DataFrame] = None,
    ):
        self.seed = seed
        self.fidelity = fidelity

    def unpack_parameters(self):
        params = {"kwargs": {"seed": self.seed, "fidelity": self.fidelity}}
        return params


### ###

### Recommend ###


class AcqFuncParams:
    """
    # Acquisition function parameters

    Class for acquisition function parameter configuration used in twinLab.

    ## Attributes

    - `weights`: `list[float]`, `optional`. A list of weighting values used to scalarise the objective function in case of a multi-output model. Default is equal weights for each dimension.
    """

    def __init__(
        self,
        weights: Optional[List[float]] = None,
        # mc_points: Optional[int] = None, # TODO: Cannot be included because tensor
    ):
        self.weights = weights
        self.mc_points = None

    def unpack_parameters(self):
        params = {"weights": self.weights, "mc_points": self.mc_points}
        return params


class OptimiserParams:
    """
    # Optimiser parameters

    Class for optimiser parameter configuration used in twinLab.

    ## Attributes

    - `num_restarts`: `int`, `optional`. The number of random restarts for optimisation. Default value is `5`.
    - `raw_samples`: `int`,`optional`. The number of samples for initialization. Default value is `128`.
    - `bounds`: `pandas.DataFrame`, `optional`. A `pandas.DataFrame` with exactly two rows and the same number of columns as input dimensions.
        The `pandas.DataFrame` must have two indices: `"lower_bounds"` and `"upper_bounds"`.
        The `"lower_bounds"` row should contain per-dimension lower-bounds for optimisation. The "upper_bounds" row should contain per-dimension upper-bounds for optimisation.
        Lower bounds cannot be larger than the respective upper bounds.
    """

    def __init__(
        self,
        num_restarts: int = 5,
        raw_samples: int = 128,
        bounds: Optional[pd.DataFrame] = None,
    ):
        self.num_restarts = num_restarts
        self.raw_samples = raw_samples
        self.bounds = bounds

    def unpack_parameters(self):
        params = {
            "num_restarts": self.num_restarts,
            "raw_samples": self.raw_samples,
            "bounds": self.bounds,
        }
        return params


class RecommendParams:
    """
    # Emulator.recommend parameters

    Class for Emulator.recommend parameters.

    ## Attributes

    - `seed`: `int`, `optional`. Seed used to initialise the random number generators for reproducibility.
    - `acq_kwargs`: `AcqFuncParams`, `optional`. An `AcqFuncParams` object for customising the `BoTorch` acquisition function.
    - `opt_kwargs`: `OptimiserParams`, `optional`. An `OptimiserParams` object for customising the optimisation routine.
    """

    def __init__(
        self,
        acq_kwargs: AcqFuncParams = AcqFuncParams(),
        opt_kwargs: OptimiserParams = OptimiserParams(),
        seed: Optional[int] = None,
    ):
        self.acq_kwargs = acq_kwargs
        self.opt_kwargs = opt_kwargs
        self.seed = seed

    def unpack_parameters(self):
        params = {
            "acq_kwargs": self.acq_kwargs.unpack_parameters(),
            "opt_kwargs": self.opt_kwargs.unpack_parameters(),
            "kwargs": {"seed": self.seed},
        }
        return params


### ###

### Calibrate ###


class CalibrateParams:
    """
    # Emulator.calibration parameters

    Class for Emulator.calibrate parameters.

    ## Attributes

    - `y_std_model`: Union[`bool`,`pd.DataFrame`], `optional`. Whether to include model noise covariance in the likelihood. If a `pandas.DataFrame` is supplied, it must contain the same columns as `y`.
    - `return_summary`: `bool`, `optional`. If `True`, return summary diagnostics of the inverse solution. If `False`, return the entire solution.
    - `kwargs`: `InverseSolveParams`, `optional`. An `InverseSolveParams` object to configure the underlying inverse solver routine.
    """

    def __init__(
        self,
        y_std_model: bool = False,
        # method: Optional[str] = "TinyDA", # TODO: Commented-out as interacts with "method" of use_model_method
        # prior: Optional[str] = "uniform", # TODO: Commented-out as scipy types
        return_summary: bool = True,
        iterations: int = 10000,
        n_chains: int = 2,
        force_sequential: bool = False,
        seed: Optional[int] = None,
    ):
        self.y_std_model = y_std_model
        # self.method = method
        # self.prior = prior
        self.return_summary = return_summary
        self.iterations = iterations
        self.n_chains = n_chains
        self.force_sequential = force_sequential
        self.seed = seed

    def unpack_parameters(self):
        params = {
            "y_std_model": self.y_std_model,
            # "method": self.method,
            # "prior": self.prior,
            "return_summary": self.return_summary,
            "kwargs": {
                "iterations": self.iterations,
                "n_chains": self.n_chains,
                "force_sequential": self.force_sequential,
                "seed": self.seed,
            },
        }
        return params


### ###


class DesignParams:
    """
    # Emulator.initial_design parameters

    Class for Emulator.get_initial_design parameters.

    ## Attributes

    - `sampling_method`: `SamplingMethods`. The sampling method to use for the initial design. This defaults to latin hypercube sampling.
    - `seed`: `int`, `Optional`. Seed used to initialise the random number generators for reproducibility.
    """

    def __init__(
        self,
        sampling_method: Sampling = LatinHypercube(),
        seed: Optional[int] = None,
    ):
        self.seed = seed
        self.sampling_method = sampling_method
