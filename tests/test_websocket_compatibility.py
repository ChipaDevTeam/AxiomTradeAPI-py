"""
Test WebSocket client compatibility with v1.1.5 curl_cffi architecture.

In v1.1.5 the WebSocket client was rewritten to use curl_cffi with
impersonate="chrome136" to bypass Cloudflare TLS fingerprinting.
The old _connect_with_headers / self.ws interface was removed;
the live connection object is stored in self._curl_ws and callbacks
are stored in self._callbacks.
"""
import asyncio
import unittest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axiomtradeapi.websocket._client import AxiomTradeWebSocketClient


def _make_mock_auth_manager(access_token="test_access_token", refresh_token="test_refresh_token"):
    mock_auth = Mock()
    mock_auth.ensure_valid_authentication.return_value = True
    mock_tokens = Mock()
    mock_tokens.access_token = access_token
    mock_tokens.refresh_token = refresh_token
    mock_auth.get_tokens.return_value = mock_tokens
    mock_auth.tokens = mock_tokens
    return mock_auth


class TestWebSocketClientCreation(unittest.TestCase):
    """Client creation and interface smoke tests."""

    def setUp(self):
        self.mock_auth = _make_mock_auth_manager()
        self.client = AxiomTradeWebSocketClient(self.mock_auth)

    def test_client_has_required_methods(self):
        self.assertTrue(hasattr(self.client, 'subscribe_new_tokens'))
        self.assertTrue(hasattr(self.client, 'subscribe_wallet_transactions'))
        self.assertTrue(hasattr(self.client, 'start'))
        self.assertTrue(hasattr(self.client, 'close'))

    def test_curl_ws_starts_as_none(self):
        self.assertIsNone(self.client._curl_ws)

    def test_callbacks_dict_exists(self):
        self.assertIsInstance(self.client._callbacks, dict)

    def test_no_legacy_connect_with_headers(self):
        """_connect_with_headers was removed in v1.1.5 — _connect_curl is the primary path."""
        self.assertFalse(hasattr(self.client, '_connect_with_headers'))
        self.assertTrue(hasattr(self.client, '_connect_curl'))


class TestWebSocketCurlCffiConnection(unittest.TestCase):
    """Test that _connect_curl stores the WebSocket in _curl_ws."""

    def setUp(self):
        self.mock_auth = _make_mock_auth_manager()
        self.client = AxiomTradeWebSocketClient(self.mock_auth)

    def test_connect_curl_stores_ws(self):
        async def run():
            mock_ws = AsyncMock()
            mock_ws.recv = AsyncMock(return_value=(b'{"type":"ping"}', None))

            mock_ctx = MagicMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_ws)
            mock_ctx.__aexit__ = AsyncMock(return_value=False)

            mock_session = MagicMock()
            mock_session.get = AsyncMock(return_value=MagicMock(status_code=200))
            mock_session.ws_connect = Mock(return_value=mock_ctx)
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=False)

            mock_tokens = Mock()
            mock_tokens.access_token = "tok"
            mock_tokens.refresh_token = "ref"

            with patch('axiomtradeapi.websocket._client.CurlAsyncSession',
                       return_value=mock_session):
                connected = await self.client._connect_curl(mock_tokens, [self.client.ws_url])

            self.assertTrue(connected)
            self.assertIs(self.client._curl_ws, mock_ws)

        asyncio.run(run())

    def test_connect_curl_tries_fallback_urls(self):
        """On failure of first URL, _connect_curl should try the next."""
        async def run():
            mock_ws = AsyncMock()
            mock_ctx = MagicMock()
            mock_ctx.__aenter__ = AsyncMock(return_value=mock_ws)
            mock_ctx.__aexit__ = AsyncMock(return_value=False)

            call_count = {"n": 0}

            def mock_ws_connect(url, **kwargs):
                call_count["n"] += 1
                if call_count["n"] == 1:
                    raise Exception("First URL failed")
                return mock_ctx

            mock_session = MagicMock()
            mock_session.get = AsyncMock(return_value=MagicMock(status_code=200))
            mock_session.ws_connect = mock_ws_connect
            mock_session.__aenter__ = AsyncMock(return_value=mock_session)
            mock_session.__aexit__ = AsyncMock(return_value=False)

            mock_tokens = Mock()
            mock_tokens.access_token = "tok"
            mock_tokens.refresh_token = "ref"

            with patch('axiomtradeapi.websocket._client.CurlAsyncSession',
                       return_value=mock_session):
                urls = [self.client.ws_url, "wss://cluster3.axiom.trade/"]
                connected = await self.client._connect_curl(mock_tokens, urls)

            self.assertTrue(connected)
            self.assertEqual(call_count["n"], 2)

        asyncio.run(run())


class TestWebSocketSubscribeCallbacks(unittest.TestCase):
    """Test that subscribe methods register callbacks in _callbacks."""

    def setUp(self):
        self.mock_auth = _make_mock_auth_manager()
        self.client = AxiomTradeWebSocketClient(self.mock_auth)

    def test_subscribe_new_tokens_registers_callback(self):
        """subscribe_new_tokens stores callback under 'new_pairs' key."""
        async def my_callback(tokens):
            pass

        async def run():
            # Patch _ensure_connected so no real network call is made
            with patch.object(self.client, '_ensure_connected', new=AsyncMock(return_value=True)):
                with patch.object(self.client, '_send', new=AsyncMock()):
                    await self.client.subscribe_new_tokens(my_callback)

        asyncio.run(run())
        self.assertIs(self.client._callbacks.get('new_pairs'), my_callback)

    def test_subscribe_wallet_transactions_registers_callback(self):
        async def my_callback(data):
            pass

        wallet = "BJBgjyDZx5FSsyJf6bFKVXuJV7DZY9PCSMSi5d9tcEVh"

        async def run():
            with patch.object(self.client, '_ensure_connected', new=AsyncMock(return_value=True)):
                with patch.object(self.client, '_send', new=AsyncMock()):
                    await self.client.subscribe_wallet_transactions(wallet, my_callback)

        asyncio.run(run())
        expected_key = f"wallet_transactions_{wallet}"
        self.assertIs(self.client._callbacks.get(expected_key), my_callback)


if __name__ == '__main__':
    unittest.main()
