import os
import httpx
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import json

class FinverseClient:
    """Finverse API client for bank data aggregation"""
    
    def __init__(self):
        self.customer_app_id = os.getenv("FINVERSE_CUSTOMER_APP_ID")
        self.client_id = os.getenv("FINVERSE_CLIENT_ID")
        self.client_secret = os.getenv("FINVERSE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("FINVERSE_REDIRECT_URI")
        self.base_url = "https://api.prod.finverse.net"  # Production environment
        self._customer_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        
    def is_configured(self) -> bool:
        """Check if Finverse API credentials are properly configured"""
        return all([self.customer_app_id, self.client_id, self.client_secret, self.redirect_uri])
    
    async def get_customer_token(self) -> str:
        """Get or refresh customer token for API authentication"""
        if self._customer_token and self._token_expires_at and datetime.now() < self._token_expires_at:
            return self._customer_token
            
        if not self.is_configured():
            raise ValueError("Finverse API credentials not configured")
            
        url = f"{self.base_url}/auth/customer/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            response.raise_for_status()
            
            token_data = response.json()
            self._customer_token = token_data["access_token"]
            # Token expires in 60 minutes
            self._token_expires_at = datetime.now() + timedelta(minutes=55)
            
            return self._customer_token
    
    async def create_link_token(self) -> Dict[str, Any]:
        """Create a link token for connecting bank accounts"""
        token = await self.get_customer_token()
        
        url = f"{self.base_url}/link/token/create"
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "customer_app_id": self.customer_app_id,
            "redirect_uri": self.redirect_uri,
            "products": ["accounts", "transactions", "balances"]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    
    async def exchange_public_token(self, public_token: str) -> Dict[str, Any]:
        """Exchange public token from Finverse Link for access token"""
        token = await self.get_customer_token()
        
        url = f"{self.base_url}/link/token/exchange"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"public_token": public_token}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
    
    async def get_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        """Get all bank accounts for a given access token"""
        token = await self.get_customer_token()
        
        url = f"{self.base_url}/data/accounts"
        headers = {
            "Authorization": f"Bearer {token}",
            "Finverse-Account-Access-Token": access_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("accounts", [])
    
    async def get_balances(self, access_token: str) -> List[Dict[str, Any]]:
        """Get balances for all accounts"""
        token = await self.get_customer_token()
        
        url = f"{self.base_url}/data/balances"
        headers = {
            "Authorization": f"Bearer {token}",
            "Finverse-Account-Access-Token": access_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("balances", [])
    
    async def get_transactions(self, access_token: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get transactions for all accounts"""
        token = await self.get_customer_token()
        
        url = f"{self.base_url}/data/transactions"
        headers = {
            "Authorization": f"Bearer {token}",
            "Finverse-Account-Access-Token": access_token
        }
        params = {"days": days}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("transactions", [])
    
    async def get_identity(self, access_token: str) -> Dict[str, Any]:
        """Get identity information for account holder"""
        token = await self.get_customer_token()
        
        url = f"{self.base_url}/data/identity"
        headers = {
            "Authorization": f"Bearer {token}",
            "Finverse-Account-Access-Token": access_token
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

# Global Finverse client instance
finverse_client = FinverseClient()
