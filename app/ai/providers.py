"""AI Providers abstraction layer for Finovate Journal AI."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import json


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.is_available = False

    @abstractmethod
    def analyze_transaction(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze a transaction text and return structured data."""
        pass

    @abstractmethod
    def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        """Explain why an accounting entry was made."""
        pass

    @abstractmethod
    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Answer accounting-related questions."""
        pass

    def is_connected(self) -> bool:
        """Check if the provider is connected and available."""
        return self.is_available

    def get_provider_name(self) -> str:
        """Get the name of the provider."""
        return self.__class__.__name__


class OpenAICompatibleProvider(AIProvider):
    """OpenAI-compatible API provider."""

    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, base_url, model)
        try:
            import requests
            self.requests = requests
            self.is_available = True
        except ImportError:
            self.is_available = False

    def analyze_transaction(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze a transaction using OpenAI-compatible API."""
        if not self.is_available:
            return self._get_fallback_response()

        system_prompt = """You are an accounting assistant. Analyze the transaction and return JSON with:
        - transaction_type: type of transaction
        - amount: numeric amount
        - currency: currency code
        - debit_account: suggested debit account
        - credit_account: suggested credit account
        - confidence: 0-100
        - explanation: brief explanation
        Return ONLY valid JSON."""

        try:
            response = self.requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": text}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 500
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            return self._get_fallback_response(str(e))

    def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        """Explain an accounting entry."""
        return f"Debit: {entry_data.get('debit_account', 'N/A')}, Credit: {entry_data.get('credit_account', 'N/A')}"

    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Answer accounting questions."""
        return "This feature requires an active AI connection."

    def _get_fallback_response(self, error: str = "") -> Dict[str, Any]:
        """Return fallback response when AI is unavailable."""
        return {
            "transaction_type": None,
            "amount": None,
            "currency": "EGP",
            "debit_account": None,
            "credit_account": None,
            "confidence": 0,
            "explanation": f"AI unavailable: {error}" if error else "AI service not available",
            "ambiguities": ["ai_unavailable"]
        }


class OllamaProvider(AIProvider):
    """Local Ollama LLM provider."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        super().__init__(base_url=base_url, model=model)
        try:
            import requests
            self.requests = requests
            self.is_available = self._check_connection()
        except ImportError:
            self.is_available = False

    def _check_connection(self) -> bool:
        """Check if Ollama is running."""
        try:
            response = self.requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def analyze_transaction(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze using local Ollama."""
        if not self.is_available:
            return {"transaction_type": None, "confidence": 0, "ambiguities": ["ollama_unavailable"]}

        prompt = f"""Analyze this accounting transaction and return JSON:
        Transaction: {text}
        Return: {{ "transaction_type": "", "amount": 0, "debit_account": "", "credit_account": "", "confidence": 0 }}"""

        try:
            response = self.requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return json.loads(data["response"])
        except Exception:
            return {"transaction_type": None, "confidence": 0}

    def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        """Explain entry using local LLM."""
        return f"Local AI explanation: {entry_data}"

    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Answer using local LLM."""
        return "Local AI response"


class LMStudioProvider(AIProvider):
    """LM Studio local provider."""

    def __init__(self, base_url: str = "http://localhost:1234/v1", model: str = "local-model"):
        super().__init__(base_url=base_url, model=model)
        try:
            import requests
            self.requests = requests
            self.is_available = self._check_connection()
        except ImportError:
            self.is_available = False

    def _check_connection(self) -> bool:
        """Check LM Studio connection."""
        try:
            response = self.requests.get(f"{self.base_url}/models", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def analyze_transaction(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze using LM Studio."""
        if not self.is_available:
            return {"transaction_type": None, "confidence": 0}
        # Similar to Ollama implementation
        return {"transaction_type": None, "confidence": 0}

    def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        return "LM Studio explanation"

    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        return "LM Studio response"


class DisabledProvider(AIProvider):
    """Disabled AI provider (offline mode)."""

    def __init__(self):
        super().__init__()
        self.is_available = False

    def analyze_transaction(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return {
            "transaction_type": None,
            "amount": None,
            "confidence": 0,
            "ambiguities": ["ai_disabled"],
            "explanation": "AI is disabled. Using rule-based analysis only."
        }

    def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        return "AI is disabled. No explanation available."

    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> str:
        return "AI is disabled. Please enable AI in settings."


def create_provider(provider_type: str, config: Dict[str, Any]) -> AIProvider:
    """Factory function to create AI provider instances."""
    providers = {
        "openai": OpenAICompatibleProvider,
        "ollama": OllamaProvider,
        "lmstudio": LMStudioProvider,
        "disabled": DisabledProvider,
    }

    provider_class = providers.get(provider_type.lower(), DisabledProvider)
    return provider_class(**config)
