from typeguard import typechecked
import json


@typechecked
class Prior:
    """
    # Prior

    A class representing a prior probability distribution

    ## Attributes

    - `name`: `str`, This is the name given to the prior.
    - `distribution`: `Distribution`, Specifies the type of distribution.
    """

    def __init__(self, name, distribution):
        self.name = name
        self.distribution = distribution

    def to_json(self):
        return json.dumps(
            {"name": self.name, "distribution": self.distribution.to_json()}
        )
