"""
Finovate Journal AI - AI Provider Abstraction Layer
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import json
import logging

from app.utils.logging_config import get_logger

logger = get_logger(__name__)


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key
        self.endpoint = endpoint
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def analyze_transaction(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze a transaction description and return structured data
        
        Args:
            text: Transaction description
            context: Additional context (accounts, rules, etc.)
            
        Returns:
            Dictionary with analysis results
        """
        pass
    
    @abstractmethod
    async def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        """
        Explain why a journal entry was created this way
        
        Args:
            entry_data: Journal entry data
            
        Returns:
            Human-readable explanation
        """
        pass
    
    @abstractmethod
    async def answer_question(self, question: str, context: Optional[Dict] = None) -> str:
        """
        Answer accounting-related questions
        
        Args:
            question: User question
            context: Additional context
            
        Returns:
            Answer string
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available/configured"""
        pass


class OpenAICompatibleProvider(AIProvider):
    """OpenAI-compatible API provider"""
    
    def __init__(self, api_key: str, endpoint: str = "https://api.openai.com/v1", model: str = "gpt-3.5-turbo"):
        super().__init__(api_key, endpoint)
        self.model = model
        self._available = bool(api_key)
    
    def is_available(self) -> bool:
        return self._available
    
    async def analyze_transaction(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze transaction using OpenAI-compatible API"""
        if not self.is_available():
            raise RuntimeError("API key not configured")
        
        # TODO: Implement actual API call
        # This is a placeholder for the actual implementation
        return {
            "transaction_type": "general",
            "amount": None,
            "currency": "EGP",
            "entries": [],
            "confidence": 0.0,
            "explanation": "AI provider not fully implemented yet"
        }
    
    async def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        """Explain journal entry"""
        if not self.is_available():
            return "AI provider not available"
        
        # TODO: Implement actual API call
        return "Explanation not available - AI provider not fully implemented"
    
    async def answer_question(self, question: str, context: Optional[Dict] = None) -> str:
        """Answer accounting question"""
        if not self.is_available():
            return "AI provider not available"
        
        # TODO: Implement actual API call
        return "Answer not available - AI provider not fully implemented"


class OllamaProvider(AIProvider):
    """Local Ollama LLM provider"""
    
    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "llama2"):
        super().__init__(endpoint=endpoint)
        self.model = model
        self._available = False  # Will check on first use
    
    def is_available(self) -> bool:
        # TODO: Implement health check
        return self._available
    
    async def analyze_transaction(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze transaction using local Ollama"""
        if not self.is_available():
            raise RuntimeError("Ollama not available")
        
        # TODO: Implement actual API call
        return {
            "transaction_type": "general",
            "amount": None,
            "currency": "EGP",
            "entries": [],
            "confidence": 0.0,
            "explanation": "Local AI not fully implemented yet"
        }
    
    async def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        return "Local AI explanation not available yet"
    
    async def answer_question(self, question: str, context: Optional[Dict] = None) -> str:
        return "Local AI answers not available yet"


class LMStudioProvider(AIProvider):
    """LM Studio local LLM provider"""
    
    def __init__(self, endpoint: str = "http://localhost:1234/v1", model: str = "local-model"):
        super().__init__(endpoint=endpoint)
        self.model = model
        self._available = False
    
    def is_available(self) -> bool:
        return self._available
    
    async def analyze_transaction(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        if not self.is_available():
            raise RuntimeError("LM Studio not available")
        
        # TODO: Implement actual API call
        return {
            "transaction_type": "general",
            "amount": None,
            "currency": "EGP",
            "entries": [],
            "confidence": 0.0,
            "explanation": "LM Studio not fully implemented yet"
        }
    
    async def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        return "LM Studio explanation not available yet"
    
    async def answer_question(self, question: str, context: Optional[Dict] = None) -> str:
        return "LM Studio answers not available yet"


class RuleBasedProvider(AIProvider):
    """
    Rule-based provider that uses the accounting rule engine
    This works offline and doesn't require any AI service
    """
    
    def __init__(self, rule_engine=None):
        super().__init__()
        self.rule_engine = rule_engine
        self._available = True
    
    def is_available(self) -> bool:
        return True
    
    async def analyze_transaction(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Analyze transaction using rule engine"""
        from app.accounting.rules import get_rule_engine
        from app.nlp.parser import get_parser
        
        if self.rule_engine is None:
            self.rule_engine = get_rule_engine()
        
        parser = get_parser()
        
        # Parse with NLP
        parsed = parser.parse(text)
        
        # Match with rules
        rule, lines = self.rule_engine.suggest_accounts(text, parsed.amount or 0)
        
        entries = []
        if rule:
            for line in lines:
                entries.append({
                    "account_code": line.account_code,
                    "account_name": line.account_name,
                    "debit": str(line.debit),
                    "credit": str(line.credit),
                    "description": line.description
                })
        
        return {
            "transaction_type": parsed.transaction_type,
            "amount": str(parsed.amount) if parsed.amount else None,
            "currency": parsed.currency,
            "party": parsed.party,
            "payment_method": parsed.payment_method,
            "tax_detected": parsed.tax_detected,
            "tax_amount": str(parsed.tax_amount) if parsed.tax_amount else None,
            "entries": entries,
            "confidence": parsed.confidence,
            "ambiguities": parsed.ambiguities,
            "explanation": parsed.explanation,
            "matched_rule": rule.id if rule else None,
            "source": "rule_engine"
        }
    
    async def explain_entry(self, entry_data: Dict[str, Any]) -> str:
        """Explain entry based on accounting rules"""
        entries = entry_data.get("entries", [])
        explanation_parts = []
        
        for entry in entries:
            debit = entry.get("debit", "0")
            credit = entry.get("credit", "0")
            account = entry.get("account_name", "Unknown")
            
            if float(debit) > 0:
                explanation_parts.append(f"تم قيد مبلغ {debit} في حساب {account} (مدين)")
            if float(credit) > 0:
                explanation_parts.append(f"تم قيد مبلغ {credit} في حساب {account} (دائن)")
        
        return "\n".join(explanation_parts) if explanation_parts else "لا يوجد تفسير متاح"
    
    async def answer_question(self, question: str, context: Optional[Dict] = None) -> str:
        """Answer basic accounting questions using predefined responses"""
        question_lower = question.lower()
        
        # Simple keyword matching for common questions
        if "ميزان" in question_lower or "trial balance" in question_lower:
            return "ميزان المراجعة هو تقرير يعرض أرصدة جميع الحسابات للتأكد من توازن المدين والدائن"
        
        if "قيد" in question_lower and ("لماذا" in question_lower or "why" in question_lower):
            return "يتم إنشاء القيد بناءً على قواعد محاسبية معتمدة. يرجى مراجعة تفاصيل القيد لفهم الحسابات المستخدمة"
        
        if "ضريبة" in question_lower or "tax" in question_lower:
            return "الضريبة تُحسب حسب النسبة المحددة في الإعدادات. حالياً النسبة الافتراضية هي 14%"
        
        return "عذراً، لا أملك إجابة محددة لهذا السؤال. يمكنك الرجوع إلى دليل المحاسبة أو استشارة محاسب مختص"


# Provider factory
def create_provider(provider_type: str, **kwargs) -> AIProvider:
    """
    Create an AI provider instance
    
    Args:
        provider_type: Type of provider (openai, ollama, lmstudio, rule_based)
        **kwargs: Provider-specific arguments
        
    Returns:
        AIProvider instance
    """
    providers = {
        "openai": OpenAICompatibleProvider,
        "ollama": OllamaProvider,
        "lmstudio": LMStudioProvider,
        "rule_based": RuleBasedProvider,
    }
    
    provider_class = providers.get(provider_type.lower())
    if not provider_class:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    return provider_class(**kwargs)


# Global provider registry
_providers: Dict[str, AIProvider] = {}


def register_provider(name: str, provider: AIProvider) -> None:
    """Register an AI provider"""
    _providers[name] = provider
    logger.info("Registered AI provider: %s", name)


def get_provider(name: str) -> Optional[AIProvider]:
    """Get a registered AI provider"""
    return _providers.get(name)


def get_default_provider() -> AIProvider:
    """Get the default rule-based provider"""
    if "default" not in _providers:
        _providers["default"] = RuleBasedProvider()
    return _providers["default"]
