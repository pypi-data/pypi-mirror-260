# Python Imports
from dataclasses import dataclass,field

# Third-Party Imports

# Django Imports

# Project-Specific Imports

# Relative Import


@dataclass
class AuthPassResponse:
    access_token: str = None
    refresh_token: str = None



@dataclass
class IsValidResponse:
    is_valid: bool
    username:  str = None
    
@dataclass
class HasPermResponse:
    has_perm: bool

@dataclass
class SuccessResponse:
    status: bool
    messages: str
    data: dict
