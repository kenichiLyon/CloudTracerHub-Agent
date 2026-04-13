from pathlib import Path

from lubster.config import load_config
from lubster.mcp_server import MCPServer


BASE = Path(__file__).resolve().parents[1]


def test_load_config_uses_project_default(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    cfg = load_config()
    assert cfg["mock_mode"] is True


def test_mcp_call_without_config_path_uses_default_config(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    server = MCPServer()
    response = server.handle_request(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "lubster_agent_diagnose",
                "arguments": {
                    "incident": {
                        "title": "worker timeout",
                        "namespace": "default",
                        "service": "worker",
                        "symptoms": ["timeout"],
                    }
                },
            },
        }
    )
    assert response is not None
    assert response["result"]["isError"] is False
    assert response["result"]["structuredContent"]["meta"]["engine"] == "lubster"
    assert response["result"]["structuredContent"]["meta"]["server"] == "lubster-agent"


def test_project_example_config_exists():
    assert (BASE / "examples" / "lubster.config.json").exists()
