# Standard imports
from pprint import pprint
from typing import Dict, List
import os

# Third-party imports
from typeguard import typechecked

# Project imports
from . import api
from . import utils


@typechecked
def set_api_key(api_key: str, verbose: bool = False) -> None:
    """
    # Set API key

    Set the user API key for their `twinLab` cloud account.

    ## Arguments:

    - `api_key`: `str`. API key for the `twinLab` cloud.
    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.

    ## Example:

    ```python
    import twinlab as tl

    tl.set_api_key("12345")
    ```
    """
    os.environ["TWINLAB_API_KEY"] = api_key
    if verbose:
        print("API key: {}".format(api_key))


@typechecked
def set_server_url(url: str, verbose: bool = False) -> None:
    """
    # Set server URL

    Set the URL from which `twinLab` is being served from.

    ## Arguments:

    - `url`: `str`. URL for the `twinLab` cloud.
    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.

    ## Example:

    ```python
    import twinlab as tl

    tl.set_server_url("https://twinlab.digilab.co.uk")
    ```
    """
    os.environ["TWINLAB_URL"] = url
    if verbose:
        print("Server URL: {}".format(url))


@typechecked
def get_server_url(verbose: bool = False) -> str:
    """
    # Get the server URL

    Fetch the URL from which `twinLab` is being served from.

    ## Arguments:

    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.

    ## Returns:

    - `str` containing the server URL.

    ## Example:

    ```python
    import twinlab as tl

    tl.get_server_url()
    ```
    """
    server_url = os.getenv("TWINLAB_URL")
    if verbose:
        print("Server URL: {}".format(server_url))
    return server_url


@typechecked
def get_api_key(verbose: bool = False) -> str:
    """
    # Get the user API key

    Get a user API key for their`twinLab` cloud account.

    ## Arguments:

    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.

    ## Returns:

    - `str` containing the server API key.

    ## Example:

    ```python
    import twinlab as tl

    tl.get_api_key()
    ```
    """
    api_key = os.getenv("TWINLAB_API_KEY")
    if verbose:
        print("API key: {}".format(api_key))
    return api_key


@typechecked
def user_information(verbose: bool = False, debug: bool = False) -> Dict:
    """
    # User information

    Get information about the user.

    ## Arguments:

    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
    - `debug`: `bool`, `optional`. Determining level of information logged on the server.

    ## Returns:

    - `dict` containing user information.

    ## Example:

    ```python
    import twinlab as tl

    user_info = tl.user_information()
    print(user_info)
    ```
    """
    status, response = api.get_user(verbose=debug)
    if utils.is_not_success_status(status):
        raise Exception(f"Error: {utils.get_message(response)}")
    user_info = response
    if verbose:
        print("User information:")
        pprint(user_info, compact=True, sort_dicts=False)
    return user_info


@typechecked
def versions(verbose: bool = False, debug: bool = False) -> Dict[str, str]:
    """
    # twinLab versions

    Get information about the twinLab version being used.

    ## Arguments:

    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
    - `debug`: `bool`, `optional`. Determining level of information logged on the server.

    ## Returns:

    - `dict` containing version information.

    ## Example:

    ```python
    import twinlab as tl

    version_info = tl.versions()
    print(version_info)
    ```
    """
    status, response = api.get_versions(verbose=debug)
    if utils.is_not_success_status(status):
        raise Exception(f"Error: {utils.get_message(response)}")
    version_info = response
    if verbose:
        print("Version information:")
        pprint(version_info, compact=True, sort_dicts=False)
    return version_info


@typechecked
def list_datasets(verbose: bool = False, debug: bool = False) -> List[str]:
    """
    # List datasets

    List datasets that have been uploaded to the user's `twinLab` cloud account.

    ## Arguments:

    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
    - `debug`: `bool`, `optional`. Determining level of information logged on the server.

    ## Returns:

    - `list` of `str` dataset IDs.

    ## Example:

    ```python
    import pandas as pd
    import twinlab as tl

    datasets = tl.list_datasets()
    print(datasets)
    ```
    """
    status, response = api.list_datasets(verbose=debug)
    if utils.is_not_success_status(status):
        raise Exception(f"Error: {utils.get_message(response)}")
    datasets = utils.get_value_from_body("datasets", response)
    if verbose:
        print("Datasets:")
        pprint(datasets, compact=True, sort_dicts=False)
    return datasets


@typechecked
def list_emulators(verbose: bool = False, debug: bool = False) -> List[str]:
    """
    # List emulators

    List emulators that have been set up in the user's `twinLab` cloud account.

    ## Arguments:

    - `verbose`: `bool`, `optional`. Determining level of information returned to the user.
    - `debug`: `bool`, `optional`. Determining level of information logged on the server.

    ## Returns:

    - A `list` of `str` campaign IDs.

    ## Example:

    ```python
    import twinlab as tl

    emulators = tl.list_emulators()
    print(emulators)
    ```
    """
    status, response = api.list_models(verbose=debug)
    if utils.is_not_success_status(status):
        raise Exception(f"Error: {utils.get_message(response)}")
    campaigns = utils.get_value_from_body("models", response)
    if verbose:
        print("Trained models:")
        pprint(campaigns, compact=True, sort_dicts=False)
    return campaigns
