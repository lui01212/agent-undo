"""Tests for agent-undo journal."""

from __future__ import annotations

import pytest
from pathlib import Path

from agent_undo.journal import Journal


@pytest.fixture
def journal(tmp_path):
    """Create a temporary journal."""
    return Journal(tmp_path / "test.db")


def test_record_and_retrieve(journal):
    op_id = journal.record("test-session", "file-write", path="/tmp/foo.txt")
    assert op_id > 0
    ops = journal.get_session_ops("test-session")
    assert len(ops) == 1
    assert ops[0]["path"] == "/tmp/foo.txt"


def test_checkpoint(journal):
    journal.record("test-session", "file-write", path="/tmp/bar.txt")
    op_id = journal.checkpoint("test-session", "test-checkpoint")
    assert op_id > 0
    found = journal.find_checkpoint("test-session", "test-checkpoint")
    assert found == op_id


def test_timeline(journal):
    journal.record("test-session", "shell", command="echo hello")
    journal.record("test-session", "file-write", path="/tmp/x")
    journal.checkpoint("test-session", "cp1")
    timeline = journal.get_timeline("test-session")
    assert len(timeline) == 3


def test_rollback_ops_since(journal):
    journal.record("test-session", "file-write", path="/tmp/a")
    cp_id = journal.checkpoint("test-session", "before-change")
    journal.record("test-session", "file-write", path="/tmp/b")
    journal.record("test-session", "shell", command="rm -rf /tmp/c")
    ops = journal.get_ops_since("test-session", cp_id)
    # Returns only ops strictly AFTER the checkpoint (the checkpoint itself is just a marker)
    assert len(ops) == 2


def test_statistics(journal):
    journal.record("s1", "file-write")
    journal.record("s1", "shell")
    journal.record("s2", "file-write")
    stats = journal.get_statistics()
    assert stats["total_operations"] == 3
    assert stats["total_sessions"] == 2
    assert stats["by_type"]["file-write"] == 2
