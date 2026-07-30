from enum import Enum
class HTTPMethod(str, Enum):
    """Supported HTTP methods."""
    
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"