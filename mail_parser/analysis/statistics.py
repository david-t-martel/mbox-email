"""Email statistics and analytics."""

import logging
from typing import Any
from collections import defaultdict, Counter
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)


class EmailStatistics:
    """Collect and analyze email statistics."""

    def __init__(self):
        """Initialize statistics collector."""
        self.total_emails = 0
        self.emails_by_date = defaultdict(int)
        self.emails_by_hour = defaultdict(int)
        self.emails_by_dow = defaultdict(int)  # Day of week
        self.emails_by_sender = defaultdict(int)
        self.emails_by_domain = defaultdict(int)
        self.emails_with_attachments = 0
        self.total_attachment_size = 0
        self.labels_count = Counter()
        self.threads = set()

    def add_email(self, metadata: dict[str, Any], attachments: list[dict[str, Any]]) -> None:
        """
        Add email to statistics.

        Args:
            metadata: Email metadata
            attachments: List of attachments
        """
        self.total_emails += 1

        # Date statistics
        date = metadata.get('date')
        if isinstance(date, datetime):
            date_key = date.strftime('%Y-%m-%d')
            self.emails_by_date[date_key] += 1

            hour = date.hour
            self.emails_by_hour[hour] += 1

            dow = date.strftime('%A')  # Day name
            self.emails_by_dow[dow] += 1

        # Sender statistics
        from_addr = metadata.get('from', {})
        sender_email = from_addr.get('email', 'unknown')
        self.emails_by_sender[sender_email] += 1

        # Domain statistics
        if '@' in sender_email:
            domain = sender_email.split('@')[1]
            self.emails_by_domain[domain] += 1

        # Attachment statistics
        if attachments:
            self.emails_with_attachments += 1
            total_size = sum(att.get('size', 0) for att in attachments)
            self.total_attachment_size += total_size

        # Label statistics
        labels = metadata.get('gmail_labels', [])
        for label in labels:
            self.labels_count[label] += 1

        # Thread statistics
        thread_id = metadata.get('gmail_thread_id')
        if thread_id:
            self.threads.add(thread_id)

    def get_summary(self) -> dict[str, Any]:
        """
        Get statistics summary.

        Returns:
            Dictionary of statistics
        """
        return {
            'total_emails': self.total_emails,
            'unique_threads': len(self.threads),
            'emails_with_attachments': self.emails_with_attachments,
            'total_attachment_size': self.total_attachment_size,
            'unique_senders': len(self.emails_by_sender),
            'unique_domains': len(self.emails_by_domain),
            'unique_labels': len(self.labels_count),
            'top_senders': dict(Counter(self.emails_by_sender).most_common(20)),
            'top_domains': dict(Counter(self.emails_by_domain).most_common(20)),
            'top_labels': dict(self.labels_count.most_common(20)),
            'emails_by_hour': dict(self.emails_by_hour),
            'emails_by_dow': dict(self.emails_by_dow),
        }

    def to_dataframe(self) -> dict[str, pd.DataFrame]:
        """
        Convert statistics to pandas DataFrames.

        Returns:
            Dictionary of DataFrames
        """
        return {
            'daily': pd.DataFrame([
                {'date': date, 'count': count}
                for date, count in sorted(self.emails_by_date.items())
            ]),
            'hourly': pd.DataFrame([
                {'hour': hour, 'count': count}
                for hour, count in sorted(self.emails_by_hour.items())
            ]),
            'dow': pd.DataFrame([
                {'day': day, 'count': count}
                for day, count in self.emails_by_dow.items()
            ]),
            'top_senders': pd.DataFrame([
                {'sender': sender, 'count': count}
                for sender, count in Counter(self.emails_by_sender).most_common(50)
            ]),
            'top_domains': pd.DataFrame([
                {'domain': domain, 'count': count}
                for domain, count in Counter(self.emails_by_domain).most_common(50)
            ]),
            'top_labels': pd.DataFrame([
                {'label': label, 'count': count}
                for label, count in self.labels_count.most_common(50)
            ]),
        }

    def generate_html_report(self, output_path: str) -> None:
        """
        Generate HTML analytics report with charts.

        Args:
            output_path: Output HTML file path
        """
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        summary = self.get_summary()
        dfs = self.to_dataframe()

        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Emails Over Time',
                'Emails by Hour of Day',
                'Top 10 Senders',
                'Top 10 Domains',
                'Top 10 Labels',
                'Emails by Day of Week'
            ),
            specs=[
                [{'type': 'scatter'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'bar'}, {'type': 'bar'}]
            ]
        )

        # Daily emails
        if not dfs['daily'].empty:
            fig.add_trace(
                go.Scatter(
                    x=dfs['daily']['date'],
                    y=dfs['daily']['count'],
                    mode='lines',
                    name='Daily Emails'
                ),
                row=1, col=1
            )

        # Hourly distribution
        if not dfs['hourly'].empty:
            fig.add_trace(
                go.Bar(
                    x=dfs['hourly']['hour'],
                    y=dfs['hourly']['count'],
                    name='Hourly'
                ),
                row=1, col=2
            )

        # Top senders
        if not dfs['top_senders'].empty:
            top_10_senders = dfs['top_senders'].head(10)
            fig.add_trace(
                go.Bar(
                    x=top_10_senders['count'],
                    y=top_10_senders['sender'],
                    orientation='h',
                    name='Top Senders'
                ),
                row=2, col=1
            )

        # Top domains
        if not dfs['top_domains'].empty:
            top_10_domains = dfs['top_domains'].head(10)
            fig.add_trace(
                go.Bar(
                    x=top_10_domains['count'],
                    y=top_10_domains['domain'],
                    orientation='h',
                    name='Top Domains'
                ),
                row=2, col=2
            )

        # Top labels
        if not dfs['top_labels'].empty:
            top_10_labels = dfs['top_labels'].head(10)
            fig.add_trace(
                go.Bar(
                    x=top_10_labels['count'],
                    y=top_10_labels['label'],
                    orientation='h',
                    name='Top Labels'
                ),
                row=3, col=1
            )

        # Day of week
        if not dfs['dow'].empty:
            # Order days correctly
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_df = dfs['dow'].set_index('day').reindex(day_order).reset_index().fillna(0)

            fig.add_trace(
                go.Bar(
                    x=dow_df['day'],
                    y=dow_df['count'],
                    name='Day of Week'
                ),
                row=3, col=2
            )

        # Update layout
        fig.update_layout(
            height=1200,
            showlegend=False,
            title_text=f"Email Analytics - {summary['total_emails']:,} Emails"
        )

        # Create HTML with summary
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Email Analytics Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Email Analytics Report</h1>

        <div class="summary">
            <div class="stat-box">
                <div class="stat-label">Total Emails</div>
                <div class="stat-value">{summary['total_emails']:,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Unique Threads</div>
                <div class="stat-value">{summary['unique_threads']:,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Unique Senders</div>
                <div class="stat-value">{summary['unique_senders']:,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">With Attachments</div>
                <div class="stat-value">{summary['emails_with_attachments']:,}</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Total Attachment Size</div>
                <div class="stat-value">{summary['total_attachment_size'] / (1024**3):.2f} GB</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">Unique Labels</div>
                <div class="stat-value">{summary['unique_labels']:,}</div>
            </div>
        </div>

        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
</body>
</html>
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"Analytics report saved to {output_path}")
