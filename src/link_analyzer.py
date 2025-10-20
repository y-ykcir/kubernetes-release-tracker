"""Intelligent link analysis module for Kubernetes releases."""

import re
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field

from .github_client import GitHubClient, PRInfo, IssueInfo, ReleaseInfo
from .config import AnalysisConfig


@dataclass
class AnalysisResult:
    """Result of link analysis."""
    release_info: ReleaseInfo
    analyzed_prs: Dict[int, PRInfo] = field(default_factory=dict)
    analyzed_issues: Dict[int, IssueInfo] = field(default_factory=dict)
    important_items: List[Tuple[str, str, str]] = field(default_factory=list)  # (type, title, reason)
    analysis_summary: str = ""
    # Kubernetes 特有字段
    changelog_summary: str = ""  # CHANGELOG 主要内容摘要


class LinkAnalyzer:
    """Intelligent link analyzer for Kubernetes releases."""
    
    def __init__(self, github_client: GitHubClient, config: AnalysisConfig):
        self.github_client = github_client
        self.config = config
    
    def analyze_release(self, release_info: ReleaseInfo) -> AnalysisResult:
        """Perform comprehensive analysis of a Kubernetes release."""
        result = AnalysisResult(release_info=release_info)
        
        # 如果有 CHANGELOG sections，优先分析这些
        if release_info.changelog_sections:
            print(f"📚 Analyzing CHANGELOG sections: {len(release_info.changelog_sections)} sections found")
            self._analyze_changelog_sections(release_info, result)
        else:
            # 否则从 release body 中提取 PR
            pr_numbers = self.github_client.extract_pr_numbers_from_text(release_info.body)
            self._analyze_prs_and_issues(pr_numbers[:self.config.max_links_to_analyze], result)
        
        # Identify important items
        self._identify_important_items(result)
        
        # Generate changelog summary
        result.changelog_summary = self._generate_changelog_summary(release_info)
        
        return result
    
    def _analyze_changelog_sections(self, release_info: ReleaseInfo, result: AnalysisResult) -> None:
        """分析 CHANGELOG 的各个部分。"""
        analyzed_prs = set()
        analyzed_issues = set()
        
        # 优先分析重要的部分（按优先级排序）
        priority_sections = [
            "Important Security Information",  # 最高优先级：安全信息
            "Urgent Upgrade Notes",            # 紧急升级注意事项
            "Deprecation",                     # 废弃功能
            "API Change",                      # API 变更
            "Bug or Regression"                # Bug 修复
        ]
        
        for section_title in priority_sections:
            if section_title in release_info.changelog_sections:
                section = release_info.changelog_sections[section_title]
                print(f"  📝 Analyzing section: {section_title} ({len(section.pr_numbers)} PRs)")
                self._analyze_prs_and_issues(
                    section.pr_numbers[:self.config.max_links_to_analyze // 4], 
                    result, 
                    analyzed_prs, 
                    analyzed_issues
                )
        
        # 然后分析其他部分
        for section_title, section in release_info.changelog_sections.items():
            if section_title not in priority_sections and len(analyzed_prs) < self.config.max_links_to_analyze:
                remaining_quota = self.config.max_links_to_analyze - len(analyzed_prs)
                if remaining_quota > 0:
                    print(f"  📝 Analyzing section: {section_title} ({len(section.pr_numbers)} PRs)")
                    self._analyze_prs_and_issues(
                        section.pr_numbers[:remaining_quota // 2], 
                        result, 
                        analyzed_prs, 
                        analyzed_issues
                    )
    
    def _analyze_prs_and_issues(self, pr_numbers: List[int], result: AnalysisResult, 
                                analyzed_prs: Optional[Set[int]] = None,
                                analyzed_issues: Optional[Set[int]] = None) -> None:
        """分析给定的 PR 列表及其关联的 issues。"""
        if analyzed_prs is None:
            analyzed_prs = set()
        if analyzed_issues is None:
            analyzed_issues = set()
        
        for pr_number in pr_numbers:
            if pr_number in analyzed_prs:
                continue
            
            pr_info = self.github_client.get_pr_info(pr_number)
            if not pr_info:
                continue
            
            analyzed_prs.add(pr_number)
            result.analyzed_prs[pr_number] = pr_info
            
            # 提取该 PR 中关联的 issues
            related_issues = self.github_client.extract_issue_numbers_from_text(
                f"{pr_info.title} {pr_info.body}"
            )
            
            # 分析相关 issues
            for issue_number in related_issues:
                if issue_number not in analyzed_issues:
                    self._analyze_issue(issue_number, result, analyzed_issues)
    
    def _analyze_issue(self, issue_number: int, result: AnalysisResult, 
                      analyzed_issues: Set[int]) -> None:
        """Analyze an issue."""
        if issue_number in analyzed_issues:
            return
        
        issue_info = self.github_client.get_issue_info(issue_number)
        if not issue_info:
            return
        
        analyzed_issues.add(issue_number)
        result.analyzed_issues[issue_number] = issue_info
    
    def _identify_important_items(self, result: AnalysisResult) -> None:
        """Identify important PRs and issues based on keywords and patterns."""
        important_items = []
        
        # Check PRs for important keywords
        for pr_number, pr_info in result.analyzed_prs.items():
            importance_reasons = self._check_importance(
                f"{pr_info.title} {pr_info.body}", pr_info.labels
            )
            if importance_reasons:
                important_items.append((
                    "PR", 
                    f"#{pr_number}: {pr_info.title}",
                    "; ".join(importance_reasons)
                ))
        
        # Check issues for important keywords
        for issue_number, issue_info in result.analyzed_issues.items():
            importance_reasons = self._check_importance(
                f"{issue_info.title} {issue_info.body}", issue_info.labels
            )
            if importance_reasons:
                important_items.append((
                    "Issue", 
                    f"#{issue_number}: {issue_info.title}",
                    "; ".join(importance_reasons)
                ))
        
        result.important_items = important_items
    
    def _check_importance(self, text: str, labels: List[str]) -> List[str]:
        """Check if text or labels contain important keywords."""
        reasons = []
        text_lower = text.lower()
        
        # Check for important keywords in text
        for keyword in self.config.important_keywords:
            if keyword.lower() in text_lower:
                reasons.append(f"Contains '{keyword}'")
        
        # Check for important labels
        important_labels = ['security', 'critical', 'urgent', 'bug', 'regression', 'kind/bug', 
                           'sig/api-machinery', 'priority/critical-urgent']
        for label in labels:
            if any(important_label in label.lower() for important_label in important_labels):
                reasons.append(f"Has label '{label}'")
        
        # Check for panic or crash patterns
        if re.search(r'panic|crash|segfault|sigsegv', text_lower):
            reasons.append("Potential crash issue")
        
        # Check for performance issues
        if re.search(r'performance|slow|timeout|hang', text_lower):
            reasons.append("Performance related")
        
        # Check for breaking changes
        if re.search(r'breaking.?change', text_lower):
            reasons.append("Breaking change")
        
        # Check for deprecation
        if re.search(r'deprecat', text_lower):
            reasons.append("Deprecation")
        
        return reasons
    
    def _generate_changelog_summary(self, release_info: ReleaseInfo) -> str:
        """生成 CHANGELOG 的摘要。"""
        if not release_info.changelog_sections:
            return ""
        
        summary_parts = []
        
        # 优先总结重要部分（按优先级排序）
        
        # 1. 安全信息（最高优先级）
        if "Important Security Information" in release_info.changelog_sections:
            section = release_info.changelog_sections["Important Security Information"]
            summary_parts.append(f"🔒 **重要安全信息** ({len(section.pr_numbers)} PRs)")
            # 提取前几行内容作为预览
            preview = self._extract_preview(section.content, 3)
            if preview:
                summary_parts.append(preview)
        
        # 2. 紧急升级注意事项
        if "Urgent Upgrade Notes" in release_info.changelog_sections:
            section = release_info.changelog_sections["Urgent Upgrade Notes"]
            summary_parts.append(f"\n⚠️ **紧急升级注意事项** ({len(section.pr_numbers)} PRs)")
            # 提取前几行内容作为预览
            preview = self._extract_preview(section.content, 3)
            if preview:
                summary_parts.append(preview)
        
        # 3. 废弃功能
        if "Deprecation" in release_info.changelog_sections:
            section = release_info.changelog_sections["Deprecation"]
            summary_parts.append(f"\n🔄 **废弃功能** ({len(section.pr_numbers)} PRs)")
        
        # 4. API 变更
        if "API Change" in release_info.changelog_sections:
            section = release_info.changelog_sections["API Change"]
            summary_parts.append(f"\n🔧 **API 变更** ({len(section.pr_numbers)} PRs)")
        
        # 5. Bug 修复
        if "Bug or Regression" in release_info.changelog_sections:
            section = release_info.changelog_sections["Bug or Regression"]
            summary_parts.append(f"\n🐛 **Bug 修复** ({len(section.pr_numbers)} PRs)")
        
        # 6. 新功能
        if "Feature" in release_info.changelog_sections:
            section = release_info.changelog_sections["Feature"]
            summary_parts.append(f"\n✨ **新功能** ({len(section.pr_numbers)} PRs)")
        
        # 7. 文档更新
        if "Documentation" in release_info.changelog_sections:
            section = release_info.changelog_sections["Documentation"]
            summary_parts.append(f"\n📚 **文档更新** ({len(section.pr_numbers)} PRs)")
        
        return "\n".join(summary_parts)
    
    def _extract_preview(self, content: str, max_lines: int = 3) -> str:
        """提取内容的前几行作为预览。"""
        lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('#')]
        preview_lines = lines[:max_lines]
        if len(lines) > max_lines:
            preview_lines.append("...")
        return "\n".join(preview_lines)
    
    def generate_summary(self, result: AnalysisResult) -> str:
        """Generate a summary of the analysis."""
        summary_parts = []
        
        summary_parts.append(f"Release: {result.release_info.name} ({result.release_info.tag_name})")
        summary_parts.append(f"Published: {result.release_info.published_at}")
        summary_parts.append(f"Analyzed PRs: {len(result.analyzed_prs)}")
        summary_parts.append(f"Analyzed Issues: {len(result.analyzed_issues)}")
        summary_parts.append(f"Important Items: {len(result.important_items)}")
        
        if result.changelog_summary:
            summary_parts.append("\nCHANGELOG Summary:")
            summary_parts.append(result.changelog_summary)
        
        if result.important_items:
            summary_parts.append("\nImportant Items:")
            for item_type, title, reason in result.important_items[:10]:  # 只显示前10个
                summary_parts.append(f"- {item_type}: {title} ({reason})")
        
        result.analysis_summary = "\n".join(summary_parts)
        return result.analysis_summary
