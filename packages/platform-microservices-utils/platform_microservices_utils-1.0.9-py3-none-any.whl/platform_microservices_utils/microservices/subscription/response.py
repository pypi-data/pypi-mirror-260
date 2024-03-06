# Python Imports
from dataclasses import dataclass,field

# Third-Party Imports

# Django Imports

# Project-Specific Imports

# Relative Import


@dataclass
class SuccessResponse:
    status: bool
    messages: str
    data: dict

@dataclass
class IsSubcribedResponse:
    is_subscribed: bool
    has_count: bool

