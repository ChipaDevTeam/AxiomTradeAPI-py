"""
Test websocket compatibility for different websockets library versions.
Tests that the _connect_with_headers method works with both websockets 10.x (extra_headers)
and websockets 13+ (additional_headers).
"""
import asyncio
import unittest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axiomtradeapi.websocket._client import AxiomTradeWebSocketClient


class TestWebSocketCompatibility(unittest.TestCase):
    """Test WebSocket connection compatibility with different websockets versions."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock auth manager
        self.mock_auth_manager = Mock()
        self.mock_auth_manager.ensure_valid_authentication.return_value = True
        
        # Create mock tokens
        mock_tokens = Mock()
        mock_tokens.access_token = "test_access_token"
        mock_tokens.refresh_token = "test_refresh_token"
        self.mock_auth_manager.get_tokens.return_value = mock_tokens
        
        # Create client
        self.client = AxiomTradeWebSocketClient(self.mock_auth_manager)

    def test_connect_with_additional_headers(self):
        """Test that connection works with additional_headers (websockets 13+)."""
        async def run_test():
            mock_ws = AsyncMock()
            
            with patch('axiomtradeapi.websocket._client.websockets.connect', new=AsyncMock(return_value=mock_ws)) as mock_connect:
                # Test the helper method directly
                result = await self.client._connect_with_headers("wss://test.example.com", {"Test": "Header"})
                
                # Verify connect was called with additional_headers
                mock_connect.assert_called_once_with("wss://test.example.com", additional_headers={"Test": "Header"})
                self.assertEqual(result, mock_ws)
        
        asyncio.run(run_test())

    def test_connect_fallback_to_extra_headers(self):
        """Test that connection falls back to extra_headers when additional_headers is not available."""
        async def run_test():
            mock_ws = AsyncMock()
            
            # Mock the client to simulate websockets 10.x (only extra_headers available)
            self.client._uses_additional_headers = False
            self.client._uses_extra_headers = True
            
            async def mock_connect_impl(url, **kwargs):
                # Simulate websockets 10.x behavior: reject additional_headers, accept extra_headers
                if 'additional_headers' in kwargs:
                    raise TypeError("connect() got an unexpected keyword argument 'additional_headers'")
                elif 'extra_headers' in kwargs:
                    return mock_ws
                else:
                    raise ValueError("No headers provided")
            
            with patch('axiomtradeapi.websocket._client.websockets.connect', new=mock_connect_impl):
                # Test the helper method
                result = await self.client._connect_with_headers("wss://test.example.com", {"Test": "Header"})
                
                # Verify we got the mock websocket back (meaning extra_headers worked)
                self.assertEqual(result, mock_ws)
        
        asyncio.run(run_test())

    def test_connect_reraises_other_typeerror(self):
        """Test that other TypeErrors are re-raised."""
        async def run_test():
            with patch('axiomtradeapi.websocket._client.websockets.connect') as mock_connect:
                # Raise a different TypeError that's not about additional_headers
                mock_connect.side_effect = TypeError("Some other error")
                
                # Test the helper method - should raise the TypeError
                with self.assertRaises(TypeError) as context:
                    await self.client._connect_with_headers("wss://test.example.com", {"Test": "Header"})
                
                self.assertIn("Some other error", str(context.exception))
        
        asyncio.run(run_test())

    def test_full_connect_uses_compatibility_method(self):
        """Test that the full connect() method uses the compatibility helper."""
        async def run_test():
            mock_ws = AsyncMock()
            
            with patch.object(self.client, '_connect_with_headers', new=AsyncMock(return_value=mock_ws)) as mock_helper:
                # Call the main connect method
                result = await self.client.connect()
                
                # Verify the helper was called
                mock_helper.assert_called_once()
                self.assertTrue(result)
                self.assertEqual(self.client.ws, mock_ws)
        
        asyncio.run(run_test())

    def test_alternative_url_uses_compatibility_method(self):
        """Test that alternative URL connection also uses the compatibility helper."""
        async def run_test():
            mock_ws = AsyncMock()
            
            # Change the URL to trigger the alternative URL path
            self.client.ws_url = "wss://cluster-usc2.axiom.trade/"
            
            with patch.object(self.client, '_connect_with_headers') as mock_helper:
                # First call fails, second call succeeds
                mock_helper.side_effect = [
                    Exception("Connection failed"),
                    mock_ws
                ]
                
                # Call the main connect method
                result = await self.client.connect()
                
                # Verify the helper was called twice (once for primary, once for alternative)
                self.assertEqual(mock_helper.call_count, 2)
                self.assertTrue(result)
                self.assertEqual(self.client.ws, mock_ws)
        
        asyncio.run(run_test())

    def test_fallback_when_version_not_detected(self):
        """Test that the fallback mechanism works when version detection fails."""
        async def run_test():
            mock_ws = AsyncMock()
            
            # Simulate version detection failure
            self.client._uses_additional_headers = False
            self.client._uses_extra_headers = False
            
            async def mock_connect_impl(url, **kwargs):
                # First call with additional_headers fails, second with extra_headers succeeds
                if 'additional_headers' in kwargs:
                    raise TypeError("connect() got an unexpected keyword argument 'additional_headers'")
                elif 'extra_headers' in kwargs:
                    return mock_ws
                else:
                    raise ValueError("No headers provided")
            
            with patch('axiomtradeapi.websocket._client.websockets.connect', new=mock_connect_impl):
                # Test the helper method
                result = await self.client._connect_with_headers("wss://test.example.com", {"Test": "Header"})
                
                # Verify we got the mock websocket back (meaning fallback to extra_headers worked)
                self.assertEqual(result, mock_ws)
        
        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
