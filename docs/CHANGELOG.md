# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-09-03

### Added
- **Automatic Token Refresh System**: Secure token storage with encryption and automatic refresh
- **8 New API Functions**: Comprehensive meme token analytics and trading data
  - `get_token_info_by_pair()` - Token holder stats, bot detection, insider analysis
  - `get_last_transaction()` - Latest transaction data with prices and volumes
  - `get_pair_info()` - Comprehensive token pair details (name, ticker, socials)
  - `get_pair_stats()` - Pair statistics and metrics
  - `get_meme_open_positions()` - User's current meme token holdings
  - `get_holder_data()` - Deep token holder analysis
  - `get_dev_tokens()` - All tokens created by a developer
  - `get_token_analysis()` - Risk analysis for tokens and developers
- **Enhanced Authentication**: Secure token storage using Fernet encryption
- **Direct RPC Transaction Sending**: Send transactions directly to Solana RPC endpoints
- **Comprehensive Error Handling**: Better error messages and debugging support
- **Production-Ready Status**: Upgraded from Beta to Production/Stable

### Changed
- **Updated Base URLs**: Fixed API endpoints to use correct `api10.axiom.trade` URLs
- **Enhanced Security**: All tokens now encrypted at rest
- **Improved Documentation**: Comprehensive examples and usage guides
- **Better Testing**: Added test scripts for all functionality

### Dependencies
- Added `cryptography>=3.4.8` for secure token encryption
- Updated package metadata for better PyPI presentation

### Fixed
- **Trading Endpoints**: Corrected non-existent API endpoints
- **Authentication Flow**: Fixed token refresh mechanism
- **Error Handling**: Better handling of API failures and network issues

## [0.2.0] - Previous Release

### Added
- Basic AxiomTrade API integration
- WebSocket support
- Telegram bot integration
- Token-based authentication
- Basic trading functionality

### Features
- Get trending tokens
- Portfolio management
- Basic balance checking
- WebSocket real-time data

---

## Migration Guide from v0.2.0 to v1.0.3

### New Installation
```bash
pip install axiomtradeapi==1.0.3
```

### Updated Usage
```python
from axiomtradeapi.client import AxiomTradeClient

# Enhanced client with automatic authentication
client = AxiomTradeClient(
    auth_token="your_token",
    refresh_token="your_refresh_token"
)

# New analytics functions
token_info = client.get_token_info_by_pair("PAIR_ADDRESS")
positions = client.get_meme_open_positions("WALLET_ADDRESS")
```

### Breaking Changes
- Trading endpoints now require manual transaction building (see documentation)
- Some API endpoints changed from `api6.axiom.trade` to `api10.axiom.trade`

### New Features Available
- Automatic token refresh and secure storage
- 8 new analytics functions for comprehensive meme token analysis
- Enhanced error handling and logging
- Direct RPC transaction capabilities
