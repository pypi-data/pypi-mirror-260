import json
from pprint import pprint

import pandas as pd
from typeguard import typechecked


@typechecked
def load_dataset(filepath: str, verbose: bool = False) -> pd.DataFrame:
    """
    # Load dataset

    Load a dataset from a local file.

    ## Arguments:

    - filepath: `str`. Path to the dataset file
    - verbose: `bool`, `optional`. Determining level of information returned to the user. Default is False.
    """
    df = pd.read_csv(filepath)
    if verbose:
        print("Dataset loaded:")
        print(df)
    return df


def load_params(filepath: str, verbose: bool = False) -> dict:
    """
    # Load dataset

    Load a dataset from a local file.

    ## Arguments:

    - filepath: `str`. Path to the dataset file
    - verbose: `bool`, `optional`. Determining level of information returned to the user. Default is False.
    """

    with open(filepath) as f:
        params = json.load(f)
    if verbose:
        print("Parameters loaded from file:")
        pprint(params)
    return params


def get_sample(df: pd.DataFrame, key: int) -> pd.DataFrame:
    """
    # Get samples

    Retrieves individual samples from the dataframe containing multiple sample functions
    from the posterior distribution of the trained GP in twinLab

    ## Arguments:

    - df: `pd.DataFrame`: Output dataframe from the sample method
    - key: `int`: Specifies the n-th sample to be taken from the entire set of samples
    """
    key_str = str(key)
    sample_df = df.xs(key=key_str, level=-1, axis="columns")
    return sample_df


def join_samples(
    df_one: pd.DataFrame,
    df_two: pd.DataFrame,
) -> pd.DataFrame:
    """
    # Join samples

    Joins two dataframes that contain sample functions from the posterior distribution of the trained GP in twinLab
    together to form a single dataframe

    ## Arguments:

    - df_one: `pd.DataFrame`: First Dataframe
    - df_two: `pd.DataFrame`: Second Dataframe
    """
    # Get the number of samples in each dataframe and find the maximum
    n_samples_df_one, n_samples_df_two = len(df_one.columns), len(df_two.columns)
    n_samples = int(max(n_samples_df_one / 2, n_samples_df_two / 2))

    # If the first dataframe has more samples than the second, swap them
    if n_samples_df_one > n_samples_df_two:
        df_one, df_two = df_two, df_one

    # Convert the larger dataframe to a dictionary
    df_dict = df_two.to_dict()
    new_dict, new_keys = {}, {}

    # Form the new dictionary with updated indices
    for key in df_dict.keys():
        _key = (key[0], str(int(key[1]) + n_samples))
        new_keys[key] = _key
    for key in new_keys:
        new_dict[new_keys[key]] = df_dict[key]

    # Convert the new dictionary to a dataframe
    new_df = pd.DataFrame(new_dict)
    final_df = pd.concat((df_one, new_df), axis="columns")
    sorted_df = final_df.sort_index(axis="columns")
    return sorted_df
