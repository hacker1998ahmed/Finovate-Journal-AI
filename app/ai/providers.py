# Finovate Journal AI - AI Provider Abstraction Layer

"""
AI Provider abstraction for Finovate Journal AI.
Supports multiple providers: OpenAI, Ollama, LM Studio, etc.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers."""
    
    @abstractmethod
    def analyze_transaction(self, text: str) -> Optional[Dict[str, Any]]:
        """Analyze a transaction text and return structured data."""
        pass
    
    @abstractmethod
    def explain_entry(self, entry_data: Dict[str, Any]) -> Optional[str]:
        """Explain why a journal entry was created this way."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available."""
        pass


class DisabledProvider(AIProvider):
    """Provider that disables AI functionality (offline mode)."""
    
    def analyze_transaction(self, text: str) -> Optional[Dict[str, Any]]:
        logger.info("AI disabled - using rule engine only")
        return None
    
    def explain_entry(self, entry_data: Dict[str, Any]) -> Optional[str]:
        return None
    
    def is_available(self) -> bool:
        return False


class OpenAICompatibleProvider(AIProvider):
    """Provider for OpenAI-compatible APIs."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", 
                 model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self._available = False
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key, base_url=self.base_url)
            # Test connection
            self.client.models.list()
            self._available = True
            logger.info(f"Connected to OpenAI-compatible API at {base_url}")
        except Exception as e:
            logger.warning(f"Failed to connect to OpenAI API: {e}")
            self._available = False
    
    def is_available(self) -> bool:
        return self._available
    
    def analyze_transaction(self, text: str) -> Optional[Dict[str, Any]]:
        if not self._available:
            return None
        
        system_prompt = """You are an accounting assistant. Analyze the transaction text and extract:
- transaction_type: Type of transaction (purchase, sale, payment, receipt, etc.)
- amount: Numeric amount
- currency: Currency code (EGP, USD, etc.)
- party: Counterparty name (customer, supplier, etc.)
- payment_method: cash, bank, credit, etc.
- tax_amount: Tax amount if mentioned
- is_tax_inclusive: Whether amount includes tax
- debit_account_suggestion: Suggested debit account
- credit_account_suggestion: Suggested credit account
- confidence: 0-100 confidence score
- ambiguities: List of unclear points
- explanation: Brief explanation

Return ONLY valid JSON. Do not invent accounts or amounts."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this accounting transaction: {text}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            # Extract JSON from response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            result = json.loads(content)
            logger.info(f"AI analysis successful: {result.get('transaction_type', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return None
    
    def explain_entry(self, entry_data: Dict[str, Any]) -> Optional[str]:
        if not self._available:
            return None
        
        try:
            prompt = f"""Explain this accounting entry in simple terms:
Debit: {entry_data.get('debit_account', 'Unknown')}
Credit: {entry_data.get('credit_account', 'Unknown')}
Amount: {entry_data.get('amount', 0)}
Description: {entry_data.get('description', '')}

Why is this the correct accounting treatment?"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"AI explanation failed: {e}")
            return None


class OllamaProvider(AIProvider):
    """Provider for local Ollama LLM."""
    
    def __init__(self, base_url: str = "http://localhost:11434", 
                 model: str = "llama3.1"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self._available = False
        
        try:
            import requests
            # Test connection
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                self._available = True
                logger.info(f"Connected to Ollama at {base_url}")
        except Exception as e:
            logger.warning(f"Failed to connect to Ollama: {e}")
            self._available = False
    
    def is_available(self) -> bool:
        return self._available
    
    def analyze_transaction(self, text: str) -> Optional[Dict[str, Any]]:
        if not self._available:
            return None
        
        try:
            import requests
            
            prompt = f"""Analyze this accounting transaction and return JSON only:
Transaction: {text}

Required JSON fields:
{{
  "transaction_type": "",
  "amount": 0,
  "currency": "EGP",
  "party": "",
  "payment_method": "",
  "confidence": 0,
  "ambiguities": [],
  "explanation": ""
}}"""

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3}
                },
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json().get('response', '')
                # Extract JSON
                if '{' in content and '}' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    json_str = content[start:end]
                    return json.loads(json_str)
            
            return None
            
        except Exception as e:
            logger.error(f"Ollama analysis failed: {e}")
            return None
    
    def explain_entry(self, entry_data: Dict[str, Any]) -> Optional[str]:
        if not self._available:
            return None
        
        try:
            import requests
            
            prompt = f"""Explain this accounting entry simply:
Debit: {entry_data.get('debit_account', 'Unknown')}
Credit: {entry_data.get('credit_account', 'Unknown')}
Amount: {entry_data.get('amount', 0)}
Description: {entry_data.get('description', '')}

Why is this correct?"""

            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get('response', '')
            
            return None
            
        except Exception as e:
            logger.error(f"Ollama explanation failed: {e}")
            return None


class LMStudioProvider(AIProvider):
    """Provider for LM Studio local server."""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", 
                 model: str = "local-model"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self._available = False
        
        try:
            import requests
            # Test connection
            response = requests.get(f"{self.base_url}/models", timeout=5)
            if response.status_code == 200:
                self._available = True
                logger.info(f"Connected to LM Studio at {base_url}")
        except Exception as e:
            logger.warning(f"Failed to connect to LM Studio: {e}")
            self._available = False
    
    def is_available(self) -> bool:
        return self._available
    
    def analyze_transaction(self, text: str) -> Optional[Dict[str, Any]]:
        if not self._available:
            return None
        
        try:
            import requests
            
            system_prompt = """You are an accounting assistant. Return ONLY JSON with these fields:
transaction_type, amount, currency, party, payment_method, confidence, ambiguities, explanation"""

            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Analyze: {text}"}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500
                },
                timeout=30
            )
            
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                if '{' in content and '}' in content:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    json_str = content[start:end]
                    return json.loads(json_str)
            
            return None
            
        except Exception as e:
            logger.error(f"LM Studio analysis failed: {e}")
            return None
    
    def explain_entry(self, entry_data: Dict[str, Any]) -> Optional[str]:
        if not self._available:
            return None
        
        try:
            import requests
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{
                        "role": "user", 
                        "content": f"Explain: Dr {entry_data.get('debit_account')} Cr {entry_data.get('credit_account')} Amount {entry_data.get('amount')}"
                    }],
                    "temperature": 0.5
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            
            return None
            
        except Exception as e:
            logger.error(f"LM Studio explanation failed: {e}")
            return None


def create_provider(provider_type: str, config: Dict[str, Any]) -> AIProvider:
    """Factory function to create AI provider based on type."""
    
    if provider_type == "disabled" or not config.get('enabled', False):
        return DisabledProvider()
    
    elif provider_type == "openai":
        return OpenAICompatibleProvider(
            api_key=config.get('api_key', ''),
            base_url=config.get('base_url', 'https://api.openai.com/v1'),
            model=config.get('model', 'gpt-3.5-turbo')
        )
    
    elif provider_type == "ollama":
        return OllamaProvider(
            base_url=config.get('base_url', 'http://localhost:11434'),
            model=config.get('model', 'llama3.1')
        )
    
    elif provider_type == "lmstudio":
        return LMStudioProvider(
            base_url=config.get('base_url', 'http://localhost:1234/v1'),
            model=config.get('model', 'local-model')
        )
    
    else:
        logger.warning(f"Unknown provider type: {provider_type}, using disabled")
        return DisabledProvider()
