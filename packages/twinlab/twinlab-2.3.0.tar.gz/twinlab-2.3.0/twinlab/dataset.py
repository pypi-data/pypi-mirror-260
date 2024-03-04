# Standard imports
import io
from typing import List

# Third-party imports
import pandas as pd
from typeguard import typechecked

# Project imports
from . import api
from . import settings
from . import utils


class Dataset:
    """
    # Datasets for twinLab

    A twinLab dataset that can be used for training an emulator online.

    ## Arguments:
    - `id`: `str`. Name of the dataset.
    """

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return f"Dataset ID: {self.id}"

    @typechecked
    def upload(
        self,
        df: pd.DataFrame,
        use_upload_url: bool = True,
        verbose: bool = False,
        debug: bool = False,
    ) -> None:
        """
        # Upload

        Upload a dataset to the user's `twinLab` cloud account so that it can be queried and used for training.

        ## Arguments:

        - `df`: `pandas.DataFrame`. A `pandas.DataFrame` containing the desired dataset.
        - `use_upload_url`: `bool`, `optional`. Determining whether to upload via a pre-signed url or directly to the server.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.

        ## Examples:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        ```
        """

        # Upload the file (either via link or directly)
        if use_upload_url:
            _, response = api.generate_upload_url(self.id, verbose=debug)
            upload_url = utils.get_value_from_body("url", response)
            utils.upload_dataframe_to_presigned_url(
                df,
                upload_url,
                verbose=verbose,
                check=settings.CHECK_DATASETS,
            )
            if verbose:
                print("Processing dataset")
            _, response = api.process_uploaded_dataset(self.id, verbose=debug)

        else:
            csv_string = utils.get_csv_string(df)
            _, response = api.upload_dataset(self.id, csv_string, verbose=debug)
        if verbose:
            message = utils.get_message(response)
            print(message)

    @typechecked
    def _analyse_variance(
        self,
        columns: List[str],
        verbose: bool = False,
        debug: bool = False,
    ) -> pd.DataFrame:
        columns_string = ",".join(columns)
        _, response = api.analyse_dataset(
            self.id, columns=columns_string, verbose=debug
        )

        csv_string = utils.get_value_from_body("dataframe", response)
        csv_string = io.StringIO(csv_string)
        df = pd.read_csv(csv_string, index_col=0, sep=",")
        if verbose:
            print("Variance Analysis:")
            print(df)
        return df

    @typechecked
    def analyse_input_variance(
        self,
        columns: List[str],
        verbose: bool = False,
        debug: bool = False,
    ) -> pd.DataFrame:
        """
        # Analyse_input

        A method that returns a dataframe showing the cumulative variance retained per number of dimmensions after aplying SVD.

        ## Arguments:

        - `columns`: `List[str]` List of input colums to evaluate.
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.

        ## Examples:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3], 'y': [1, 4, 9],'z': [1, 8, 27]})
        dataset = tl.Dataset("my_dataset")
        dataset.analyse_input_variance([x,y])
        ```
        """
        df = self._analyse_variance(columns=columns, verbose=verbose, debug=debug)
        return df

    @typechecked
    def analyse_output_variance(
        self,
        columns: List[str],
        verbose: bool = False,
        debug: bool = False,
    ) -> pd.DataFrame:
        """
        # Analyse_output

        A method that returns a dataframe showing the cumulative variance retained per number of dimmensions after aplying SVD.

        ## Arguments:

        - `columns`: `List[str]` List of output colums to evaluate
        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.

        ## Examples:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3], 'y': [1, 4, 9],'z': [1, 8, 27]})
        dataset = tl.Dataset("my_dataset")
        dataset.analyse_output_variance([x,y])
        ```
        """
        df = self._analyse_variance(columns=columns, verbose=verbose, debug=debug)
        return df

    # TODO: This should possibly be called 'download' instead of 'view'
    @typechecked
    def view(self, verbose: bool = False, debug: bool = False) -> pd.DataFrame:
        """
        # View datasets

        View a dataset that exists on the user's twinLab cloud account.

        ## Arguments:

        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.

        ## Returns:

        - `pandas.DataFrame` of the dataset.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        df = dataset.view()
        print(df)
        ```
        """
        _, response = api.view_dataset(self.id, verbose=debug)

        csv_string = utils.get_value_from_body("dataset", response)
        csv_string = io.StringIO(csv_string)
        df = pd.read_csv(csv_string, sep=",")
        if verbose:
            print("Dataset:")
            print(df)
        return df

    @typechecked
    def summarise(self, verbose: bool = False, debug: bool = False) -> pd.DataFrame:
        """
        # Summarise datasets

        Summarise a dataset that exists on the user's `twinLab` cloud account by printing summary statistics.

        ## Arguments:

        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.

        ## Returns:

        - `pandas.DataFrame` containing summary statistics for the dataset.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        df_summary = dataset.summarise()
        print(df_summary)
        ```
        """
        _, response = api.summarise_dataset(self.id, verbose=debug)

        csv_string = utils.get_value_from_body("dataset_summary", response)
        csv_string = io.StringIO(csv_string)
        df = pd.read_csv(csv_string, index_col=0, sep=",")
        if verbose:
            print("Dataset summary:")
            print(df)
        return df

    @typechecked
    def delete(self, verbose: bool = False, debug: bool = False) -> None:
        """
        # Delete datasets

        Delete a dataset from the user's `twinLab` cloud account.

        ## Arguments:

        - `verbose`: `bool`, `optional`. Determining level of information returned to the user. Default is False.
        - `debug`: `bool`, `optional`. Determining level of information logged on the server. Default is False.

        ## Example:

        ```python
        import pandas as pd
        import twinlab as tl

        df = pd.DataFrame({'X': [1, 2, 3, 4], 'y': [1, 4, 9, 16]})
        dataset = tl.Dataset("my_dataset")
        dataset.upload(df)
        dataset.delete()
        ```
        """
        _, response = api.delete_dataset(self.id, verbose=debug)

        if verbose:
            message = utils.get_message(response)
            print(message)
