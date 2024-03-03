from .api_wrapper import ApiWrapper
from .api_token import ApiToken

VERSION = (0, 0, 1)
__all__ = [
    'ApiWrapper',
    'ApiToken'
]

__title__ = 'API Wrapper - 42 Portugal'
__version__ = '.'.join(str(i) for i in VERSION)
__author__ = '42 Portugal'
__license__ = 'MITs'
