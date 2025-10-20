"""Report generation module for creating detailed analysis reports."""

import os
import re
import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from .config import ReportsConfig
from .llm_analyzer import LLMAnalysisResult, LLMAnalyzer
from .link_analyzer import AnalysisResult


class ReportGenerator:
    """Generate detailed analysis reports."""
    
    def __init__(self, config: ReportsConfig, llm_analyzer: LLMAnalyzer = None):
        self.config = config
        self.llm_analyzer = llm_analyzer
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, analysis_result: AnalysisResult, 
                       llm_result: LLMAnalysisResult) -> str:
        """Generate comprehensive analysis report."""
        release = analysis_result.release_info
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 清理 tag_name，替换不安全的文件名字符
        safe_tag_name = release.tag_name.replace('/', '_').replace('\\', '_')
        filename = f"kubernetes_release_{safe_tag_name}_{timestamp}.md"
        filepath = os.path.join(self.config.output_dir, filename)
        
        # Generate report content
        content = self._generate_markdown_report(analysis_result, llm_result)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Also generate JSON report for programmatic access
        json_filename = f"kubernetes_release_{safe_tag_name}_{timestamp}.json"
        json_filepath = os.path.join(self.config.output_dir, json_filename)
        self._generate_json_report(analysis_result, llm_result, json_filepath)
        
        print(f"Report generated: {filepath}")
        print(f"JSON data generated: {json_filepath}")
        
        return filepath
    
    def _generate_markdown_report(self, analysis_result: AnalysisResult,
                                llm_result: LLMAnalysisResult) -> str:
        """Generate markdown report content."""
        release = analysis_result.release_info

        md_parts = []

        # Title and metadata
        md_parts.append(f"# Kubernetes 版本发布分析报告")
        md_parts.append(f"## {release.name} ({release.tag_name})")
        md_parts.append("")
        md_parts.append("### 📋 版本信息")
        md_parts.append(f"- **版本标签：** {release.tag_name}")
        md_parts.append(f"- **版本名称：** {release.name}")
        md_parts.append(f"- **发布时间：** {release.published_at}")
        md_parts.append(f"- **发布者：** {release.author}")
        md_parts.append(f"- **预发布版本：** {'是' if release.prerelease else '否'}")
        md_parts.append(f"- **草稿状态：** {'是' if release.draft else '否'}")
        md_parts.append(f"- **GitHub 链接：** {release.html_url}")
        md_parts.append("")

        # Analysis metadata
        md_parts.append("### 🔍 分析统计")
        md_parts.append(f"- **分析时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_parts.append(f"- **分析的 PR 数量：** {len(analysis_result.analyzed_prs)}")
        md_parts.append(f"- **分析的 Issue 数量：** {len(analysis_result.analyzed_issues)}")
        md_parts.append(f"- **重要项目数量：** {len(analysis_result.important_items)}")
        md_parts.append("")
        
        # Executive Summary
        md_parts.append("## 📊 版本概述")
        if llm_result.summary:
            md_parts.append(llm_result.summary)
        else:
            md_parts.append("暂无 AI 生成的版本概述。")
        md_parts.append("")

        # Security Issues (优先显示安全问题)
        if llm_result.security_issues:
            md_parts.append("## 🔒 安全问题修复")
            for i, security_issue in enumerate(llm_result.security_issues, 1):
                md_parts.append(f"{i}. ⚠️ {security_issue}")
            md_parts.append("")
            md_parts.append("**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。")
            md_parts.append("")

        # Important Bugfixes
        if llm_result.important_bugfixes:
            md_parts.append("## 🐛 重要问题修复")
            for i, bugfix in enumerate(llm_result.important_bugfixes, 1):
                md_parts.append(f"{i}. {bugfix}")
            md_parts.append("")

        # Breaking Changes
        if llm_result.breaking_changes:
            md_parts.append("## 💥 破坏性变更")
            for i, breaking_change in enumerate(llm_result.breaking_changes, 1):
                md_parts.append(f"{i}. 🚨 {breaking_change}")
            md_parts.append("")
            md_parts.append("**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。")
            md_parts.append("")

        # Key Changes
        if llm_result.key_changes:
            md_parts.append("## ✨ 主要变更")
            for i, change in enumerate(llm_result.key_changes, 1):
                md_parts.append(f"{i}. {change}")
            md_parts.append("")

        # Performance Improvements
        if llm_result.performance_improvements:
            md_parts.append("## 🚀 性能优化")
            for i, improvement in enumerate(llm_result.performance_improvements, 1):
                md_parts.append(f"{i}. {improvement}")
            md_parts.append("")
        
        # Risk Assessment
        if llm_result.risk_assessment:
            md_parts.append("## 🎯 风险评估")
            md_parts.append(llm_result.risk_assessment)
            md_parts.append("")

        # Recommendations
        if llm_result.recommendations:
            md_parts.append("## 📋 升级建议")
            for i, recommendation in enumerate(llm_result.recommendations, 1):
                md_parts.append(f"{i}. {recommendation}")
            md_parts.append("")
        
        # 完整的 Release PR 列表（只显示 release notes 中直接提到的 PR）
        if self.config.include_pr_details and analysis_result.analyzed_prs:
            # 获取 release notes 中直接提到的 PR（这些是要展示的主要PR）
            release_prs = self._get_release_mentioned_prs(analysis_result)
            
            if release_prs:
                # 批量收集聚合内容并总结
                pr_summaries = {}
                if self.llm_analyzer:
                    pr_aggregated_texts = {}
                    for pr_number, pr_info in release_prs.items():
                        # 收集PR的所有相关内容（包括Issues、原始PR、原始PR的Issues）
                        aggregated_content = self._collect_pr_aggregated_content(
                            pr_number, pr_info, analysis_result
                        )
                        # 使用字符串格式的数字作为键，与 LLM 返回格式一致
                        pr_aggregated_texts[str(pr_number)] = aggregated_content
                    
                    # 批量总结所有PR的聚合内容
                    pr_summaries = self.llm_analyzer.batch_summarize_texts(
                        pr_aggregated_texts, 
                        item_type="PR完整内容（包含关联Issue和原始PR）", 
                        max_length=400,  # 因为内容更丰富，增加总结长度
                        min_length_to_summarize=50
                    )
                
                md_parts.append("## 📋 Release 包含的变更")
                md_parts.append("")
                
                for pr_number, pr_info in sorted(release_prs.items()):
                    md_parts.append(f"### PR #{pr_number}: {pr_info.title}")
                    md_parts.append(f"- **链接：** {pr_info.url}")
                    md_parts.append(f"- **状态：** {pr_info.state}")
                    md_parts.append(f"- **已合并：** {'是' if pr_info.merged else '否'}")
                    md_parts.append(f"- **作者：** {pr_info.author}")
                    
                    if pr_info.labels:
                        md_parts.append(f"- **标签：** {', '.join(pr_info.labels)}")
                    
                    # 显示聚合后的智能总结
                    md_parts.append(f"- **变更说明：**")
                    summary_key = str(pr_number)  # 使用字符串格式的数字
                    if summary_key in pr_summaries:
                        # 使用聚合总结
                        md_parts.append(f"  {pr_summaries[summary_key]}")
                    else:
                        # Fallback: 简单显示PR body
                        if pr_info.body:
                            md_parts.append(f"  {pr_info.body[:400]}{'...' if len(pr_info.body) > 400 else ''}")
                        else:
                            md_parts.append(f"  （无详细描述）")
                    
                    md_parts.append("")

        # Footer
        md_parts.append("---")
        md_parts.append("*本报告由 Containerd Release Tracker 自动生成*")

        return "\n".join(md_parts)

    def _generate_bugfix_recommendations(self, bugfixes: list, important_items: list) -> list:
        """Generate specific recommendations for bugfixes."""
        recommendations = []

        # Analyze bugfix patterns
        critical_keywords = ['panic', 'deadlock', 'crash', 'memory leak', 'corruption', 'hang']
        performance_keywords = ['slow', 'performance', 'latency', 'timeout', 'bottleneck']
        security_keywords = ['security', 'vulnerability', 'cve', 'exploit', 'privilege']

        has_critical = any(any(keyword in bugfix.lower() for keyword in critical_keywords) for bugfix in bugfixes)
        has_performance = any(any(keyword in bugfix.lower() for keyword in performance_keywords) for bugfix in bugfixes)
        has_security = any(any(keyword in bugfix.lower() for keyword in security_keywords) for bugfix in bugfixes)

        if has_critical:
            recommendations.append("🚨 **高优先级升级**：此版本修复了可能导致系统崩溃或数据损坏的严重问题，建议尽快升级")
            recommendations.append("📋 **升级前准备**：建议在升级前备份重要数据，并在测试环境中验证")

        if has_security:
            recommendations.append("🔒 **安全升级**：此版本包含安全修复，建议立即评估并升级")
            recommendations.append("🔍 **安全检查**：升级后建议检查相关安全配置和访问控制")

        if has_performance:
            recommendations.append("⚡ **性能提升**：此版本包含性能优化，可能改善系统响应速度")
            recommendations.append("📊 **性能监控**：升级后建议监控系统性能指标变化")

        # Check for important items
        for item_type, title, reason in important_items:
            if 'regression' in reason.lower():
                recommendations.append("🔄 **回归修复**：此版本修复了之前版本引入的问题，建议从受影响版本升级")
            if 'cherry-pick' in reason.lower() or 'backport' in reason.lower():
                recommendations.append("🍒 **向后移植**：此版本包含从新版本向后移植的重要修复")

        if not recommendations:
            recommendations.append("✅ **常规升级**：此版本包含常规问题修复，可按正常升级流程进行")
            recommendations.append("🧪 **测试建议**：升级前建议在测试环境中验证核心功能")

        return recommendations

    def _collect_pr_aggregated_content(self, pr_number: int, pr_info: Any, 
                                      analysis_result: AnalysisResult) -> str:
        """收集PR的所有相关内容用于聚合总结。
        
        包括：PR本身、关联的Issue、cherry-pick的原始PR（如果有）、原始PR的Issue
        """
        context_parts = []
        
        # 1. PR 基本信息
        context_parts.append(f"**PR #{pr_number}:** {pr_info.title}")
        if pr_info.labels:
            context_parts.append(f"**标签:** {', '.join(pr_info.labels)}")
        
        # 2. 如果是 cherry-pick，获取原始 PR 信息（仅 Containerd 支持）
        original_pr = None
        if hasattr(pr_info, 'cherry_pick_from') and pr_info.cherry_pick_from:
            original_pr = analysis_result.analyzed_prs.get(pr_info.cherry_pick_from)
            if original_pr:
                context_parts.append(f"\n**原始PR #{pr_info.cherry_pick_from}:** {original_pr.title}")
                if original_pr.labels:
                    context_parts.append(f"**原始PR标签:** {', '.join(original_pr.labels)}")
                if original_pr.body:
                    context_parts.append(f"**原始PR内容:** {original_pr.body}")
        
        # 3. PR 自身内容
        if pr_info.body:
            if hasattr(pr_info, 'cherry_pick_from') and pr_info.cherry_pick_from:
                context_parts.append(f"\n**Cherry-pick PR内容:** {pr_info.body}")
            else:
                context_parts.append(f"\n**PR内容:** {pr_info.body}")
        
        # 4. 收集当前PR关联的Issues
        pr_related_issues = self._extract_related_issues(pr_info, analysis_result)
        if pr_related_issues:
            context_parts.append("\n**关联的Issues:**")
            for issue_num, issue_info in pr_related_issues.items():
                context_parts.append(f"- Issue #{issue_num}: {issue_info.title}")
                if issue_info.body:
                    context_parts.append(f"  {issue_info.body[:200]}...")
        
        # 5. 收集原始PR关联的Issues（如果是cherry-pick）
        if original_pr:
            original_pr_issues = self._extract_related_issues(original_pr, analysis_result)
            if original_pr_issues:
                context_parts.append("\n**原始PR关联的Issues:**")
                for issue_num, issue_info in original_pr_issues.items():
                    context_parts.append(f"- Issue #{issue_num}: {issue_info.title}")
                    if issue_info.body:
                        context_parts.append(f"  {issue_info.body[:200]}...")
        
        return "\n".join(context_parts)
    
    def _extract_related_issues(self, pr_info: Any, analysis_result: AnalysisResult) -> Dict[int, Any]:
        """从PR中提取关联的Issues。"""
        patterns = [
            r'https://github\.com/[^/]+/[^/]+/issues/(\d+)',
            r'(?:fixes?|closes?|resolves?)\s+#(\d+)',
        ]
        
        issue_numbers = set()
        text = f"{pr_info.title} {pr_info.body}"
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            issue_numbers.update(int(match) for match in matches)
        
        # 返回已分析的Issues
        related_issues = {}
        for issue_num in issue_numbers:
            if issue_num in analysis_result.analyzed_issues:
                related_issues[issue_num] = analysis_result.analyzed_issues[issue_num]
        
        return related_issues
    
    def _get_release_mentioned_prs(self, analysis_result: AnalysisResult) -> dict:
        """获取 release notes 中直接提到的 PR。
        
        这些是要在报告中展示的主要PR，不包括通过关联发现的PR。
        
        对于 Kubernetes：从 CHANGELOG sections 中提取
        对于 Containerd：从 release body 中提取
        """
        mentioned_pr_numbers = set()
        
        # 优先从 CHANGELOG sections 中提取（Kubernetes 方式）
        if hasattr(analysis_result.release_info, 'changelog_sections') and \
           analysis_result.release_info.changelog_sections:
            for section_title, section in analysis_result.release_info.changelog_sections.items():
                mentioned_pr_numbers.update(section.pr_numbers)
        else:
            # Fallback：从 release body 中提取（Containerd 方式）
            release_body = analysis_result.release_info.body
            patterns = [
                r'https://github\.com/[^/]+/[^/]+/pull/(\d+)',
                r'(?:^|\s)#(\d+)',  # #123 格式
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, release_body, re.MULTILINE)
                mentioned_pr_numbers.update(int(match) for match in matches)
        
        # 返回这些PR（如果已分析）
        release_prs = {}
        for pr_num in mentioned_pr_numbers:
            if pr_num in analysis_result.analyzed_prs:
                release_prs[pr_num] = analysis_result.analyzed_prs[pr_num]
        
        return release_prs
    
    def _filter_important_prs(self, all_prs: dict, important_items: list) -> dict:
        """Filter PRs to only include important ones."""
        important_pr_numbers = set()

        # Get PR numbers from important items
        for item_type, title, reason in important_items:
            if item_type == "PR" and title.startswith("#"):
                try:
                    pr_number = int(title.split(":")[0][1:])
                    important_pr_numbers.add(pr_number)
                except (ValueError, IndexError):
                    pass

        # Filter PRs
        return {num: pr for num, pr in all_prs.items() if num in important_pr_numbers}

    def _filter_important_issues(self, all_issues: dict, important_items: list) -> dict:
        """Filter Issues to only include important ones."""
        important_issue_numbers = set()

        # Get issue numbers from important items
        for item_type, title, reason in important_items:
            if item_type == "Issue" and title.startswith("#"):
                try:
                    issue_number = int(title.split(":")[0][1:])
                    important_issue_numbers.add(issue_number)
                except (ValueError, IndexError):
                    pass

        # Filter issues
        return {num: issue for num, issue in all_issues.items() if num in important_issue_numbers}
    
    def _generate_json_report(self, analysis_result: AnalysisResult, 
                            llm_result: LLMAnalysisResult, filepath: str):
        """Generate JSON report for programmatic access."""
        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "tool": "containerd-release-tracker",
                "version": "1.0.0"
            },
            "release": {
                "tag_name": analysis_result.release_info.tag_name,
                "name": analysis_result.release_info.name,
                "body": analysis_result.release_info.body,
                "published_at": analysis_result.release_info.published_at,
                "prerelease": analysis_result.release_info.prerelease,
                "draft": analysis_result.release_info.draft,
                "html_url": analysis_result.release_info.html_url,
                "author": analysis_result.release_info.author
            },
            "analysis": {
                "summary": llm_result.summary,
                "key_changes": llm_result.key_changes,
                "important_bugfixes": llm_result.important_bugfixes,
                "security_issues": llm_result.security_issues,
                "performance_improvements": llm_result.performance_improvements,
                "breaking_changes": llm_result.breaking_changes,
                "recommendations": llm_result.recommendations,
                "risk_assessment": llm_result.risk_assessment
            },
            "statistics": {
                "analyzed_prs": len(analysis_result.analyzed_prs),
                "analyzed_issues": len(analysis_result.analyzed_issues),
                "important_items": len(analysis_result.important_items)
            },
            "important_items": [
                {
                    "type": item_type,
                    "title": title,
                    "reason": reason
                }
                for item_type, title, reason in analysis_result.important_items
            ]
        }
        
        if self.config.include_pr_details:
            data["prs"] = {
                str(pr_number): {
                    "title": pr_info.title,
                    "url": pr_info.url,
                    "body": pr_info.body,
                    "state": pr_info.state,
                    "merged": pr_info.merged,
                    "created_at": pr_info.created_at,
                    "merged_at": pr_info.merged_at,
                    "author": pr_info.author,
                    "labels": pr_info.labels
                }
                for pr_number, pr_info in analysis_result.analyzed_prs.items()
            }
        
        if self.config.include_issue_details:
            data["issues"] = {
                str(issue_number): {
                    "title": issue_info.title,
                    "url": issue_info.url,
                    "body": issue_info.body,
                    "state": issue_info.state,
                    "created_at": issue_info.created_at,
                    "closed_at": issue_info.closed_at,
                    "author": issue_info.author,
                    "labels": issue_info.labels
                }
                for issue_number, issue_info in analysis_result.analyzed_issues.items()
            }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
