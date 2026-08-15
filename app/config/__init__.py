"""
Finovate Journal AI - Configuration Module

Developer: Ahmed Mostafa Ibrahim
Brand: Finovate – AHMED EG
"""

from .settings import Settings, get_settings
from .constants import (
    APP_NAME,
    APP_VERSION,
    DEVELOPER_NAME,
    DEVELOPER_BRAND,
    DEVELOPER_EMAIL,
    DEVELOPER_PHONE,
    COPYRIGHT_TEXT,
    DEFAULT_CURRENCY,
    DEFAULT_LANGUAGE,
    SUPPORTED_LANGUAGES,
    JOURNAL_ENTRY_PREFIX,
)

__all__ = [
    "Settings",
    "get_settings",
    "APP_NAME",
    "APP_VERSION",
    "DEVELOPER_NAME",
    "DEVELOPER_BRAND",
    "DEVELOPER_EMAIL",
    "DEVELOPER_PHONE",
    "COPYRIGHT_TEXT",
    "DEFAULT_CURRENCY",
    "DEFAULT_LANGUAGE",
    "SUPPORTED_LANGUAGES",
    "JOURNAL_ENTRY_PREFIX",
]
