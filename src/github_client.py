"""GitHub API client for fetching Kubernetes release information."""

import re
import requests
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs

from .config import GitHubConfig


@dataclass
class PRInfo:
    """Pull request information."""
    number: int
    title: str
    url: str
    body: str
    state: str
    merged: bool
    created_at: str
    merged_at: Optional[str]
    author: str
    labels: List[str]
    # Kubernetes 不需要 cherry_pick_from 字段


@dataclass
class IssueInfo:
    """Issue information."""
    number: int
    title: str
    url: str
    body: str
    state: str
    created_at: str
    closed_at: Optional[str]
    author: str
    labels: List[str]


@dataclass
class ChangelogSection:
    """CHANGELOG 中的一个变更部分。"""
    title: str
    content: str
    pr_numbers: List[int]
    issue_numbers: List[int]


@dataclass
class ReleaseInfo:
    """Release information."""
    tag_name: str
    name: str
    body: str
    published_at: str
    prerelease: bool
    draft: bool
    html_url: str
    author: str
    # Kubernetes 特有字段
    changelog_url: Optional[str] = None
    changelog_content: Optional[str] = None
    changelog_sections: Dict[str, ChangelogSection] = None  # 按标题索引的 sections


class GitHubClient:
    """GitHub API client for Kubernetes."""
    
    def __init__(self, config: GitHubConfig):
        self.config = config
        self.session = requests.Session()
        if config.token:
            self.session.headers.update({
                'Authorization': f'token {config.token}',
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def get_latest_release(self, include_prerelease: bool = False) -> Optional[ReleaseInfo]:
        """Get the latest release information."""
        if include_prerelease:
            # Get all releases and find the latest one (including prereleases)
            url = f"{self.config.api_url}/repos/{self.config.repo_owner}/{self.config.repo_name}/releases"
            try:
                response = self.session.get(url)
                response.raise_for_status()
                releases = response.json()

                if not releases:
                    return None

                # Return the first release (most recent)
                data = releases[0]
            except requests.RequestException as e:
                print(f"Error fetching releases: {e}")
                return None
        else:
            # Get only the latest stable release
            url = f"{self.config.api_url}/repos/{self.config.repo_owner}/{self.config.repo_name}/releases/latest"
            try:
                response = self.session.get(url)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                print(f"Error fetching latest release: {e}")
                return None

        release_info = ReleaseInfo(
            tag_name=data['tag_name'],
            name=data['name'],
            body=data['body'],
            published_at=data['published_at'],
            prerelease=data['prerelease'],
            draft=data['draft'],
            html_url=data['html_url'],
            author=data['author']['login'],
            changelog_sections={}
        )
        
        # 提取 CHANGELOG URL 并获取内容
        changelog_url = self._extract_changelog_url(data['body'], data['tag_name'])
        if changelog_url:
            release_info.changelog_url = changelog_url
            release_info.changelog_content = self._fetch_changelog(changelog_url)
            if release_info.changelog_content:
                release_info.changelog_sections = self._parse_changelog_sections(
                    release_info.changelog_content, 
                    data['tag_name']
                )
        
        return release_info
    
    def _extract_changelog_url(self, body: str, tag_name: str) -> Optional[str]:
        """从 release body 中提取 CHANGELOG URL。"""
        # 从 release body 中查找 CHANGELOG 链接
        patterns = [
            r'CHANGELOG\[(https://github\.com/kubernetes/kubernetes/blob/[^\]]+)\]',
            r'(https://github\.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-[\d.]+\.md)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, body)
            if match:
                url = match.group(1)
                # 转换为 raw URL
                return url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        
        # 如果没有找到，根据 tag 构造 URL
        # 例如 v1.34.0 -> CHANGELOG-1.34.md
        version_match = re.match(r'v(\d+)\.(\d+)', tag_name)
        if version_match:
            major, minor = version_match.groups()
            return self.config.changelog_url_template.format(version=f"{major}.{minor}")
        
        return None
    
    def _fetch_changelog(self, url: str) -> Optional[str]:
        """获取 CHANGELOG 文件内容。"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching changelog from {url}: {e}")
            return None
    
    def _parse_changelog_sections(self, content: str, tag_name: str) -> Dict[str, ChangelogSection]:
        """解析 CHANGELOG 内容，提取指定版本的各个部分。"""
        sections = {}
        
        # 找到指定版本的起始位置
        # 例如：# v1.34.0
        version_pattern = rf'^#\s+{re.escape(tag_name)}\s*$'
        lines = content.split('\n')
        
        start_idx = None
        for i, line in enumerate(lines):
            if re.match(version_pattern, line, re.MULTILINE):
                start_idx = i
                break
        
        if start_idx is None:
            print(f"⚠️ Version {tag_name} not found in CHANGELOG")
            return sections
        
        # 找到下一个版本的起始位置（或文件结尾）
        end_idx = len(lines)
        for i in range(start_idx + 1, len(lines)):
            if re.match(r'^#\s+v\d+\.\d+', lines[i]):
                end_idx = i
                break
        
        # 提取该版本的内容
        version_content = '\n'.join(lines[start_idx:end_idx])
        
        # 解析各个主要部分
        # 注意：Changes by Kind 是父标题，不单独提取，只提取它下面的子标题
        # 忽略：Downloads for、Dependencies 等非变更内容
        section_patterns = [
            # 二级标题（## 级别）
            (r'##\s+Changelog since v[\d.]+', "Changelog"),
            (r'##\s+Urgent Upgrade Notes', "Urgent Upgrade Notes"),
            (r'##\s+Important Security Information', "Important Security Information"),
            
            # Changes by Kind 下的子标题（### 级别）
            (r'###\s+Deprecation', "Deprecation"),
            (r'###\s+API Change', "API Change"),
            (r'###\s+Feature', "Feature"),
            (r'###\s+Documentation', "Documentation"),
            (r'###\s+Bug or Regression', "Bug or Regression"),
            (r'###\s+Failing Test', "Failing Test"),
            (r'###\s+Other \(Cleanup or Flake\)', "Other"),  # 匹配完整标题
            (r'###\s+Other', "Other"),
        ]
        
        for pattern, title in section_patterns:
            section_content = self._extract_section(version_content, pattern)
            if section_content:
                pr_numbers = self.extract_pr_numbers_from_text(section_content)
                issue_numbers = self.extract_issue_numbers_from_text(section_content)
                sections[title] = ChangelogSection(
                    title=title,
                    content=section_content,
                    pr_numbers=pr_numbers,
                    issue_numbers=issue_numbers
                )
        
        return sections
    
    def _extract_section(self, content: str, header_pattern: str) -> Optional[str]:
        """提取 CHANGELOG 中的某个部分。"""
        lines = content.split('\n')
        start_idx = None
        
        for i, line in enumerate(lines):
            if re.match(header_pattern, line):
                start_idx = i
                break
        
        if start_idx is None:
            return None
        
        # 找到下一个同级或更高级标题
        header_level = lines[start_idx].count('#')
        end_idx = len(lines)
        
        for i in range(start_idx + 1, len(lines)):
            line_level = 0
            if lines[i].startswith('#'):
                line_level = len(lines[i]) - len(lines[i].lstrip('#'))
                if line_level <= header_level:
                    end_idx = i
                    break
        
        return '\n'.join(lines[start_idx:end_idx])
    
    def extract_pr_numbers_from_text(self, text: str) -> List[int]:
        """Extract PR numbers from text."""
        # Kubernetes PR 格式: #12345 或完整 URL
        patterns = [
            r'#(\d+)',  # #12345
            r'https://github\.com/kubernetes/kubernetes/pull/(\d+)',  # Full PR URLs
        ]
        
        pr_numbers = set()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            pr_numbers.update(int(match) for match in matches)
        
        return sorted(list(pr_numbers))
    
    def get_pr_info(self, pr_number: int) -> Optional[PRInfo]:
        """Get detailed information about a pull request."""
        url = f"{self.config.api_url}/repos/{self.config.repo_owner}/{self.config.repo_name}/pulls/{pr_number}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            return PRInfo(
                number=data['number'],
                title=data['title'],
                url=data['html_url'],
                body=data['body'] or '',
                state=data['state'],
                merged=data['merged'],
                created_at=data['created_at'],
                merged_at=data.get('merged_at'),
                author=data['user']['login'],
                labels=[label['name'] for label in data['labels']]
            )
        except requests.RequestException as e:
            # 404 错误可能是正常的（PR 不存在或已删除），使用 debug 级别
            if '404' in str(e):
                print(f"⚠️  PR #{pr_number} not found (may have been deleted or is invalid)")
            else:
                print(f"❌ Error fetching PR {pr_number}: {e}")
            return None
    
    def extract_issue_numbers_from_text(self, text: str) -> List[int]:
        """Extract issue numbers from text."""
        # Pattern to match GitHub issue links
        patterns = [
            r'https://github\.com/kubernetes/kubernetes/issues/(\d+)',  # Full issue URLs
            r'(?:fixes?|closes?|resolves?)\s+#(\d+)',  # "fixes #123"
        ]
        
        issue_numbers = set()
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            issue_numbers.update(int(match) for match in matches)
        
        return sorted(list(issue_numbers))
    
    def get_issue_info(self, issue_number: int) -> Optional[IssueInfo]:
        """Get detailed information about an issue."""
        url = f"{self.config.api_url}/repos/{self.config.repo_owner}/{self.config.repo_name}/issues/{issue_number}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Skip if this is actually a PR (GitHub treats PRs as issues)
            if 'pull_request' in data:
                return None
            
            return IssueInfo(
                number=data['number'],
                title=data['title'],
                url=data['html_url'],
                body=data['body'] or '',
                state=data['state'],
                created_at=data['created_at'],
                closed_at=data.get('closed_at'),
                author=data['user']['login'],
                labels=[label['name'] for label in data['labels']]
            )
        except requests.RequestException as e:
            # 404 错误可能是正常的（Issue 不存在或已删除），使用 debug 级别
            if '404' in str(e):
                print(f"⚠️  Issue #{issue_number} not found (may have been deleted or is invalid)")
            else:
                print(f"❌ Error fetching issue {issue_number}: {e}")
            return None

