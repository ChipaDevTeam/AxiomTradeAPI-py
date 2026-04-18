"""
Multi-Account Manager for Axiom Trade API
Run tasks across multiple accounts with proxy support
"""

import asyncio
import logging
from typing import List, Dict, Callable, Optional, Union
from ..client import AxiomTradeClient
from .proxy_manager import ProxyManager

class MultiAccountManager:
    """Manages multiple AxiomTradeClient instances with proxies"""
    
    def __init__(self, use_proxies: bool = True):
        self.clients: List[Dict] = []  # List of {'client': client, 'id': int, 'proxy': dict}
        self.proxy_manager = ProxyManager()
        self.use_proxies = use_proxies
        self.logger = logging.getLogger(__name__)

    async def initialize_proxies(self, count: int):
        """Pre-fetch enough proxies"""
        if self.use_proxies:
            self.logger.info(f"Fetching proxies for {count} accounts...")
            self.proxy_manager.fetch_free_proxies(limit=count + 10)  # Fetch a few extra

    def add_account(self, username: str = None, password: str = None, 
                    auth_token: str = None, refresh_token: str = None):
        """Add an account to the pool"""
        proxies = None
        if self.use_proxies:
            proxies = self.proxy_manager.get_proxy()
            if not proxies:
                self.logger.warning("No proxies available, using direct connection")
        
        client = AxiomTradeClient(
            username=username,
            password=password,
            auth_token=auth_token,
            refresh_token=refresh_token,
            proxies=proxies,
            use_saved_tokens=False # Don't conflict with saved file
        )
        
        account_id = len(self.clients) + 1
        self.clients.append({
            'client': client,
            'id': account_id,
            'proxy': proxies
        })
        self.logger.info(f"Added account #{account_id} with proxy: {proxies}")
        return client

    def load_accounts_from_file(self, filepath: str):
        """Load accounts from file (format: email:password per line)"""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            # Pre-fetch proxies
            if self.use_proxies and not self.proxy_manager.proxies:
                self.proxy_manager.fetch_free_proxies(len(lines))
                
            for line in lines:
                line = line.strip()
                if ':' in line:
                    email, password = line.split(':', 1)
                    self.add_account(username=email, password=password)
        except Exception as e:
            self.logger.error(f"Failed to load accounts: {e}")

    async def run_active_users_monitor(self, duration: int = None, callback: Callable = None):
        """
        Run get_active_axiom_users on all accounts simultaneously
        """
        if not self.clients:
            self.logger.warning("No accounts configured")
            return

        tasks = []
        
        async def _make_callback(account_id):
            """Factory to create a specific callback for an account"""
            async def _inner_callback(count: int):
                if callback:
                    # Determine if callback accepts 1 or 2 args
                    # But easiest is to just pass a string or modify what we pass
                    # If callback expects (count, id), we pass that.
                    # But client expects callback(count). 
                    # So we call user's callback with extra info.
                    try:
                        await callback(count, account_id) 
                    except TypeError:
                        await callback(count) # Fallback to just count
                else:
                    print(f"[Account #{account_id}] Active Users: {count}")
            return _inner_callback

        self.logger.info(f"Starting monitor on {len(self.clients)} accounts...")
        
        for account_data in self.clients:
            client: AxiomTradeClient = account_data['client']
            account_id = account_data['id']
            
            # Check login first (if needed, this might block, but client login is sync usually unless purely token based)
            # If username/pass provided, client might need login() call if not doing it in init?
            # AxiomTradeClient init sets up AuthManager, but doesn't auto-login unless use_saved_tokens works/finds something.
            # But we set use_saved_tokens=False.
            # So we should probably call login() in a wrapper task.
            
            task_callback = await _make_callback(account_id)
            
            tasks.append(self._run_single_client_monitor(client, task_callback, duration))
            
        await asyncio.gather(*tasks)

    async def _run_single_client_monitor(self, client: AxiomTradeClient, callback, duration):
        try:
            # Login if needed
            if not client.is_authenticated():
                if client.auth_manager.username and client.auth_manager.password:
                    client.login() # This is sync in current client?
                else:
                    self.logger.warning("Client not authenticated and no credentials provided")
                    return

            await client.get_active_axiom_users(callback=callback, duration=duration)
        except Exception as e:
            self.logger.error(f"Error in client task: {e}")

