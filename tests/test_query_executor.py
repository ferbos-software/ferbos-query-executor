"""Unit tests for Ferbos Query Executor integration."""
from __future__ import annotations

import pytest
from unittest.mock import MagicMock

# Import after conftest.py has mocked websocket_api
from custom_components.ferbos_query_executor.__init__ import _run_sqlite_query


@pytest.mark.unit
class TestRunSqliteQuery:
    """Test the _run_sqlite_query function."""

    @pytest.mark.asyncio
    async def test_missing_query(self):
        """Test that missing query returns error."""
        hass = MagicMock()
        result = await _run_sqlite_query(hass, {})
        assert result["success"] is False
        assert result["error"]["code"] == "invalid"
        assert "Missing query" in result["error"]["message"]
