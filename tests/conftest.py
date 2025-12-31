"""Pytest configuration - mock websocket_api before any imports."""
from __future__ import annotations

import sys
from unittest.mock import MagicMock

# Mock websocket_api BEFORE any test imports to avoid circular import
_mock_websocket_api = MagicMock()
_mock_websocket_api.websocket_command = lambda *args, **kwargs: lambda func: func
_mock_websocket_api.async_response = lambda func: func
_mock_websocket_api.async_register_command = MagicMock()

# Insert into sys.modules before any imports
sys.modules["homeassistant.components.websocket_api"] = _mock_websocket_api

