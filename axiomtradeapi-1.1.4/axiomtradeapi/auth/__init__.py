"""
Authentication module for Axiom Trade API
Handles automatic token management and cookie handling
"""

from .auth_manager import AuthManager, CookieManager

__all__ = ['AuthManager', 'CookieManager']
