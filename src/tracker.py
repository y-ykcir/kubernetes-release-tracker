"""Main tracker module that orchestrates the Kubernetes release analysis process."""

from typing import Optional
import sys

from .config import Config
from .github_client import GitHubClient
from .link_analyzer import LinkAnalyzer
from .llm_analyzer import LLMAnalyzer
from .notifier import RuliuNotifier
from .report_generator import ReportGenerator


class KubernetesReleaseTracker:
    """Main tracker class that orchestrates the Kubernetes release analysis."""
    
    def __init__(self, config: Config):
        self.config = config
        self.github_client = GitHubClient(config.github)
        self.link_analyzer = LinkAnalyzer(self.github_client, config.analysis)
        self.llm_analyzer = LLMAnalyzer(config.llm)
        self.notifier = RuliuNotifier(config.notification)
        self.report_generator = ReportGenerator(config.reports, self.llm_analyzer)
    
    def run_analysis(self, send_notification: bool = True,
                    generate_report: bool = True, include_prerelease: bool = False) -> bool:
        """Run complete release analysis."""
        print("🚀 Starting Kubernetes Release Analysis...")

        # Step 1: Get latest release
        if include_prerelease:
            print("📡 Fetching latest release information (including prereleases)...")
        else:
            print("📡 Fetching latest release information...")
        release_info = self.github_client.get_latest_release(include_prerelease=include_prerelease)
        if not release_info:
            print("❌ Failed to fetch release information")
            return False
        
        print(f"✅ Found release: {release_info.name} ({release_info.tag_name})")
        
        if release_info.changelog_url:
            print(f"📚 CHANGELOG URL: {release_info.changelog_url}")
            print(f"📊 Parsed {len(release_info.changelog_sections)} CHANGELOG sections")
        
        # Step 2: Analyze links and gather detailed information
        print("🔍 Analyzing PRs and issues from CHANGELOG...")
        analysis_result = self.link_analyzer.analyze_release(release_info)
        
        print(f"✅ Analysis complete:")
        print(f"   - Analyzed PRs: {len(analysis_result.analyzed_prs)}")
        print(f"   - Analyzed Issues: {len(analysis_result.analyzed_issues)}")
        print(f"   - Important Items: {len(analysis_result.important_items)}")
        
        # Step 3: LLM analysis
        print("🤖 Running AI analysis...")
        try:
            llm_result = self.llm_analyzer.analyze_release(analysis_result)
            print("✅ AI analysis complete")
        except Exception as e:
            print(f"⚠️ AI analysis failed: {e}")
            # Create empty LLM result to continue
            from .llm_analyzer import LLMAnalysisResult
            llm_result = LLMAnalysisResult(
                summary="AI analysis unavailable",
                key_changes=[],
                important_bugfixes=[],
                security_issues=[],
                performance_improvements=[],
                breaking_changes=[],
                recommendations=[],
                risk_assessment=""
            )
        
        # Step 4: Generate report
        if generate_report:
            print("📄 Generating report...")
            try:
                report_path = self.report_generator.generate_report(analysis_result, llm_result)
                print(f"✅ Report generated: {report_path}")
            except Exception as e:
                print(f"⚠️ Report generation failed: {e}")
        
        # Step 5: Send notification
        if send_notification:
            print("📢 Sending notification...")
            try:
                success = self.notifier.send_release_notification(analysis_result, llm_result)
                if success:
                    print("✅ Notification sent successfully")
                else:
                    print("⚠️ Notification failed")
            except Exception as e:
                print(f"⚠️ Notification failed: {e}")
        
        print("🎉 Analysis complete!")
        return True
    
    def test_connections(self) -> bool:
        """Test all external connections."""
        print("🧪 Testing connections...")
        
        # Test GitHub API
        print("Testing GitHub API...")
        release = self.github_client.get_latest_release()
        if release:
            print(f"✅ GitHub API: OK (Latest: {release.tag_name})")
        else:
            print("❌ GitHub API: Failed")
            return False
        
        # Test LLM API
        print("Testing LLM API...")
        try:
            test_response = self.llm_analyzer._call_llm("Test message")
            if "Error" not in test_response:
                print("✅ LLM API: OK")
            else:
                print(f"❌ LLM API: {test_response}")
                return False
        except Exception as e:
            print(f"❌ LLM API: {e}")
            return False
        
        # Test Ruliu notification
        print("Testing Ruliu notification...")
        try:
            success = self.notifier.test_connection()
            if success:
                print("✅ Ruliu API: OK")
            else:
                print("❌ Ruliu API: Failed")
                return False
        except Exception as e:
            print(f"❌ Ruliu API: {e}")
            return False
        
        print("✅ All connections tested successfully!")
        return True
    
    def get_release_summary(self, include_prerelease: bool = False) -> Optional[str]:
        """Get a quick summary of the latest release."""
        release_info = self.github_client.get_latest_release(include_prerelease=include_prerelease)
        if not release_info:
            return None
        
        summary_parts = [
            f"Latest Kubernetes Release: {release_info.name}",
            f"Tag: {release_info.tag_name}",
            f"Published: {release_info.published_at}",
            f"Author: {release_info.author}",
            f"Prerelease: {release_info.prerelease}",
            f"URL: {release_info.html_url}",
        ]
        
        if release_info.changelog_url:
            summary_parts.append(f"CHANGELOG: {release_info.changelog_url}")
            summary_parts.append(f"CHANGELOG Sections: {len(release_info.changelog_sections)}")
        
        summary_parts.extend([
            "",
            "Release Notes Preview:",
            release_info.body[:500] + ('...' if len(release_info.body) > 500 else ''),
        ])
        
        return "\n".join(summary_parts)


