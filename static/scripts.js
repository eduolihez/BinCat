document.addEventListener('DOMContentLoaded', function () {
    const totalTokens = document.getElementById('total-tokens');
    const activeUsers = document.getElementById('active-users');
    const systemLogs = document.getElementById('system-logs');
    const logsTable = document.getElementById('logs-table');
    const downloadLogsButton = document.getElementById('download-logs');

    // Mock data to populate dashboard
    totalTokens.textContent = '150';
    activeUsers.textContent = '25';
    systemLogs.textContent = '120 entries';

    // Function to update logs dynamically
    function loadLogs() {
        const logs = [
            { timestamp: '2025-01-13 10:30:00', action: 'Create Token', details: 'Token ABC123 created' },
            { timestamp: '2025-01-13 11:00:00', action: 'Validate Token', details: 'Token XYZ789 validated' },
        ];

        logs.forEach(log => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${log.timestamp}</td>
                <td>${log.action}</td>
                <td>${log.details}</td>
            `;
            logsTable.appendChild(row);
        });
    }

    // Trigger loading logs
    loadLogs();

    // Log download button click event
    downloadLogsButton.addEventListener('click', function () {
        alert('Logs downloading...');
    });
});
