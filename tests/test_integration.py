"""Integration smoke tests for Ferbos Query Executor."""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pathlib import Path


@pytest.mark.smoke
@pytest.mark.integration
class TestIntegrationSmoke:
    """Smoke tests for basic integration functionality."""

    @pytest.mark.asyncio
    async def test_manifest_valid(self):
        """Test that manifest.json is valid and contains required fields."""
        import json
        from pathlib import Path
        
        manifest_path = Path("custom_components/ferbos_query_executor/manifest.json")
        assert manifest_path.exists(), "manifest.json does not exist"
        
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        required_fields = ["domain", "name", "version", "codeowners"]
        for field in required_fields:
            assert field in manifest, f"Missing required field: {field}"
        
        assert manifest["domain"] == "ferbos_query_executor"
        assert isinstance(manifest.get("codeowners", []), list)

    @pytest.mark.asyncio
    async def test_hacs_json_valid(self):
        """Test that hacs.json is valid."""
        import json
        from pathlib import Path
        
        hacs_path = Path("hacs.json")
        assert hacs_path.exists(), "hacs.json does not exist"
        
        with open(hacs_path) as f:
            hacs = json.load(f)
        
        assert "name" in hacs
        assert "domains" in hacs
        assert isinstance(hacs["domains"], list)
        assert "ferbos_query_executor" in hacs["domains"]

    @pytest.mark.asyncio
    async def test_const_domain(self):
        """Test that const.py defines DOMAIN correctly."""
        from custom_components.ferbos_query_executor.const import DOMAIN
        assert DOMAIN == "ferbos_query_executor"

    @pytest.mark.asyncio
    async def test_imports(self):
        """Test that all modules can be imported."""
        from custom_components.ferbos_query_executor import async_setup, async_setup_entry
        from custom_components.ferbos_query_executor.config_flow import FerbosQueryExecutorConfigFlow
        from custom_components.ferbos_query_executor.const import DOMAIN
        
        assert async_setup is not None
        assert async_setup_entry is not None
        assert FerbosQueryExecutorConfigFlow is not None
        assert DOMAIN is not None

    @pytest.mark.asyncio
    async def test_websocket_command_registration(self):
        """Test that websocket commands are registered during setup."""
        from unittest.mock import MagicMock, patch
        
        hass = MagicMock()
        config = {}
        
        with patch("custom_components.ferbos_query_executor.__init__.websocket_api") as mock_ws:
            from custom_components.ferbos_query_executor import async_setup
            await async_setup(hass, config)
            
            # Verify websocket command was registered
            assert mock_ws.async_register_command.called

