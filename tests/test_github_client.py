"""Tests for GitHub client."""

import pytest
from src.github_client import GitHubClient
from src.config import GitHubConfig


def test_github_client_initialization():
    """Test GitHub client initialization."""
    config = GitHubConfig()
    client = GitHubClient(config)
    assert client.config.repo_owner == "kubernetes"
    assert client.config.repo_name == "kubernetes"


def test_extract_pr_numbers():
    """Test PR number extraction from text."""
    config = GitHubConfig()
    client = GitHubClient(config)
    
    text = """
    This release includes #12345 and fixes #67890.
    See https://github.com/kubernetes/kubernetes/pull/11111 for details.
    """
    
    pr_numbers = client.extract_pr_numbers_from_text(text)
    assert 12345 in pr_numbers
    assert 67890 in pr_numbers
    assert 11111 in pr_numbers


def test_extract_issue_numbers():
    """Test issue number extraction from text."""
    config = GitHubConfig()
    client = GitHubClient(config)
    
    text = """
    Fixes #123 and closes https://github.com/kubernetes/kubernetes/issues/456
    Resolves #789
    """
    
    issue_numbers = client.extract_issue_numbers_from_text(text)
    assert 123 in issue_numbers
    assert 456 in issue_numbers
    assert 789 in issue_numbers


def test_changelog_url_extraction():
    """Test CHANGELOG URL extraction."""
    config = GitHubConfig()
    client = GitHubClient(config)
    
    # Test with explicit CHANGELOG link
    body = "See CHANGELOG[https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.34.md] for details."
    tag_name = "v1.34.0"
    
    url = client._extract_changelog_url(body, tag_name)
    assert url is not None
    assert "CHANGELOG-1.34.md" in url
    assert "raw.githubusercontent.com" in url


def test_parse_changelog_sections():
    """Test CHANGELOG section parsing."""
    config = GitHubConfig()
    client = GitHubClient(config)
    
    changelog_content = """
# v1.34.0

## Changelog since v1.33.0

## Urgent Upgrade Notes

- Important note 1 - [PR #12345](https://github.com/kubernetes/kubernetes/pull/12345)
- Important note 2

## Changes by Kind

### API Change

- API change 1 - [PR #12346](https://github.com/kubernetes/kubernetes/pull/12346)

### Bug or Regression

- Bug fix 1 - fixes #123

# v1.33.0

## Changelog since v1.32.0
"""
    
    sections = client._parse_changelog_sections(changelog_content, "v1.34.0")
    
    assert "Urgent Upgrade Notes" in sections
    assert "API Change" in sections
    assert "Bug or Regression" in sections
    
    # Check PR numbers are extracted
    urgent_section = sections["Urgent Upgrade Notes"]
    assert 12345 in urgent_section.pr_numbers
    
    api_section = sections["API Change"]
    assert 12346 in api_section.pr_numbers
    
    bug_section = sections["Bug or Regression"]
    assert 123 in bug_section.issue_numbers


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


