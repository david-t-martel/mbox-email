"""Generate interactive web dashboard for browsing emails."""

import json
import logging
from pathlib import Path
from typing import Any
from datetime import datetime

logger = logging.getLogger(__name__)


class DashboardGenerator:
    """Generate interactive HTML dashboard for email browsing."""

    def __init__(self, output_dir: Path, database_path: Path):
        """
        Initialize dashboard generator.

        Args:
            output_dir: Output directory containing emails
            database_path: Path to SQLite database
        """
        self.output_dir = Path(output_dir)
        self.database_path = Path(database_path)

    def generate(self) -> None:
        """Generate complete dashboard with index.html and data files."""
        logger.info("Generating email browser dashboard...")

        # Generate email index JSON
        email_data = self._generate_email_index()

        # Save email data as JSON
        data_file = self.output_dir / 'email_data.json'
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(email_data, f, indent=2)

        logger.info(f"Saved email data: {data_file}")

        # Generate index.html
        self._generate_index_html()

        logger.info(f"Dashboard generated: {self.output_dir / 'index.html'}")

    def _generate_email_index(self) -> dict[str, Any]:
        """
        Generate email index from database.

        Returns:
            Dictionary with email data
        """
        from ..indexing.database import EmailDatabase

        try:
            with EmailDatabase(str(self.database_path)) as db:
                cursor = db.conn.cursor()

                # Get all emails
                cursor.execute("""
                    SELECT
                        email_id,
                        message_id,
                        thread_id,
                        sender_name,
                        sender_email,
                        sender_domain,
                        subject,
                        date,
                        labels,
                        has_attachments,
                        html_path
                    FROM emails
                    ORDER BY date DESC
                """)

                emails = []
                for row in cursor.fetchall():
                    email = dict(row)
                    # Convert relative path to work from index.html location
                    if email['html_path']:
                        email['html_path'] = str(Path(email['html_path']).as_posix())
                    emails.append(email)

                # Get statistics
                stats = db.get_statistics()

                # Get unique domains
                cursor.execute("""
                    SELECT DISTINCT sender_domain
                    FROM emails
                    WHERE sender_domain IS NOT NULL AND sender_domain != ''
                    ORDER BY sender_domain
                """)
                domains = [row['sender_domain'] for row in cursor.fetchall()]

                # Get unique labels
                cursor.execute("""
                    SELECT labels
                    FROM emails
                    WHERE labels IS NOT NULL AND labels != ''
                """)
                all_labels = set()
                for row in cursor.fetchall():
                    labels = row['labels'].split(',')
                    all_labels.update([label.strip() for label in labels if label.strip()])

                return {
                    'emails': emails,
                    'statistics': stats,
                    'domains': domains,
                    'labels': sorted(list(all_labels)),
                    'generated_at': datetime.now().isoformat(),
                }

        except Exception as e:
            logger.error(f"Failed to generate email index: {e}")
            return {
                'emails': [],
                'statistics': {},
                'domains': [],
                'labels': [],
                'error': str(e),
            }

    def _generate_index_html(self) -> None:
        """Generate index.html dashboard."""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Browser Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            color: #333;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .header h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-box {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px;
        }

        .controls {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 25px;
        }

        .search-bar {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }

        .search-input {
            flex: 1;
            min-width: 300px;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }

        .search-input:focus {
            outline: none;
            border-color: #667eea;
        }

        .filter-group {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }

        .filter-group label {
            font-weight: 600;
            color: #555;
            margin-right: 5px;
        }

        select, button {
            padding: 10px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
        }

        select:hover, button:hover {
            border-color: #667eea;
        }

        button {
            background: #667eea;
            color: white;
            border: none;
            font-weight: 600;
        }

        button:hover {
            background: #5568d3;
        }

        .email-table {
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        thead {
            background: #f8f9fa;
        }

        th {
            padding: 15px 20px;
            text-align: left;
            font-weight: 600;
            color: #555;
            border-bottom: 2px solid #e0e0e0;
            cursor: pointer;
            user-select: none;
        }

        th:hover {
            background: #e9ecef;
        }

        th.sorted-asc::after {
            content: ' ↑';
        }

        th.sorted-desc::after {
            content: ' ↓';
        }

        td {
            padding: 15px 20px;
            border-bottom: 1px solid #f0f0f0;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .email-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }

        .email-link:hover {
            color: #764ba2;
            text-decoration: underline;
        }

        .label-badge {
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            margin-right: 4px;
            margin-bottom: 4px;
        }

        .attachment-icon {
            color: #ff9800;
        }

        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 10px;
            margin-top: 25px;
            padding: 20px;
        }

        .pagination button {
            min-width: 80px;
        }

        .pagination button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .page-info {
            font-weight: 600;
            color: #555;
        }

        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: #999;
            font-size: 18px;
        }

        .loading {
            text-align: center;
            padding: 60px 20px;
            color: #667eea;
            font-size: 18px;
        }

        .view-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }

        .view-tab {
            padding: 10px 20px;
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .view-tab.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }

            table {
                font-size: 14px;
            }

            th, td {
                padding: 10px;
            }

            .search-bar {
                flex-direction: column;
            }

            .search-input {
                min-width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📧 Email Browser</h1>
        <div class="stats" id="stats">
            <!-- Stats populated by JavaScript -->
        </div>
    </div>

    <div class="container">
        <div class="controls">
            <div class="search-bar">
                <input
                    type="text"
                    id="searchInput"
                    class="search-input"
                    placeholder="🔍 Search emails by subject, sender, or content..."
                >
            </div>

            <div class="filter-group">
                <label>Filter by Domain:</label>
                <select id="domainFilter">
                    <option value="">All Domains</option>
                </select>

                <label>Filter by Label:</label>
                <select id="labelFilter">
                    <option value="">All Labels</option>
                </select>

                <label>Has Attachments:</label>
                <select id="attachmentFilter">
                    <option value="">All</option>
                    <option value="yes">Yes</option>
                    <option value="no">No</option>
                </select>

                <button onclick="clearFilters()">Clear Filters</button>
            </div>

            <div class="view-tabs">
                <div class="view-tab active" onclick="changeView('date')">📅 By Date</div>
                <div class="view-tab" onclick="changeView('sender')">👤 By Sender</div>
                <div class="view-tab" onclick="changeView('thread')">💬 By Thread</div>
            </div>
        </div>

        <div class="email-table">
            <div id="loading" class="loading">Loading emails...</div>
            <table id="emailTable" style="display: none;">
                <thead>
                    <tr>
                        <th onclick="sortTable('date')">Date</th>
                        <th onclick="sortTable('sender_name')">From</th>
                        <th onclick="sortTable('subject')">Subject</th>
                        <th onclick="sortTable('labels')">Labels</th>
                        <th>📎</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="emailTableBody">
                    <!-- Populated by JavaScript -->
                </tbody>
            </table>
            <div id="noResults" class="no-results" style="display: none;">
                No emails found matching your criteria.
            </div>
        </div>

        <div class="pagination">
            <button id="prevPage" onclick="previousPage()">Previous</button>
            <span class="page-info" id="pageInfo">Page 1 of 1</span>
            <button id="nextPage" onclick="nextPage()">Next</button>
        </div>
    </div>

    <script>
        let allEmails = [];
        let filteredEmails = [];
        let currentPage = 1;
        const emailsPerPage = 50;
        let sortColumn = 'date';
        let sortDirection = 'desc';
        let currentView = 'date';

        // Load email data
        async function loadEmails() {
            try {
                const response = await fetch('email_data.json');
                const data = await response.json();

                allEmails = data.emails;
                filteredEmails = allEmails;

                // Populate filters
                populateFilters(data.domains, data.labels);

                // Display statistics
                displayStats(data.statistics);

                // Display emails
                displayEmails();

                document.getElementById('loading').style.display = 'none';
                document.getElementById('emailTable').style.display = 'table';
            } catch (error) {
                console.error('Failed to load emails:', error);
                document.getElementById('loading').textContent = 'Failed to load emails. Check console for details.';
            }
        }

        function populateFilters(domains, labels) {
            const domainFilter = document.getElementById('domainFilter');
            domains.forEach(domain => {
                const option = document.createElement('option');
                option.value = domain;
                option.textContent = domain;
                domainFilter.appendChild(option);
            });

            const labelFilter = document.getElementById('labelFilter');
            labels.forEach(label => {
                const option = document.createElement('option');
                option.value = label;
                option.textContent = label;
                labelFilter.appendChild(option);
            });
        }

        function displayStats(stats) {
            const statsDiv = document.getElementById('stats');
            statsDiv.innerHTML = `
                <div class="stat-box">
                    <div class="stat-value">${stats.total_emails?.toLocaleString() || 0}</div>
                    <div class="stat-label">Total Emails</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${stats.unique_threads?.toLocaleString() || 0}</div>
                    <div class="stat-label">Threads</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${stats.unique_domains?.toLocaleString() || 0}</div>
                    <div class="stat-label">Domains</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${stats.with_attachments?.toLocaleString() || 0}</div>
                    <div class="stat-label">With Attachments</div>
                </div>
            `;
        }

        function displayEmails() {
            const tbody = document.getElementById('emailTableBody');
            tbody.innerHTML = '';

            // Calculate pagination
            const start = (currentPage - 1) * emailsPerPage;
            const end = start + emailsPerPage;
            const pageEmails = filteredEmails.slice(start, end);

            if (pageEmails.length === 0) {
                document.getElementById('emailTable').style.display = 'none';
                document.getElementById('noResults').style.display = 'block';
                return;
            }

            document.getElementById('emailTable').style.display = 'table';
            document.getElementById('noResults').style.display = 'none';

            pageEmails.forEach(email => {
                const row = document.createElement('tr');

                // Format date
                const date = email.date ? new Date(email.date).toLocaleDateString() : 'Unknown';

                // Format sender
                const sender = email.sender_name || email.sender_email || 'Unknown';

                // Format labels
                const labels = email.labels ? email.labels.split(',').map(label =>
                    `<span class="label-badge">${label.trim()}</span>`
                ).join('') : '';

                // Attachment icon
                const attachmentIcon = email.has_attachments ? '<span class="attachment-icon">📎</span>' : '';

                // Generate proper path based on view
                let emailPath = email.html_path;
                if (currentView === 'date') {
                    emailPath = email.html_path;
                } else if (currentView === 'sender') {
                    emailPath = email.html_path.replace('/by-date/', '/by-sender/');
                } else if (currentView === 'thread') {
                    emailPath = email.html_path.replace('/by-date/', '/by-thread/');
                }

                row.innerHTML = `
                    <td>${date}</td>
                    <td><strong>${sender}</strong><br><small>${email.sender_email || ''}</small></td>
                    <td><a href="${emailPath}" target="_blank" class="email-link">${email.subject || '(No Subject)'}</a></td>
                    <td>${labels}</td>
                    <td>${attachmentIcon}</td>
                    <td><a href="${emailPath}" target="_blank" class="email-link">Open</a></td>
                `;

                tbody.appendChild(row);
            });

            updatePagination();
        }

        function updatePagination() {
            const totalPages = Math.ceil(filteredEmails.length / emailsPerPage);
            document.getElementById('pageInfo').textContent = `Page ${currentPage} of ${totalPages}`;
            document.getElementById('prevPage').disabled = currentPage === 1;
            document.getElementById('nextPage').disabled = currentPage === totalPages;
        }

        function nextPage() {
            const totalPages = Math.ceil(filteredEmails.length / emailsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                displayEmails();
                window.scrollTo(0, 0);
            }
        }

        function previousPage() {
            if (currentPage > 1) {
                currentPage--;
                displayEmails();
                window.scrollTo(0, 0);
            }
        }

        function sortTable(column) {
            if (sortColumn === column) {
                sortDirection = sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn = column;
                sortDirection = 'desc';
            }

            filteredEmails.sort((a, b) => {
                let valA = a[column] || '';
                let valB = b[column] || '';

                if (column === 'date') {
                    valA = new Date(valA);
                    valB = new Date(valB);
                }

                if (sortDirection === 'asc') {
                    return valA > valB ? 1 : -1;
                } else {
                    return valA < valB ? 1 : -1;
                }
            });

            // Update table headers
            document.querySelectorAll('th').forEach(th => {
                th.classList.remove('sorted-asc', 'sorted-desc');
            });
            event.target.classList.add(`sorted-${sortDirection}`);

            currentPage = 1;
            displayEmails();
        }

        function filterEmails() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const domainFilter = document.getElementById('domainFilter').value;
            const labelFilter = document.getElementById('labelFilter').value;
            const attachmentFilter = document.getElementById('attachmentFilter').value;

            filteredEmails = allEmails.filter(email => {
                // Search filter
                const searchMatch = !searchTerm ||
                    (email.subject && email.subject.toLowerCase().includes(searchTerm)) ||
                    (email.sender_name && email.sender_name.toLowerCase().includes(searchTerm)) ||
                    (email.sender_email && email.sender_email.toLowerCase().includes(searchTerm));

                // Domain filter
                const domainMatch = !domainFilter || email.sender_domain === domainFilter;

                // Label filter
                const labelMatch = !labelFilter || (email.labels && email.labels.includes(labelFilter));

                // Attachment filter
                const attachmentMatch = !attachmentFilter ||
                    (attachmentFilter === 'yes' && email.has_attachments) ||
                    (attachmentFilter === 'no' && !email.has_attachments);

                return searchMatch && domainMatch && labelMatch && attachmentMatch;
            });

            currentPage = 1;
            displayEmails();
        }

        function clearFilters() {
            document.getElementById('searchInput').value = '';
            document.getElementById('domainFilter').value = '';
            document.getElementById('labelFilter').value = '';
            document.getElementById('attachmentFilter').value = '';
            filterEmails();
        }

        function changeView(view) {
            currentView = view;

            // Update active tab
            document.querySelectorAll('.view-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');

            displayEmails();
        }

        // Event listeners
        document.getElementById('searchInput').addEventListener('input', filterEmails);
        document.getElementById('domainFilter').addEventListener('change', filterEmails);
        document.getElementById('labelFilter').addEventListener('change', filterEmails);
        document.getElementById('attachmentFilter').addEventListener('change', filterEmails);

        // Load emails on page load
        loadEmails();
    </script>
</body>
</html>
"""

        index_path = self.output_dir / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"Generated index.html: {index_path}")
