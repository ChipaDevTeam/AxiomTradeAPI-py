"""
Proxy Manager tool for Axiom Trade API
Fetches free proxies from various sources
"""

import requests
import re
import random
import logging
from typing import List, Dict, Optional

class ProxyManager:
    """Manages fetching and validating proxies"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.proxies = []
        
    def fetch_free_proxies(self, limit: int = 100) -> List[Dict[str, str]]:
        """
        Fetch free proxies from public sources.
        Returns a list of proxy dicts suitable for requests/AxiomTradeClient.
        """
        self.proxies = []
        
        # Source 1: sslproxies.org
        try:
            self._fetch_from_sslproxies()
        except Exception as e:
            self.logger.warning(f"Failed to fetch from sslproxies: {e}")
            
        # Source 2: free-proxy-list.net
        try:
            self._fetch_from_freeproxylist()
        except Exception as e:
            self.logger.warning(f"Failed to fetch from freeproxylist: {e}")

        # Mix them up
        random.shuffle(self.proxies)
        
        return self.proxies[:limit]

    def _fetch_from_sslproxies(self):
        """Scrape sslproxies.org"""
        url = "https://www.sslproxies.org/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # Simple regex to find IPs and ports
            # Format usually: <tr><td>IP</td><td>Port</td>...
            matches = re.findall(r'<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>', response.text)
            for ip, port in matches:
                proxy_url = f"http://{ip}:{port}"
                self.proxies.append({
                    'http': proxy_url,
                    'https': proxy_url
                })
                
    def _fetch_from_freeproxylist(self):
        """Scrape free-proxy-list.net"""
        url = "https://free-proxy-list.net/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            matches = re.findall(r'<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>', response.text)
            for ip, port in matches:
                proxy_url = f"http://{ip}:{port}"
                self.proxies.append({
                    'http': proxy_url,
                    'https': proxy_url
                })

    def get_proxy(self) -> Optional[Dict[str, str]]:
        """Get a single random proxy"""
        if not self.proxies:
            self.fetch_free_proxies()
        
        if self.proxies:
            return random.choice(self.proxies)
        return None

def get_proxy_manager():
    return ProxyManager()
