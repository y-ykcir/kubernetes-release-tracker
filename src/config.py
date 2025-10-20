"""Configuration management for the kubernetes release tracker."""

import os
import yaml
from typing import Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class GitHubConfig(BaseModel):
    """GitHub API configuration."""
    api_url: str = "https://api.github.com"
    repo_owner: str = "kubernetes"
    repo_name: str = "kubernetes"
    token: str = Field(default="", description="GitHub API token")
    # Kubernetes CHANGELOG 文件的 URL 模板
    changelog_url_template: str = "https://raw.githubusercontent.com/kubernetes/kubernetes/master/CHANGELOG/CHANGELOG-{version}.md"


class LLMConfig(BaseModel):
    """LLM API configuration."""
    api_url: str = "https://qianfan.baidubce.com/v2/chat/completions"
    model: str = "deepseek-r1"
    token: str = Field(default="", description="LLM API token")
    max_tokens: int = 4000
    temperature: float = 0.1


class NotificationConfig(BaseModel):
    """Notification configuration."""
    webhook_url: str = "http://api.im.baidu.com/api/msg/groupmsgsend"
    access_token: str = Field(default="", description="Notification access token")
    target_ids: List[int] = Field(default_factory=list, description="Target user IDs")


class AnalysisConfig(BaseModel):
    """Analysis configuration."""
    max_links_to_analyze: int = 50  # Kubernetes 有更多的 PR，增加分析数量
    important_keywords: List[str] = Field(default_factory=lambda: [
        "panic", "deadlock", "crash", "security", "vulnerability",
        "memory leak", "performance", "critical", "urgent", "regression",
        "breaking change", "deprecation", "CVE"
    ])
    # Kubernetes 特有的配置
    parse_changelog: bool = True  # 是否解析 CHANGELOG 文件
    focus_sections: List[str] = Field(default_factory=lambda: [
        "Urgent Upgrade Notes",
        "Changes by Kind",
        "Deprecation",
        "API Change",
        "Breaking Change",
        "Security",
        "Bug or Regression"
    ])


class ReportsConfig(BaseModel):
    """Reports configuration."""
    output_dir: str = "reports"
    template_dir: str = "templates"
    include_full_analysis: bool = True
    include_pr_details: bool = True
    include_issue_details: bool = True


class Config(BaseModel):
    """Main configuration class."""
    github: GitHubConfig = Field(default_factory=GitHubConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    notification: NotificationConfig = Field(default_factory=NotificationConfig)
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    reports: ReportsConfig = Field(default_factory=ReportsConfig)


def load_config(config_file: str = "config/config.yaml") -> Config:
    """Load configuration from file and environment variables."""
    # Load environment variables
    load_dotenv()
    
    # Load YAML configuration
    config_data = {}
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f) or {}
    
    # Create config object
    config = Config(**config_data)
    
    # Override with environment variables
    config.github.token = os.getenv("GITHUB_TOKEN", config.github.token)
    config.llm.token = os.getenv("QIANFAN_TOKEN", config.llm.token)
    config.notification.access_token = os.getenv("RULIU_ACCESS_TOKEN", config.notification.access_token)
    
    # Parse target IDs from environment
    target_ids_str = os.getenv("RULIU_TARGET_IDS", "")
    if target_ids_str:
        try:
            import json
            config.notification.target_ids = json.loads(target_ids_str)
        except json.JSONDecodeError:
            pass
    
    return config


