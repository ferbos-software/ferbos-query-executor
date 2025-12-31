"""Unit tests for Ferbos Query Executor integration."""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from pathlib import Path
import aiosqlite

from custom_components.ferbos_query_executor import async_setup, async_setup_entry
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

    @pytest.mark.asyncio
    async def test_database_not_found(self):
        """Test that missing database returns error."""
        hass = MagicMock()
        hass.config.path.return_value = "/nonexistent/path/home-assistant_v2.db"
        
        with patch("custom_components.ferbos_query_executor.__init__.Path") as mock_path:
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = False
            mock_path.return_value = mock_path_instance
            
            result = await _run_sqlite_query(hass, {"query": "SELECT 1"})
            assert result["success"] is False
            assert result["error"]["code"] == "not_found"

    @pytest.mark.asyncio
    async def test_select_query_success(self):
        """Test successful SELECT query."""
        hass = MagicMock()
        hass.config.path.return_value = "/test/home-assistant_v2.db"
        
        # Mock row that can be converted to dict
        # Simulate aiosqlite.Row behavior
        class MockRow:
            def __init__(self):
                self._data = {"id": 1, "name": "test"}
            
            def keys(self):
                return self._data.keys()
            
            def __getitem__(self, key):
                return self._data[key]
        
        mock_row = MockRow()
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [mock_row]
        mock_cursor.close = AsyncMock()
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_cursor
        mock_db.__aenter__.return_value = mock_db
        mock_db.__aexit__.return_value = None
        
        with patch("custom_components.ferbos_query_executor.__init__.Path") as mock_path, \
             patch("aiosqlite.connect", return_value=mock_db), \
             patch("builtins.dict", side_effect=lambda x, **kw: x._data if isinstance(x, MockRow) else dict(x, **kw) if hasattr(x, '__iter__') else {}):
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.as_posix.return_value = "/test/home-assistant_v2.db"
            mock_path.return_value = mock_path_instance
            
            result = await _run_sqlite_query(hass, {"query": "SELECT * FROM states LIMIT 1"})
            assert result["success"] is True
            assert "data" in result
            assert isinstance(result["data"], list)
            assert len(result["data"]) == 1

    @pytest.mark.asyncio
    async def test_non_select_query_success(self):
        """Test successful non-SELECT query."""
        hass = MagicMock()
        hass.config.path.return_value = "/test/home-assistant_v2.db"
        
        mock_cursor = AsyncMock()
        mock_cursor.rowcount = 1
        mock_cursor.lastrowid = 123
        mock_cursor.close = AsyncMock()
        
        mock_db = AsyncMock()
        mock_db.execute.return_value = mock_cursor
        mock_db.commit = AsyncMock()
        mock_db.__aenter__.return_value = mock_db
        mock_db.__aexit__.return_value = None
        
        with patch("custom_components.ferbos_query_executor.__init__.Path") as mock_path, \
             patch("aiosqlite.connect", return_value=mock_db):
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.as_posix.return_value = "/test/home-assistant_v2.db"
            mock_path.return_value = mock_path_instance
            
            result = await _run_sqlite_query(
                hass, 
                {"query": "UPDATE states SET state = ? WHERE entity_id = ?", "params": ["new_state", "test.entity"]}
            )
            assert result["success"] is True
            assert "data" in result
            assert result["data"]["rowcount"] == 1

    @pytest.mark.asyncio
    async def test_sqlite_error_handling(self):
        """Test that SQLite errors are properly handled."""
        hass = MagicMock()
        hass.config.path.return_value = "/test/home-assistant_v2.db"
        
        with patch("custom_components.ferbos_query_executor.__init__.Path") as mock_path, \
             patch("aiosqlite.connect", side_effect=Exception("Database locked")):
            mock_path_instance = MagicMock()
            mock_path_instance.exists.return_value = True
            mock_path_instance.as_posix.return_value = "/test/home-assistant_v2.db"
            mock_path.return_value = mock_path_instance
            
            result = await _run_sqlite_query(hass, {"query": "SELECT 1"})
            assert result["success"] is False
            assert result["error"]["code"] == "sqlite_error"
            assert "Database locked" in result["error"]["message"]


@pytest.mark.unit
class TestSetup:
    """Test setup functions."""

    @pytest.mark.asyncio
    async def test_async_setup(self):
        """Test async_setup function."""
        hass = MagicMock()
        config = {}
        
        with patch("custom_components.ferbos_query_executor.__init__.websocket_api") as mock_ws:
            result = await async_setup(hass, config)
            assert result is True
            assert mock_ws.async_register_command.called

    @pytest.mark.asyncio
    async def test_async_setup_entry(self):
        """Test async_setup_entry function."""
        hass = MagicMock()
        entry = MagicMock()
        
        with patch("custom_components.ferbos_query_executor.__init__.websocket_api") as mock_ws:
            result = await async_setup_entry(hass, entry)
            assert result is True
            assert mock_ws.async_register_command.called

