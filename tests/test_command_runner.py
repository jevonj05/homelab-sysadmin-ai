from agent.command_runner import available_actions, run_action


def test_unknown_action_is_denied():
    result = run_action("rm_everything")
    assert result["status"] == "denied"


def test_allowlist_is_explicit():
    assert "disk_free" in available_actions()
    assert "rm_everything" not in available_actions()
