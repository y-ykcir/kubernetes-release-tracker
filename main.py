#!/usr/bin/env python3
"""
Kubernetes Release Tracker - Main CLI Entry Point

This tool tracks Kubernetes releases, analyzes them using AI, and sends notifications.
"""

import os
import sys
import click
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import load_config
from src.tracker import KubernetesReleaseTracker


@click.group()
@click.option('--config', '-c', default='config/config.yaml', 
              help='Configuration file path')
@click.pass_context
def cli(ctx, config):
    """Kubernetes Release Tracker - Monitor and analyze Kubernetes releases."""
    ctx.ensure_object(dict)
    
    # Load configuration
    try:
        ctx.obj['config'] = load_config(config)
        ctx.obj['tracker'] = KubernetesReleaseTracker(ctx.obj['config'])
    except Exception as e:
        click.echo(f"Error loading configuration: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--no-notification', is_flag=True,
              help='Skip sending notification')
@click.option('--no-report', is_flag=True,
              help='Skip generating report')
@click.option('--include-prerelease', is_flag=True,
              help='Include prerelease versions (alpha, beta, rc, etc.)')
@click.pass_context
def analyze(ctx, no_notification, no_report, include_prerelease):
    """Run complete release analysis."""
    tracker = ctx.obj['tracker']

    success = tracker.run_analysis(
        send_notification=not no_notification,
        generate_report=not no_report,
        include_prerelease=include_prerelease
    )

    if not success:
        sys.exit(1)


@cli.command()
@click.pass_context
def test(ctx):
    """Test all external connections."""
    tracker = ctx.obj['tracker']
    
    success = tracker.test_connections()
    
    if not success:
        sys.exit(1)


@cli.command()
@click.option('--include-prerelease', is_flag=True,
              help='Include prerelease versions (alpha, beta, rc, etc.)')
@click.pass_context
def summary(ctx, include_prerelease):
    """Get a quick summary of the latest release."""
    tracker = ctx.obj['tracker']

    summary = tracker.get_release_summary(include_prerelease=include_prerelease)
    if summary:
        click.echo(summary)
    else:
        click.echo("Failed to fetch release information", err=True)
        sys.exit(1)


@cli.command()
@click.option('--message', '-m', required=True,
              help='Message to send')
@click.pass_context
def notify(ctx, message):
    """Send a test notification."""
    tracker = ctx.obj['tracker']

    success = tracker.notifier.send_simple_message(message)

    if success:
        click.echo("Notification sent successfully")
    else:
        click.echo("Failed to send notification", err=True)
        sys.exit(1)


@cli.command()
@click.option('--include-prerelease', is_flag=True,
              help='Include prerelease versions (alpha, beta, rc, etc.)')
@click.pass_context
def notify_release(ctx, include_prerelease):
    """Send release summary notification to Ruliu."""
    tracker = ctx.obj['tracker']

    click.echo("🚀 Analyzing latest release for notification...")

    # Run analysis without generating report
    success = tracker.run_analysis(
        send_notification=True,
        generate_report=False,
        include_prerelease=include_prerelease
    )

    if success:
        click.echo("✅ Release notification sent successfully")
    else:
        click.echo("❌ Failed to send release notification", err=True)
        sys.exit(1)


@cli.command()
@click.option('--include-prerelease', is_flag=True,
              help='Include prerelease versions (alpha, beta, rc, etc.)')
@click.pass_context
def preview_notification(ctx, include_prerelease):
    """Preview the notification markdown without sending."""
    from src.link_analyzer import LinkAnalyzer
    from src.llm_analyzer import LLMAnalyzer

    tracker = ctx.obj['tracker']

    click.echo("🚀 Generating notification preview...")

    # Get release info
    release_info = tracker.github_client.get_latest_release(include_prerelease=include_prerelease)
    if not release_info:
        click.echo("❌ Failed to fetch release information", err=True)
        sys.exit(1)

    click.echo(f"📡 Found release: {release_info.name} ({release_info.tag_name})")

    # Analyze
    analysis_result = tracker.link_analyzer.analyze_release(release_info)
    click.echo(f"🔍 Analyzed {len(analysis_result.analyzed_prs)} PRs and {len(analysis_result.analyzed_issues)} issues")

    # LLM analysis
    try:
        llm_result = tracker.llm_analyzer.analyze_release(analysis_result)
        click.echo("🤖 AI analysis complete")
    except Exception as e:
        click.echo(f"⚠️ AI analysis failed: {e}", err=True)
        sys.exit(1)

    # Generate markdown
    md_content = tracker.notifier._generate_markdown_content(analysis_result, llm_result)

    click.echo("\n" + "="*60)
    click.echo("📋 NOTIFICATION PREVIEW:")
    click.echo("="*60)
    click.echo(md_content)
    click.echo("="*60)


@cli.command()
@click.pass_context
def config_info(ctx):
    """Show current configuration."""
    config = ctx.obj['config']
    
    click.echo("Current Configuration:")
    click.echo(f"  GitHub Repo: {config.github.repo_owner}/{config.github.repo_name}")
    click.echo(f"  GitHub Token: {'Set' if config.github.token else 'Not set'}")
    click.echo(f"  LLM Model: {config.llm.model}")
    click.echo(f"  LLM Token: {'Set' if config.llm.token else 'Not set'}")
    click.echo(f"  Notification Token: {'Set' if config.notification.access_token else 'Not set'}")
    click.echo(f"  Target IDs: {config.notification.target_ids}")
    click.echo(f"  Max Links to Analyze: {config.analysis.max_links_to_analyze}")
    click.echo(f"  Reports Directory: {config.reports.output_dir}")


@cli.command()
def setup():
    """Setup the environment and configuration."""
    click.echo("Setting up Kubernetes Release Tracker...")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        click.echo("Creating .env file from template...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            click.echo("✅ .env file created. Please edit it with your API tokens.")
        else:
            click.echo("❌ .env.example not found")
    else:
        click.echo("✅ .env file already exists")
    
    # Create directories
    directories = ['reports', 'config']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        click.echo(f"✅ Directory created: {directory}")
    
    click.echo("\n📋 Next steps:")
    click.echo("1. Edit .env file with your API tokens:")
    click.echo("   - GITHUB_TOKEN (optional, for higher rate limits)")
    click.echo("   - QIANFAN_TOKEN (required for AI analysis)")
    click.echo("   - RULIU_ACCESS_TOKEN (required for notifications)")
    click.echo("   - RULIU_TARGET_IDS (required for notifications)")
    click.echo("\n2. Test the configuration:")
    click.echo("   python main.py test")
    click.echo("\n3. Run analysis:")
    click.echo("   python main.py analyze")


if __name__ == '__main__':
    cli()


