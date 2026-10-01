from agent.checks.disk_check import get_disk_usage


def test_missing_path_returns_structured_error():
    result = get_disk_usage("/this/path/should/not/exist/sysadmin-ai")
    assert result["status"] == "error"
    assert result["error"] == "path_not_found"


def test_root_path_returns_usage():
    result = get_disk_usage("/")
    assert result["status"] in {"healthy", "warning", "critical"}
    assert 0 <= result["used_percentage"] <= 100
