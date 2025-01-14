document.addEventListener('DOMContentLoaded', () => {
    const tokenForm = document.getElementById('token-form');
    const fetchTokensButton = document.getElementById('fetch-tokens');
    const fetchLogsButton = document.getElementById('fetch-logs');
    const tokenList = document.getElementById('token-list');
    const logList = document.getElementById('log-list');

    // Handle form submission
    tokenForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const action = document.querySelector('input[name="action"]:checked').value;
        const tokenInput = document.getElementById('token-input').value;

        let url = '';
        let data = {};

        if (action === 'generate') {
            url = '/generate-token';
        } else if (action === 'validate') {
            url = '/validate-token';
            data = { token: tokenInput };
        } else if (action === 'purge') {
            url = '/purge-tokens';
        }

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        alert(result.message);
    });

    // Fetch all tokens
    fetchTokensButton.addEventListener('click', async () => {
        const response = await fetch('/fetch-tokens');
        const tokens = await response.json();

        tokenList.innerHTML = '';
        tokens.forEach(token => {
            const li = document.createElement('li');
            li.textContent = token;
            tokenList.appendChild(li);
        });
    });

    // Fetch logs
    fetchLogsButton.addEventListener('click', async () => {
        const response = await fetch('/fetch-logs');
        const logs = await response.json();

        logList.innerHTML = '';
        logs.forEach(log => {
            const li = document.createElement('li');
            li.textContent = log;
            logList.appendChild(li);
        });
    });
});
