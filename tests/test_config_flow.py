"""Unit tests for config flow."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from custom_components.ferbos_query_executor.config_flow import FerbosQueryExecutorConfigFlow


@pytest.mark.unit
class TestConfigFlow:
    """Test the config flow."""

    @pytest.mark.asyncio
    async def test_async_step_user_no_input(self):
        """Test config flow step user with no input."""
        flow = FerbosQueryExecutorConfigFlow()
        flow.hass = MagicMock()
        
        result = await flow.async_step_user()
        assert result["type"] == "form"
        assert result["step_id"] == "user"

    @pytest.mark.asyncio
    async def test_async_step_user_with_input(self):
        """Test config flow step user with input."""
        flow = FerbosQueryExecutorConfigFlow()
        flow.hass = MagicMock()
        
        with patch.object(flow, "async_create_entry") as mock_create:
            mock_create.return_value = {"type": "create_entry", "title": "Ferbos Query Executor"}
            result = await flow.async_step_user(user_input={})
            assert result["type"] == "create_entry"
            mock_create.assert_called_once_with(title="Ferbos Query Executor", data={})


