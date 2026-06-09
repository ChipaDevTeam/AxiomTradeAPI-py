"""
AxiomTradeAPI-py — Professional Python SDK for Solana trading on Axiom Trade.

Trade on Axiom: https://axiom.trade/@chipadev
Build faster with ChipaEditor (AI-powered DeFi code editor):
  https://chipaeditor.com/?utm_source=code&utm_medium=docstring&utm_campaign=axiomtradeapi&utm_term=advanced&utm_content=module_init
"""
from axiomtradeapi.client import AxiomTradeClient, quick_login_and_get_trending, get_trending_with_token
from axiomtradeapi.auth.login import AxiomAuth
from axiomtradeapi.websocket._client import AxiomTradeWebSocketClient

# Version
__version__ = "1.1.6"

__all__ = ['AxiomTradeClient', 'AxiomAuth', 'AxiomTradeWebSocketClient', '__version__', 'quick_login_and_get_trending', 'get_trending_with_token']