from enum import Enum

class Errors(Enum):
    OVER_QUERY_LIMIT = 1
    REQUEST_DENIED = 2
    INVALID_REQUEST = 3
    ZERO_RESULTS = 4
    UNAVAILABLE = 5
    UNKNOWN = 6
