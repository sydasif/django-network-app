document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    let lastHostListData = null;

    // Handle "Open in New Window" button click
    document.getElementById('openNewWindow').addEventListener('click', function() {
        if (lastHostListData && lastHostListData.host_list) {
            const newWindow = window.open('', '_blank', 'width=600,height=800');
            newWindow.document.write(`
                <html>
                <head>
                    <title>CIDR Host List</title>
                    <style>
                        body { font-family: Arial, sans-serif; padding: 20px; }
                        table { width: 100%; border-collapse: collapse; }
                        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                        th { background-color: #f2f2f2; }
                    </style>
                </head>
                <body>
                    <h2>Host List</h2>
                    <table>
                        <thead>
                            <tr><th>IP Address</th></tr>
                        </thead>
                        <tbody>
                            ${lastHostListData.host_list.map(host => `<tr><td>${host}</td></tr>`).join('')}
                        </tbody>
                    </table>
                </body>
                </html>
            `);
            newWindow.document.close();
        } else {
            alert('Please generate a host list first');
        }
    });

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);
            const params = new URLSearchParams(formData);

            fetch('/ip_addr/?' + params.toString(), {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // Clear all result areas
                document.getElementById('netmask_result_display').innerHTML = '';
                document.getElementById('cidr_result_display').innerHTML = '';
                document.getElementById('netmask_v6_result_display').innerHTML = '';
                document.getElementById('host_list_display').innerHTML = '';
                document.getElementById('host_list_error_display').innerHTML = '';

                // Store host list data if present
                if (data.host_list) {
                    lastHostListData = data;
                }

                // Update the appropriate result area
                if (data.netmask_result) {
                    document.getElementById('netmask_result_display').innerHTML = data.netmask_result;
                } else if (data.cidr_result) {
                    document.getElementById('cidr_result_display').innerHTML = data.cidr_result;
                } else if (data.netmask_v6_result) {
                    document.getElementById('netmask_v6_result_display').innerHTML = data.netmask_v6_result;
                } else if (data.host_list) {
                    let hostListHTML = '<div style="height: 200px; overflow-y: scroll; border: 1px solid #ccc; padding: 5px;">';
                    hostListHTML += '<table style="width: 100%; border-collapse: collapse;">';
                    hostListHTML += '<thead><tr><th style="border: 1px solid #ccc; padding: 8px; text-align: left;">IP Address</th></tr></thead>';
                    hostListHTML += '<tbody>';
                    data.host_list.forEach(host => {
                        hostListHTML += `<tr><td style="border: 1px solid #ccc; padding: 8px;">${host}</td></tr>`;
                    });
                    hostListHTML += '</tbody></table></div>';
                    document.getElementById('host_list_display').innerHTML = hostListHTML;
                } else if (data.host_list_error) {
                    document.getElementById('host_list_error_display').innerHTML = data.host_list_error;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
