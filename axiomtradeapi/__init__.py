from axiomtradeapi.client import AxiomTradeClient, quick_login_and_get_trending, get_trending_with_token
from axiomtradeapi.auth.login import AxiomAuth

# Version
__version__ = "1.0.3"

__all__ = ['AxiomTradeClient', 'AxiomAuth', '__version__', 'quick_login_and_get_trending', 'get_trending_with_token']