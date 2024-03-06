"""Code related to the representation of processing results."""
import time
from dataclasses import dataclass
from enum import Enum
from json import JSONEncoder
from typing import List, Union
from uuid import UUID

from requests import Response

from piscada_cloud.data import write_value
from piscada_cloud.mappings import Tag


class SeverityLevel(Enum):
    """
    The severity level of an Observation.

    Following value conventions of Python logging.
    """

    INFO = 20
    WARNING = 30
    ERROR = 40


class RatingAspect(Enum):
    """The aspect described by a Rating."""

    ENERGY = 1
    COMFORT = 2
    OPERATION = 3


class ObservedValuesType(Enum):
    """
    The relationship between observed values.

    `object` : the observed values represent different aspects of the same object.
    `list` : the observed values represent a semantically similar value across objects.
    `series` : the observed values represent semantically identical values in order or at different points in time. (use the optional `timestamp` field)
    """

    OBJECT = 10
    LIST = 20
    SERIES = 30


@dataclass
class Rating:
    """Describing the impact an Observation has in relation to an aspect."""

    aspect: RatingAspect
    value: float

    def __post_init__(self):
        """Validate that the value is in the range [0.0 .. 1.0] (both inclusive)."""
        if self.value < 0 or self.value > 1:
            raise ValueError(f"The value of the rating must be in the range [0.0 .. 1.0] but is '{self.value}'.")


@dataclass
class Value:
    """
    An observed Value with an identifying name, type, unit, and value.

    Unit strings follow the UCUM standard [https://ucum.org/].
    Timestamp strings follow the ISO 8601 format [https://en.wikipedia.org/wiki/ISO_8601].
    """

    name: str
    type: str
    unit: str
    value: Union[int, float, str]
    timestamp: Union[str, None] = None


@dataclass
class Observation:  # pylint: disable=R0902  # cannot avoid having more than 7 instance attributes
    """
    An observation describing the context and aim of an algorithm.

    The time-scope is expressed as an ISO 8601 Duration such as 'P3DT7H' for 3 days and 7 hours and is back in time relative to the timestamp.
    """

    mapping_id: UUID
    mapping_table_id: UUID
    title: str
    description: str
    cause: str
    consequence: str
    time_scope: str
    source: str
    level: SeverityLevel = SeverityLevel.INFO


@dataclass
class Result:
    """Collecting related observation description, ratings, and observed values."""

    observation: Observation
    ratings: List[Rating]
    observed_values: List[Value]
    observed_values_type: ObservedValuesType = ObservedValuesType.OBJECT


class ResultsEncoder(JSONEncoder):
    """Serialise Results as JSON."""

    def default(self, o):
        """Serialize result types, forwards to the parent implementation for all else.

        Parameters
        ----------
        o : Any
            The object to serialise.

        Returns
        -------
        Any
            The object transformed to a type which is serializeable by the parent implementation.
        """
        if isinstance(o, Result):
            result_dict = o.__dict__
            result_dict.update({"ratings": {rating.aspect.name.lower(): rating.value for rating in o.ratings}})
            result_dict["observed_values_type"] = result_dict["observed_values_type"].name.lower()
            return result_dict
        if isinstance(o, Observation):
            result_dict = o.__dict__
            result_dict["level"] = o.__dict__["level"].name.upper()
            return result_dict
        if isinstance(o, Value):
            return o.__dict__
        if isinstance(o, UUID):
            return str(o)
        return JSONEncoder.default(self, o)


def write_result(tag: Tag, result: Result, timestamp: int = int(time.time() * 1000), host: Union[str, None] = None, token: Union[str, None] = None) -> Response:
    """Write the given result to the cloud.

    Parameters
    ----------
    tag : Tag
        The Tag (controller-id and tag-name) to write to.
    result : Result
        The Result to write.
    timestamp : int, optional
        The current timestamp in milliseconds since epoch, by default int(time.time() * 1000)
    host: str, optional
        Endpoint to send post request. Overrides the default, which is os.environ['WRITEAPI_HOST'].
    token: str, optional
        Access token accosiated with the host. Overrides the default, which is os.environ['WRITEAPI_TOKEN'].

    Returns
    -------
    Response
        The requests Response for the write request.
    """
    return write_value(tag=tag, value=ResultsEncoder(ensure_ascii=False).encode(result), timestamp=timestamp, host=host, token=token)
